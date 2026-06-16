import math
import sys
import time
import datetime
import numpy as np
import pandas as pd

class CIMP_Analyzer:
    def __init__(self):
        # =====================================================================
        # [CIMP PHYSICS] CORE DEVICE CONSTANTS
        # These represent the base physical properties of the memcapacitors.
        # ZigZag does not simulate at this low level; it expects us to do this 
        # math first and feed it the final System-Level Energy and Latency.
        # =====================================================================
        self.Cmax = 1e-15       # Maximum capacitance (1 fF)
        self.Vin = 0.4          # Read voltage (400 mV)
        
        # [ZIGZAG LINK] self.Sx is equivalent to "bit_serial_precision" in your YAML.
        # The default here is 1 (processing 1 bit per cycle). Your YAML had it set to 2.
        self.Sx = 1             
        
        self.T = 330            # Temperature (330 Kelvin)
        self.kT = 1.380649e-23 * self.T # Thermal energy (Boltzmann constant)
        
        # Time to charge/discharge the crossbar once. 
        # [ZIGZAG LINK] This multiplied by Nav determines the clock frequency/latency of the Multiplier array.
        self.time_per_avg_ns = 40.0 
        
        # Baseline ADC Energy (Walden FOM). 
        # [ZIGZAG LINK] Related to your YAML "adc_resolution: 3". 
        self.adc_baseline_fJ = 0.25 
        
        # [CIMP PHYSICS] Lithography constraints from Figure 7 of the paper.
        self.tech_limits_pct = {
            'duv': 0.71,
            'immersion': 0.11,
            'sonos': 0.062,
            'ideal': 0.0001
        }

    def get_max_feasible_K(self, Sw, tech='immersion'):
        """
        [CIMP PHYSICS] Calculates the maximum possible Rows (K) before manufacturing variation ruins the chip.
        [ZIGZAG LINK] This effectively puts a physical maximum limit on your 'D1' dimension size in accelerator.yaml.
        """
        limit_pct = self.tech_limits_pct.get(tech.lower(), self.tech_limits_pct['immersion'])
        Sw_eff = max(Sw, 2) # Non-differential rule: Sw=1 acts like Sw=2
        
        # Formula derived from Eq. 32 in the paper
        K_max = (100.0 / (limit_pct * 6.0 * (2**(Sw_eff - 1) - 1)))**2
        return K_max

    def evaluate_configuration(self, K, r, Sw, M, Lx):
        """
        Calculates the physics of a specific array configuration.
        """
        Sw_eff = max(Sw, 2) 
        
        # =====================================================================
        # [ZIGZAG LINK] ADC RESOLUTION
        # In the paper, ADC bits (By) scale dynamically based on K (log2(K/128)).
        # In your accelerator.yaml, you explicitly hardcoded "adc_resolution: 3".
        # If you wanted to force this code to perfectly match your YAML, you 
        # would replace these lines with: By_phys = 5 and By_sig = 3.
        # =====================================================================
        By_phys = 10 + math.log2(K / 128) # Used for thermal noise physical limits
        By_sig = 8 + math.log2(K / 128)   # Used for active signal charge movement
        
        # =====================================================================
        # [CIMP PHYSICS] CAPACITANCE CALCULATIONS
        # [ZIGZAG LINK] This is the hardware penalty for making your "D1" dimension too large.
        # K directly scales the parasitic capacitance (Cpar).
        # =====================================================================
        Cmin = self.Cmax / r
        Cpar = K * Cmin
        Ncap = (2**By_phys) / ((2**Sw_eff) * (2**self.Sx))
        Ctot = (K * Cmin) + Cpar + (Ncap * self.Cmax)
        
        # =====================================================================
        # [CIMP PHYSICS] EQUATION 42: NAV (Number of Averages)
        # Calculates how many times the array must be read to overcome thermal noise.
        # =====================================================================
        term1 = 36 * self.kT * Ctot
        term2 = ((2**(Sw_eff - 1) - 1)**2) * ((2**self.Sx - 1)**2)
        term3 = ((self.Cmax - Cmin)**2) * (self.Vin**2)
        Nav = max((term1 * term2) / term3, 1.0) # Hardware minimum is 1 read
        
        # [ZIGZAG LINK] Latency calculation. In ZigZag, this determines the 'latency' 
        # property of the MAC operation or the clock cycle frequency.
        mac_latency_ns = Lx * Nav * self.time_per_avg_ns
        
        # =====================================================================
        # [CIMP PHYSICS] EQUATION 43: ENERGY (Ecap)
        # Calculates the raw electrical energy burned by moving charge.
        # =====================================================================
        Q_LSB = ((self.Cmax - Cmin) / (2**(Sw_eff - 1) - 1)) * (self.Vin / (2**self.Sx - 1))
        energy_signal = (Lx * Nav * Q_LSB * self.Vin * (2**By_sig)) / K
        energy_wasted = Lx * Nav * Cmin * (self.Vin**2)
        
        # Total Joules for a complete MAC operation
        Ecap_MAC_J = energy_signal + energy_wasted
        
        # =====================================================================
        # CONVERSION TO ZIGZAG MULTIPLIER NODE ENERGY
        # ZigZag needs total operation energy to do system-level analysis.
        # =====================================================================
        # Intensive property (fJ per bit-operation) - mostly for plotting
        Ecap_fJ_bOP = (Ecap_MAC_J * 1e15) / (Lx * Sw)
        Eadc_fJ_bOP = self.adc_baseline_fJ * (4.0 / Sw) 
        Etot_fJ_bOP = Ecap_fJ_bOP + Eadc_fJ_bOP
        
        # Metrics for the dataframe
        pops_w_b = 1.0 / Etot_fJ_bOP
        edp = Etot_fJ_bOP * mac_latency_ns
        
        # Extensive properties (Scaling with array dimensions)
        # [ZIGZAG LINK] Total bit operations considers both K (D1) and M (D2).
        total_bit_ops = K * M * Lx * Sw
        
        # [ZIGZAG LINK] This 'total_energy_pJ' divided by the number of MACs is exactly 
        # what you plug into the "energy_cost" of your ZigZag Multiplier array!
        total_energy_pJ = (Etot_fJ_bOP * total_bit_ops) / 1000.0
        
        # Throughput (TOPS)
        throughput_tops = total_bit_ops / (mac_latency_ns * 1e-9) / 1e12
        
        return {
            'K': K, 'Cols(M)': M, 'ON/OFF': r, 'Sw': Sw, 'Lx': Lx,
            'Latency(ns)': round(mac_latency_ns, 1),
            'T-put(TOPS)': round(throughput_tops, 3),
            'Total E(pJ)': round(total_energy_pJ, 2),
            'Etot(fJ/bOP)': round(Etot_fJ_bOP, 3),
            'POPS/W/b': round(pops_w_b, 1),
            'EDP': round(edp, 2)
        }

    def run_design_space_exploration(self, tech, K_range, r_range, Sw_range, M_range, Lx_range):
        """
        Sweeps through the search space to find the best hardware configurations to give to ZigZag.
        """
        # --- SMART INPUT PARSING ---
        # If the user provides empty arrays [], fill them with the full exploration ranges.
        # Step sizes (e.g., 128) are used to prevent Python out-of-memory RAM crashes.
        # [ZIGZAG LINK] K_range maps to D1 sizes. M_range maps to D2 sizes.
        if not K_range: K_range = list(range(128, 8193, 128)) 
        if not r_range: r_range = list(range(5, 101, 5)) 
        if not Sw_range: Sw_range = [1, 2, 3, 4, 5, 6] 
        if not M_range: M_range = list(range(128, 8193, 128)) 
        
        # [ZIGZAG LINK] Lx is derived from input_precision (e.g., 8) / bit_serial_precision (e.g., 2)
        if not Lx_range: Lx_range = [4, 8, 16, 32] 
        # ---------------------------

        valid_results = []
        total_iters = len(Sw_range) * len(K_range) * len(r_range) * len(M_range) * len(Lx_range)
        current_iter = 0
        
        start_time = time.time()

        for Sw in Sw_range:
            max_K = self.get_max_feasible_K(Sw, tech)
            for K in K_range:
                # ⚡ MASSIVE SPEED OPTIMIZATION
                # If D1 (K) is too large for the lithography (tech limit), skip the entire branch.
                if K > max_K:
                    skipped = len(r_range) * len(M_range) * len(Lx_range)
                    current_iter += skipped
                    continue 

                for r in r_range:
                    for M in M_range:
                        for Lx in Lx_range:
                            current_iter += 1
                            
                            # Draw loading bar & ETA every 100k loops
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

