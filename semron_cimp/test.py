# 3D cell array 
# K layers --> y --> the bitline goes through this K
# M columns --> x 
# N rows --> z 
import math
import sys
import time
import datetime
import numpy as np
import pandas as pd

class CIMP_Analyzer:
    def __init__(self):
        self.Cmax = 1e-15
        self.Vin = 0.4
        self.Sx = 1
        self.T = 330
        self.kT = 1.380649e-23 * self.T
        self.time_per_avg_ns = 40.0
        self.adc_baseline_fJ = 0.25
        self.cell_size_um2 = 0.3528594971 #based on the 3D NAND tech. 

        self.tech_limits_pct = {
            'duv': 0.71,
            'immersion': 0.11,
            'sonos': 0.062,
            'ideal': 0.0001
        }

    def get_max_feasible_K(self, Sw, tech='immersion'):
        limit_pct = self.tech_limits_pct.get(tech.lower(), self.tech_limits_pct['immersion'])
        Sw_eff = max(Sw, 2)
        K_max = (100.0 / (limit_pct * 6.0 * (2**(Sw_eff - 1) - 1)))**2
        return K_max

    def evaluate_configuration(self, K, r, Sw, M, N, Lx): 
        Sw_eff = max(Sw, 2)
        By_phys = 10 + math.log2(K / 128)
        By_sig = 8 + math.log2(K / 128)
        Cmin = self.Cmax / r
        Cpar = K * Cmin
        Ncap = (2**By_phys) / ((2**Sw_eff) * (2**self.Sx))
        Ctot = (K * Cmin) + Cpar + (Ncap * self.Cmax)

        term1 = 36 * self.kT * Ctot
        term2 = ((2**(Sw_eff - 1) - 1)**2) * ((2**self.Sx - 1)**2)
        term3 = ((self.Cmax - Cmin)**2) * (self.Vin**2)

        Nav = max((term1 * term2) / term3, 1.0)
        mac_latency_ns = Lx * Nav * self.time_per_avg_ns

        Q_LSB = ((self.Cmax - Cmin) / (2**(Sw_eff - 1) - 1)) * (self.Vin / (2**self.Sx - 1))
        energy_signal = (Lx * Nav * Q_LSB * self.Vin * (2**By_sig)) / K
        energy_wasted = Lx * Nav * Cmin * (self.Vin**2)
        Ecap_MAC_J = energy_signal + energy_wasted

        Ecap_fJ_bOP = (Ecap_MAC_J * 1e15) / (Lx * Sw)
        Eadc_fJ_bOP = self.adc_baseline_fJ * (4.0 / Sw)
        Etot_fJ_bOP = Ecap_fJ_bOP + Eadc_fJ_bOP

        # --- EFFICIENCY MATH ---
        pops_w_b = 1.0 / Etot_fJ_bOP
        # Multiply by 1000 (Peta to Tera), divide by bit-ops (Lx*Sw), multiply by 2 (for MAC)
        mac_tops_w = (pops_w_b * 1000.0 / (Lx * Sw)) * 2.0

        # --- SPEED MATH ---
        total_bit_ops = K * M * Lx * Sw
        throughput_tbops = total_bit_ops / (mac_latency_ns * 1e-9) / 1e12
        # Divide by bit-ops (Lx*Sw), multiply by 2 (for MAC)
        mac_tops = (throughput_tbops / (Lx * Sw)) * 2.0

        edp = Etot_fJ_bOP * mac_latency_ns
        total_energy_pJ = (Etot_fJ_bOP * total_bit_ops) / 1000.0

        #area of the cell array
        cell_array_size = (N * M * self.cell_size_um2) / 1e6

        return {
            'K': K, 'Cols(M)': M, 'ON/OFF': r, 'Sw': Sw, 'Lx': Lx,
            'Latency(ns)': round(mac_latency_ns, 1),
            'TbOPS': round(throughput_tbops, 3),
            'MAC TOPS': round(mac_tops, 3),
            'Total E(pJ)': round(total_energy_pJ, 2),
            'Ecap(fJ/bOP)': round(Ecap_fJ_bOP, 3),
            'Eadc(fJ/bOP)': round(Eadc_fJ_bOP, 3),
            'Etot(fJ/bOP)': round(Etot_fJ_bOP, 3),
            'POPS/W/b': round(pops_w_b, 1),
            'MAC TOPS/W': round(mac_tops_w, 1),
            'EDP': round(edp, 2), 
            'Cell Array Area (mm^2)': round(cell_array_size, 3), 
        }

    def run_design_space_exploration(self, tech, K_range, r_range, Sw_range, M_range, Lx_range):
        # --- SMART INPUT PARSING ---
        if not K_range: K_range = list(range(128, 8193, 128)) # should be low
        if not r_range: r_range = list(range(5, 101, 1))      # should be high
        if not Sw_range: Sw_range = [1, 2, 3, 4, 5, 6]        # should be low
        if not M_range: M_range = list(range(128, 8193, 128)) # should be high
        if not Lx_range: Lx_range = [4, 8, 16, 32]            # should be low

        valid_results = []
        total_iters = len(Sw_range) * len(K_range) * len(r_range) * len(M_range) * len(Lx_range)
        current_iter = 0
        start_time = time.time()

        for Sw in Sw_range:
            max_K = self.get_max_feasible_K(Sw, tech)
            for K in K_range:
                # ⚡ MASSIVE SPEED OPTIMIZATION
                if K > max_K:
                    skipped = len(r_range) * len(M_range) * len(Lx_range)
                    current_iter += skipped
                    continue

                for r in r_range:
                    for M in M_range:
                        for Lx in Lx_range:
                            current_iter += 1

                            if current_iter % 100000 == 0 or current_iter >= total_iters:
                                elapsed_time = time.time() - start_time
                                iters_per_sec = current_iter / elapsed_time if elapsed_time > 0 else 1
                                remaining_iters = total_iters - current_iter
                                eta_seconds = remaining_iters / iters_per_sec
                                eta_str = str(datetime.timedelta(seconds=int(eta_seconds)))
                                percent = (current_iter / total_iters) * 100
                                bar = '█' * int(percent / 2) + '-' * (50 - int(percent / 2))
                                sys.stdout.write(f'\r[{bar}] {percent:.1f}% | ETA: {eta_str} | ({current_iter}/{total_iters})')
                                sys.stdout.flush()

                            res = self.evaluate_configuration(K, r, Sw, M, Lx)
                            valid_results.append(res)

        print()
        return pd.DataFrame(valid_results)

