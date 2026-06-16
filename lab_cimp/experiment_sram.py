import os
import sys
import yaml
import copy
import math
import logging
import matplotlib.pyplot as plt 

sys.path.insert(0, os.getcwd())
from zigzag.api import get_hardware_performance_zigzag

logging.getLogger("zigzag").setLevel(logging.WARNING)

from zigzag.visualization.results.plot_cme import bar_plot_cost_model_evaluations_breakdown

if not os.path.exists("figures"):
    os.makedirs("figures")

base_yaml = "lab_cimp/inputs/hardware/cimp_3D.yaml"
workload = "lab_cimp/inputs/workload/full_utilization_3d.yaml"
mapping = "lab_cimp/inputs/mapping/mapping_3D.yaml"

sizes_kb = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
base_size_kb = 256
base_r_cost = 416.16
base_w_cost = 378.4
cost_multiplier = 1.4 

with open(base_yaml, "r") as f:
    cimp_dict = yaml.safe_load(f)

print("Starting SRAM 'Goldilocks' Zone Experiment...")
print("-" * 65)
print(f"{'SRAM Size':<10} | {'r_cost':<10} | {'w_cost':<10} | {'Energy (pJ)':<15} | {'Latency (Cycles)'}")
print("-" * 65)

results = {}

for size_kb in sizes_kb:
    doublings = math.log2(size_kb / base_size_kb)
    current_multiplier = cost_multiplier ** doublings
    
    current_size_bits = size_kb * 1024 * 8
    current_r_cost = base_r_cost * current_multiplier
    current_w_cost = base_w_cost * current_multiplier
    
    mod_dict = copy.deepcopy(cimp_dict)
    mod_dict["memories"]["sram_256KB"]["size"] = current_size_bits
    mod_dict["memories"]["sram_256KB"]["r_cost"] = current_r_cost
    mod_dict["memories"]["sram_256KB"]["w_cost"] = current_w_cost
    
    temp_yaml = f"lab_cimp/inputs/hardware/temp_cimp_{size_kb}KB.yaml"
    with open(temp_yaml, "w") as f:
        yaml.dump(mod_dict, f, sort_keys=False) 
        
    try:
        # Run the ZigZag simulator
        energy, latency, tclk, area, zigzag_results = get_hardware_performance_zigzag(
            accelerator=temp_yaml,
            workload=workload,
            mapping=mapping,
            temporal_mapping_search_engine="loma",
            opt="energy",
            dump_folder=f"lab_cimp/outputs/exp_sram_{size_kb}KB",
            in_memory_compute=True,
        )
        
        cmes = [result[0] for result in zigzag_results[0][1]]
        best_cme = cmes[0]
        total_energy = best_cme.energy_total
        total_latency = best_cme.latency_total2
        
        if size_kb == 256:
            bar_plot_cost_model_evaluations_breakdown([best_cme], save_path="figures/sram_256kb_breakdown.png")
        
        results[size_kb] = (total_energy, total_latency)
        print(f"{size_kb} KB".ljust(10) + f" | {current_r_cost:<10.2f} | {current_w_cost:<10.2f} | {total_energy:<15.2f} | {total_latency:,.0f}")
        
    except Exception as e:
        import traceback
        # Catch the hardware failure and keep going!
        print(f"{size_kb} KB".ljust(10) + f" | {current_r_cost:<10.2f} | {current_w_cost:<10.2f} | FAILED: {str(e)}")
        print(traceback.format_exc())

        
    if os.path.exists(temp_yaml):
        os.remove(temp_yaml)

print("-" * 65)
# --- PLOT THE SYSTEM LATENCY & ENERGY ---
if results:
    best_size = min(results.keys(), key=lambda k: results[k][0])
    print(f"Optimal SRAM Size (Bottom of U-Curve for Energy): {best_size} KB")
    print(f"Minimum System Energy: {results[best_size][0]:.2f} pJ")

    print("\nGenerating System Latency & Energy Plots...")
    sizes = list(results.keys())
    energies = [val[0] for val in results.values()]
    latencies = [val[1] for val in results.values()]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Energy Plot
    ax1.plot(sizes, energies, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    ax1.set_title('System Energy vs. SRAM Capacity', fontsize=14)
    ax1.set_xlabel('SRAM Capacity (KB)', fontsize=12)
    ax1.set_ylabel('Total System Energy (pJ)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Fix: Log base 2 scale spaces powers of 2 evenly; rotation prevents text overlap
    ax1.set_xscale('log', base=2)
    ax1.set_xticks(sizes)
    ax1.set_xticklabels([f"{s}" for s in sizes], rotation=45, ha='right') 
    
    optimal_index = sizes.index(best_size)
    ax1.plot(sizes[optimal_index], energies[optimal_index], marker='o', color='red', markersize=10, label='Min Energy')
    ax1.legend()

    # Latency Plot
    ax2.plot(sizes, latencies, marker='^', linestyle='-', color='purple', linewidth=2, markersize=8)
    ax2.set_title('System Latency vs. SRAM Capacity', fontsize=14)
    ax2.set_xlabel('SRAM Capacity (KB)', fontsize=12)
    ax2.set_ylabel('Total System Latency (Cycles)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Fix: Log base 2 scale spaces powers of 2 evenly; rotation prevents text overlap
    ax2.set_xscale('log', base=2)
    ax2.set_xticks(sizes)
    ax2.set_xticklabels([f"{s}" for s in sizes], rotation=45, ha='right')

    plt.tight_layout()
    plot_path = "figures/sram_u_curve.png"
    plt.savefig(plot_path)
    print(f" -> Success! Open '{plot_path}' to see your U-Curve.")
else:
    print("All configurations failed. Check workload size against SRAM capacities.")