# ==========================================
# Run the Analyzer
# ==========================================
if __name__ == "__main__":
    analyzer = CIMP_Analyzer()
    technology = 'immersion'
    
    # Empty lists trigger the massive automated space search
    allowed_Ks = []
    allowed_Sws = []
    allowed_rs = []
    allowed_Ms = []
    allowed_Lxs = [] 
    
    print(f"--- Running Massive Hardware Search (Tech: {technology.upper()}) ---")
    df = analyzer.run_design_space_exploration(technology, allowed_Ks, allowed_rs, allowed_Sws, allowed_Ms, allowed_Lxs)
    
    print(f"\nTotal feasible configurations found: {len(df)}")
    
    # -------------------------------------------------------------------------
    # PRINTING THE WINNERS
    # Once you pick a winner from these lists, you take its dimensions (K, M)
    # and its Energy per MAC, and plug them directly into your ZigZag YAML!
    # -------------------------------------------------------------------------
    if len(df) > 0:
        # ---------------------------------------------------------
        # 1. PURE ENERGY EFFICIENCY
        # Hierarchy: POPS/W/b (High) -> Etot (Low) -> EDP (Low) -> TOPS (High) -> Total E (Low)
        # ---------------------------------------------------------
        print("\n🏆 BEST FOR PURE ENERGY EFFICIENCY (Highest POPS/W/b)")
        eff_cols = ['POPS/W/b', 'Etot(fJ/bOP)', 'EDP', 'T-put(TOPS)', 'Total E(pJ)']
        eff_asc  = [False,      True,           True,  False,         True]
        df_eff = df.sort_values(by=eff_cols, ascending=eff_asc)
        print(df_eff.head(10).to_string(index=False, justify='center', col_space=11))
        
        # ---------------------------------------------------------
        # 2. PURE SPEED (Lowest Latency)
        # Hierarchy: Latency (Low) -> EDP (Low) -> TOPS (High) -> POPS/W/b (High) -> Total E (Low)
        # ---------------------------------------------------------
        print("\n🏆 BEST FOR PURE SPEED (Lowest Latency)")
        spd_cols = ['Latency(ns)', 'EDP', 'T-put(TOPS)', 'POPS/W/b', 'Total E(pJ)']
        spd_asc  = [True,          True,  False,         False,      True]
        df_spd = df.sort_values(by=spd_cols, ascending=spd_asc)
        print(df_spd.head(10).to_string(index=False, justify='center', col_space=11))
        
        # ---------------------------------------------------------
        # 3. OVERALL BALANCE (Lowest EDP)
        # Hierarchy: EDP (Low) -> POPS/W/b (High) -> TOPS (High) -> Latency (Low) -> Total E (Low)
        # ---------------------------------------------------------
        print("\n🏆 BEST OVERALL BALANCE (Lowest EDP)")
        edp_cols = ['EDP', 'POPS/W/b', 'T-put(TOPS)', 'Latency(ns)', 'Total E(pJ)']
        edp_asc  = [True,  False,      False,         True,          True]
        df_edp = df.sort_values(by=edp_cols, ascending=edp_asc)
        print(df_edp.head(10).to_string(index=False, justify='center', col_space=11))
        
        # ---------------------------------------------------------
        # 4. MASSIVE THROUGHPUT (Highest TOPS)
        # Hierarchy: TOPS (High) -> POPS/W/b (High) -> EDP (Low) -> Latency (Low) -> Total E (Low)
        # ---------------------------------------------------------
        print("\n🏆 BEST FOR MASSIVE THROUGHPUT (Highest TOPS)")
        top_cols = ['T-put(TOPS)', 'POPS/W/b', 'EDP', 'Latency(ns)', 'Total E(pJ)']
        top_asc  = [False,         False,      True,  True,          True]
        df_top = df.sort_values(by=top_cols, ascending=top_asc)
        print(df_top.head(10).to_string(index=False, justify='center', col_space=11))