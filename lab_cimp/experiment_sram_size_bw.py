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

sizes_kb = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
bandwidths = [64, 128, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304]

base_size_kb = 256
base_r_cost = 416.16
base_w_cost = 378.4
cost_multiplier = 1.4

with open(base_yaml, "r") as f:
    cimp_dict = yaml.safe_load(f)

print("Starting SRAM Size & Bandwidth 2D Experiment...")
print("-" * 75)
print(f"{'SRAM Size':<10} | {'Bandwidth':<12} | {'Latency (Cycles)':<16} | {'Energy (pJ)'}")
print("-" * 75)

results = {}

for size_kb in sizes_kb:
    results[size_kb] = {'bws': [], 'energies': [], 'latencies': []}
    
    doublings = math.log2(size_kb / base_size_kb)
    current_multiplier = cost_multiplier ** doublings
    
    current_size_bits = size_kb * 1024 * 8
    current_r_cost = base_r_cost * current_multiplier
    current_w_cost = base_w_cost * current_multiplier
    
    for bw in bandwidths:
        mod_dict = copy.deepcopy(cimp_dict)
        
        # 1. Modify the SRAM size and costs
        mod_dict["memories"]["sram_256KB"]["size"] = current_size_bits
        mod_dict["memories"]["sram_256KB"]["r_cost"] = current_r_cost
        mod_dict["memories"]["sram_256KB"]["w_cost"] = current_w_cost
        
        # 2. Modify BOTH the read and write ports to the new bandwidth
        mod_dict["memories"]["sram_256KB"]["ports"][0]["bandwidth_min"] = bw
        mod_dict["memories"]["sram_256KB"]["ports"][0]["bandwidth_max"] = bw
        mod_dict["memories"]["sram_256KB"]["ports"][1]["bandwidth_min"] = bw
        mod_dict["memories"]["sram_256KB"]["ports"][1]["bandwidth_max"] = bw
        
        temp_yaml = f"lab_cimp/inputs/hardware/temp_cimp_sram_{size_kb}KB_bw_{bw}.yaml"
        with open(temp_yaml, "w") as f:
            yaml.dump(mod_dict, f, sort_keys=False) 
            
        try:
            energy, latency, tclk, area, zigzag_results = get_hardware_performance_zigzag(
                accelerator=temp_yaml,
                workload=workload,
                mapping=mapping,
                temporal_mapping_search_engine="loma",
                opt="latency", 
                dump_folder=f"lab_cimp/outputs/exp_sram_{size_kb}KB_bw_{bw}",
                in_memory_compute=True,
            )
            
            cmes = [result[0] for result in zigzag_results[0][1]]
            best_cme = cmes[0]
            total_latency_cycles = best_cme.latency_total2 
            total_energy = best_cme.energy_total
            
            results[size_kb]['bws'].append(bw)
            results[size_kb]['energies'].append(total_energy)
            results[size_kb]['latencies'].append(total_latency_cycles)
            
            print(f"{size_kb} KB".ljust(10) + f" | {bw} bits".ljust(12) + f" | {total_latency_cycles:<16,.0f} | {total_energy:.2f}")
            
        except Exception as e:
            # Silently catch hardware constraints failure to keep 2D output clean
            pass 
            
        if os.path.exists(temp_yaml):
            os.remove(temp_yaml)

print("-" * 75)

# --- PLOT THE CURVES ---
if results:
    print("\nGenerating 2D Sweep Plots for Latency & Energy...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    has_data = False
    for size_kb, data in results.items():
        if not data['bws']:
            continue
        has_data = True
        bws = data['bws']
        latencies = data['latencies']
        energies = data['energies']
        
        ax1.plot(bws, latencies, marker='^', linestyle='-', linewidth=2, markersize=6, label=f"{size_kb} KB")
        ax2.plot(bws, energies, marker='o', linestyle='-', linewidth=2, markersize=6, label=f"{size_kb} KB")

    if has_data:
        ax1.set_title('System Latency vs. SRAM Bandwidth', fontsize=14)
        ax1.set_xlabel('SRAM Bandwidth (bits/cycle)', fontsize=12)
        ax1.set_ylabel('System Latency (Clock Cycles)', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.set_xscale('log', base=2) 
        
        num_lines = len([d for d in results.values() if d['bws']])
        ncol = 2 if num_lines > 10 else 1
        ax1.legend(title="SRAM Size", fontsize=8, ncol=ncol)

        ax2.set_title('System Energy vs. SRAM Bandwidth', fontsize=14)
        ax2.set_xlabel('SRAM Bandwidth (bits/cycle)', fontsize=12)
        ax2.set_ylabel('System Energy (pJ)', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_xscale('log', base=2)
        ax2.legend(title="SRAM Size", fontsize=8, ncol=ncol)

        plt.tight_layout()
        plot_path = "figures/sram_size_bw_2d_sweep.png"
        plt.savefig(plot_path)
        print(f" -> Success! Open '{plot_path}' to see your plots.")
    else:
        print("All configurations failed.")
else:
    print("All configurations failed.")