if __name__ == "__main__":
    analyzer = CIMP_Analyzer()
    technology = 'immersion'

    allowed_Ks = [1024]
    allowed_Sws = [1]
    allowed_rs = [100]
    allowed_Ms = [1024]
    allowed_Lxs = [4]

    print(f"--- Running Massive Hardware Search (Tech: {technology.upper()}) ---")
    df = analyzer.run_design_space_exploration(technology, allowed_Ks, allowed_rs, allowed_Sws, allowed_Ms, allowed_Lxs)

    print(f"\nTotal feasible configurations found: {len(df)}")

    if len(df) > 0:
        # --- The unified layout requested ---
        display_cols = [
            'K', 'Cols(M)', 'ON/OFF', 'Sw', 'Lx',
            'Latency(ns)', 'TbOPS', 'MAC TOPS', 'Total E(pJ)',
            'Ecap(fJ/bOP)', 'Eadc(fJ/bOP)', 'Etot(fJ/bOP)',
            'POPS/W/b', 'MAC TOPS/W', 'EDP', 'Cell Array Area (mm^2)'
        ]

        # ---------------------------------------------------------
        # 1. PURE ENERGY EFFICIENCY
        # Now sorted by the true MAC TOPS/W
        # ---------------------------------------------------------
        print("\n🏆 BEST FOR PURE ENERGY EFFICIENCY (Highest MAC TOPS/W)")
        eff_cols = ['MAC TOPS/W', 'Etot(fJ/bOP)', 'EDP', 'MAC TOPS', 'Total E(pJ)']
        eff_asc  = [False,        True,           True,  False,      True]
        df_eff = df.sort_values(by=eff_cols, ascending=eff_asc)
        print(df_eff[display_cols].head(3).to_string(index=False, justify='center', col_space=10))

        # ---------------------------------------------------------
        # 2. PURE SPEED (Lowest Latency)
        # ---------------------------------------------------------
        print("\n🏆 BEST FOR PURE SPEED (Lowest Latency)")
        spd_cols = ['Latency(ns)', 'EDP', 'MAC TOPS', 'MAC TOPS/W', 'Total E(pJ)']
        spd_asc  = [True,          True,  False,      False,        True]
        df_spd = df.sort_values(by=spd_cols, ascending=spd_asc)
        print(df_spd[display_cols].head(3).to_string(index=False, justify='center', col_space=10))

        # ---------------------------------------------------------
        # 3. OVERALL BALANCE (Lowest EDP)
        # ---------------------------------------------------------
        print("\n🏆 BEST OVERALL BALANCE (Lowest EDP)")
        edp_cols = ['EDP', 'MAC TOPS/W', 'MAC TOPS', 'Latency(ns)', 'Total E(pJ)']
        edp_asc  = [True,  False,        False,      True,          True]
        df_edp = df.sort_values(by=edp_cols, ascending=edp_asc)
        print(df_edp[display_cols].head(3).to_string(index=False, justify='center', col_space=10))

        # ---------------------------------------------------------
        # 4. MASSIVE THROUGHPUT (Highest MAC TOPS)
        # Now sorted by true MAC TOPS
        # ---------------------------------------------------------
        print("\n🏆 BEST FOR MASSIVE THROUGHPUT (Highest MAC TOPS)")
        top_cols = ['MAC TOPS', 'MAC TOPS/W', 'EDP', 'Latency(ns)', 'Total E(pJ)']
        top_asc  = [False,      False,        True,  True,          True]
        df_top = df.sort_values(by=top_cols, ascending=top_asc)
        print(df_top[display_cols].head(3).to_string(index=False, justify='center', col_space=10))