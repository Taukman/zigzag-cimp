# 3D cell array with ADC grouping
# K layers --> y --> the bitline goes through K layers (one pillar)
# M columns --> x
# N rows --> z
# g = number of pillars sharing one ADC (analog sum before digitization)
# K_eff = K * g = effective column length seen by the shared ADC

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
        self.cell_size_um2 = 0.3528594971

        # Calibrated ADC FOM: at K=128, Sw=4 → Eadc=0.25 fJ/bOP
        self.FOM_W = 0.5  # fJ/conv-step

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

    def evaluate_configuration(self, K, r, Sw, M, N, Lx, g):
        Sw_eff = max(Sw, 2)

        # --- Grouping: g pillars share one ADC ---
        K_eff = K * g                          # effective column length for noise & By
        num_pillars = M * N                    # total pillars in the array
        num_adcs = math.ceil(num_pillars / g)  # ADCs needed

        # --- By uses K_eff (combined bitline dynamic range) ---
        By_phys = 10 + math.log2(K_eff / 128)
        By_sig = 8 + math.log2(K_eff / 128)

        # --- Nav uses K_eff (noise on combined bitline) ---
        Cmin = self.Cmax / r
        Cpar = K_eff * Cmin
        Ncap = (2**By_phys) / ((2**Sw_eff) * (2**self.Sx))
        Ctot = (K_eff * Cmin) + Cpar + (Ncap * self.Cmax)

        term1 = 36 * self.kT * Ctot
        term2 = ((2**(Sw_eff - 1) - 1)**2) * ((2**self.Sx - 1)**2)
        term3 = ((self.Cmax - Cmin)**2) * (self.Vin**2)

        Nav = max((term1 * term2) / term3, 1.0)
        mac_latency_ns = Lx * Nav * self.time_per_avg_ns

        # --- Ecap per group (K_eff cells summed on one bitline) ---
        Q_LSB = ((self.Cmax - Cmin) / (2**(Sw_eff - 1) - 1)) * (self.Vin / (2**self.Sx - 1))
        energy_signal = (Lx * Nav * Q_LSB * self.Vin * (2**By_sig)) / K_eff
        energy_wasted = Lx * Nav * Cmin * (self.Vin**2)
        Ecap_per_group_J = energy_signal + energy_wasted

        # --- Eadc per ADC conversion ---
        Eadc_per_conv_fJ = self.FOM_W * (2**By_sig)

        # --- Total energy for one MVM ---
        total_Ecap_fJ = Ecap_per_group_J * K_eff * 1e15 * num_adcs
        total_Eadc_fJ = Eadc_per_conv_fJ * num_adcs * Lx
        total_E_fJ = total_Ecap_fJ + total_Eadc_fJ

        # --- Per bit-op normalization ---
        total_bit_ops = K * num_pillars * Lx * Sw  # K cells per pillar, all pillars
        Ecap_fJ_bOP = total_Ecap_fJ / total_bit_ops
        Eadc_fJ_bOP = total_Eadc_fJ / total_bit_ops
        Etot_fJ_bOP = Ecap_fJ_bOP + Eadc_fJ_bOP

        # --- Efficiency ---
        pops_w_b = 1.0 / Etot_fJ_bOP
        mac_tops_w = (pops_w_b * 1000.0 / (Lx * Sw)) * 2.0

        # --- Speed ---
        throughput_tbops = total_bit_ops / (mac_latency_ns * 1e-9) / 1e12
        mac_tops = (throughput_tbops / (Lx * Sw)) * 2.0

        edp = Etot_fJ_bOP * mac_latency_ns
        total_energy_pJ = total_E_fJ / 1000.0

        # --- Area ---
        cell_array_area_mm2 = (N * M * self.cell_size_um2) / 1e6

        return {
            'K': K, 'K_eff': K * g, 'Cols(M)': M, 'Rows(N)': N,
            'ON/OFF': r, 'Sw': Sw, 'Lx': Lx,
            'g': g, 'Pillars': num_pillars, 'ADCs': num_adcs,
            'By_sig': round(By_sig, 1), 'Nav': round(Nav, 2),
            'Latency(ns)': round(mac_latency_ns, 1),
            'TbOPS': round(throughput_tbops, 3),
            'MAC TOPS': round(mac_tops, 3),
            'Total E(pJ)': round(total_energy_pJ, 2),
            'Ecap(fJ/bOP)': round(Ecap_fJ_bOP, 4),
            'Eadc(fJ/bOP)': round(Eadc_fJ_bOP, 4),
            'Etot(fJ/bOP)': round(Etot_fJ_bOP, 4),
            'POPS/W/b': round(pops_w_b, 2),
            'MAC TOPS/W': round(mac_tops_w, 1),
            'EDP': round(edp, 2),
            'Cell Area (mm^2)': round(cell_array_area_mm2, 4),
        }

    def run_design_space_exploration(self, tech, K_range, r_range, Sw_range, M_range, N_range, Lx_range, g_range):
        if not K_range: K_range = list(range(32, 513, 16))
        if not r_range: r_range = list(range(5, 101, 1))
        if not Sw_range: Sw_range = [1, 2, 3, 4, 5, 6]
        if not M_range: M_range = list(range(128, 8193, 128))
        if not N_range: N_range = list(range(128, 8193, 128))
        if not Lx_range: Lx_range = [4, 8, 16, 32]
        if not g_range: g_range = [1, 2, 4, 8, 16, 32, 64]

        valid_results = []
        total_iters = len(Sw_range) * len(K_range) * len(r_range) * len(g_range) * len(Lx_range)
        current_iter = 0
        start_time = time.time()

        for Sw in Sw_range:
            max_K_eff = self.get_max_feasible_K(Sw, tech)
            for K in K_range:
                for g in g_range:
                    K_eff = K * g
                    # Skip if combined column exceeds manufacturing limit
                    if K_eff > max_K_eff:
                        skipped = len(r_range) * len(Lx_range)
                        current_iter += skipped
                        continue
                    # Skip if K_eff < 128 (By formula needs K_eff >= 128)
                    if K_eff < 128:
                        skipped = len(r_range) * len(Lx_range)
                        current_iter += skipped
                        continue

                    for r in r_range:
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

                            # M and N applied post-sweep (Priority 2 logic)
                            for M in M_range:
                                for N in N_range:
                                    res = self.evaluate_configuration(K, r, Sw, M, N, Lx, g)
                                    valid_results.append(res)

        print()
        return pd.DataFrame(valid_results)

