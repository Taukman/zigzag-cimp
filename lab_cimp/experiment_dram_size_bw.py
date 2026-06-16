import os
import sys
import yaml
import copy
import logging
import math
import matplotlib.pyplot as plt

# Ensure zigzag is in the path
sys.path.insert(0, os.getcwd())
from zigzag.api import get_hardware_performance_zigzag

# Suppress overly verbose ZigZag logging
logging.getLogger("zigzag").setLevel(logging.WARNING)

# Create figures directory
if not os.path.exists("figures"):
    os.makedirs("figures")

base_yaml = "lab_cimp/inputs/hardware/cimp_3D.yaml"
workload = "lab_cimp/inputs/workload/full_utilization_3d.yaml"
mapping = "lab_cimp/inputs/mapping/mapping_3D.yaml"

sizes_mb = [1, 10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
bandwidths = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]

base_size_mb = 10000
base_r_cost = 700.0
base_w_cost = 750.0
cost_multiplier = 1.4

with open(base_yaml, "r") as f:
    cimp_dict = yaml.safe_load(f)

print("Starting DRAM Size & Bandwidth 2D Experiment...")
print("-" * 75)
print(f"{'DRAM Size':<10} | {'DRAM BW':<12} | {'Latency (Cycles)':<16} | {'Energy (pJ)'}")
print("-" * 75)

results = {}

for size_mb in sizes_mb:
    results[size_mb] = {'bws': [], 'energies': [], 'latencies': []}
    
    doublings = math.log2(size_mb / base_size_mb)
    current_multiplier = cost_multiplier ** doublings
    
    current_size_bits = size_mb * 1024 * 1024 * 8
    current_r_cost = base_r_cost * current_multiplier
    current_w_cost = base_w_cost * current_multiplier
    
    for bw in bandwidths:
        mod_dict = copy.deepcopy(cimp_dict)
        
        # 1. Modify the DRAM size and costs
        mod_dict["memories"]["dram"]["size"] = current_size_bits
        mod_dict["memories"]["dram"]["r_cost"] = current_r_cost
        mod_dict["memories"]["dram"]["w_cost"] = current_w_cost
        
        # 2. Modify the DRAM port bandwidth
        mod_dict["memories"]["dram"]["ports"][0]["bandwidth_min"] = bw
        mod_dict["memories"]["dram"]["ports"][0]["bandwidth_max"] = bw
        
        temp_yaml = f"lab_cimp/inputs/hardware/temp_cimp_dramsize_{size_mb}MB_bw_{bw}.yaml"
        with open(temp_yaml, "w") as f:
            yaml.dump(mod_dict, f, sort_keys=False) 
            
        try:
            energy, latency, tclk, area, zigzag_results = get_hardware_performance_zigzag(
                accelerator=temp_yaml,
                workload=workload,
                mapping=mapping,
                temporal_mapping_search_engine="loma",
                opt="latency", 
                dump_folder=f"lab_cimp/outputs/exp_dramsize_{size_mb}MB_bw_{bw}",
                in_memory_compute=True,
            )
            
            cmes = [result[0] for result in zigzag_results[0][1]]
            best_cme = cmes[0]
            total_latency_cycles = best_cme.latency_total2 
            total_energy = best_cme.energy_total
            
            results[size_mb]['bws'].append(bw)
            results[size_mb]['energies'].append(total_energy)
            results[size_mb]['latencies'].append(total_latency_cycles)
            
            print(f"{size_mb} MB".ljust(10) + f" | {bw} bits".ljust(12) + f" | {total_latency_cycles:<16,.0f} | {total_energy:.2f}")
            
        except Exception as e:
            # Silently catch hardware failures to keep the 2D output clean
            pass 
            
        if os.path.exists(temp_yaml):
            os.remove(temp_yaml)

print("-" * 75)

# --- PLOT THE CURVES ---
if results:
    print("\nGenerating 2D Sweep Plots for Latency & Energy...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    has_data = False
    for size_mb, data in results.items():
        if not data['bws']:
            continue
        has_data = True
        bws = data['bws']
        latencies = data['latencies']
        energies = data['energies']
        
        ax1.plot(bws, latencies, marker='^', linestyle='-', linewidth=2, markersize=6, label=f"{size_mb} MB")
        ax2.plot(bws, energies, marker='o', linestyle='-', linewidth=2, markersize=6, label=f"{size_mb} MB")

    if has_data:
        ax1.set_title('System Latency vs. DRAM Bandwidth', fontsize=14)
        ax1.set_xlabel('DRAM Bandwidth (bits/cycle)', fontsize=12)
        ax1.set_ylabel('System Latency (Clock Cycles)', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.set_xscale('log', base=2) 
        
        # Determine number of lines for legend formatting
        num_lines = len([d for d in results.values() if d['bws']])
        ncol = 2 if num_lines > 10 else 1
        ax1.legend(title="DRAM Size", fontsize=8, ncol=ncol)

        ax2.set_title('System Energy vs. DRAM Bandwidth', fontsize=14)
        ax2.set_xlabel('DRAM Bandwidth (bits/cycle)', fontsize=12)
        ax2.set_ylabel('System Energy (pJ)', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_xscale('log', base=2)
        ax2.legend(title="DRAM Size", fontsize=8, ncol=ncol)

        plt.tight_layout()
        plot_path = "figures/dram_size_bw_2d_sweep.png"
        plt.savefig(plot_path)
        print(f" -> Success! Open '{plot_path}' to see your plots.")
    else:
        print("All configurations failed.")
else:
    print("All configurations failed.")