if __name__ == "__main__":
    analyzer = CIMP_Analyzer()
    technology = 'immersion'

    # Fixed array: sweep only K and g to see the trade-off
    allowed_Ks = []
    allowed_Sws = [4]
    allowed_rs = [100]
    allowed_Ms = [8192]
    allowed_Ns = [8192]
    allowed_Lxs = [4]
    allowed_gs = []

    print(f"--- Running 3D CIMP with ADC Grouping (Tech: {technology.upper()}) ---")
    df = analyzer.run_design_space_exploration(
        technology, allowed_Ks, allowed_rs, allowed_Sws,
        allowed_Ms, allowed_Ns, allowed_Lxs, allowed_gs
    )

    print(f"\nTotal feasible configurations found: {len(df)}")

    if len(df) > 0:
        display_cols = [
            'K', 'g', 'K_eff', 'ADCs', 'Cols(M)', 'Rows(N)', 'ON/OFF', 'Sw', 'Lx',
            'Latency(ns)', 'TbOPS', 'MAC TOPS', 'Total E(pJ)',
            'Ecap(fJ/bOP)', 'Eadc(fJ/bOP)', 'Etot(fJ/bOP)',
            'POPS/W/b', 'MAC TOPS/W', 'EDP', 'Cell Area (mm^2)'
        ]

        # Show all feasible K×g combinations sorted by Etot
        print("\n📊 ALL FEASIBLE CONFIGURATIONS (sorted by Etot)")
        df_sorted = df.sort_values(by=['Etot(fJ/bOP)', 'ADCs'], ascending=[True, True])
        print(df_sorted[display_cols].head(5).to_string(index=False, justify='center', col_space=9))

        # Best energy efficiency
        print("\n🏆 BEST ENERGY EFFICIENCY (Highest POPS/W/b)")
        df_eff = df.sort_values(by=['POPS/W/b', 'ADCs'], ascending=[False, True])
        print(df_eff[display_cols].head(5).to_string(index=False, justify='center', col_space=9))

        # Minimum ADCs while still feasible
        print("\n🏆 MINIMUM ADCs (fewest ADCs, then best Etot)")
        df_adc = df.sort_values(by=['ADCs', 'Etot(fJ/bOP)'], ascending=[True, True])
        print(df_adc[display_cols].head(5).to_string(index=False, justify='center', col_space=9))

        # Best EDP
        print("\n🏆 BEST EDP")
        df_edp = df.sort_values(by=['EDP', 'ADCs'], ascending=[True, True])
        print(df_edp[display_cols].head(5).to_string(index=False, justify='center', col_space=9))