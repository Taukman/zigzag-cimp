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

base_yaml = "lab_cimp/inputs/hardware/cimp.yaml"
workload = "lab_cimp/inputs/workload/full_utilization.yaml"
mapping = "lab_cimp/inputs/mapping/mapping.yaml"

sizes_kb = [64, 128, 256, 512, 1024]
base_size_kb = 256
base_r_cost = 416.16
base_w_cost = 378.4
cost_multiplier = 1.4 

with open(base_yaml, "r") as f:
    cimp_dict = yaml.safe_load(f)

print("Starting SRAM 'Goldilocks' Zone Experiment...")
print("-" * 65)
print(f"{'SRAM Size':<10} | {'r_cost':<10} | {'w_cost':<10} | {'System Energy (pJ)'}")
print("-" * 65)

results = {}

for size_kb in sizes_kb:
    doublings = math.log2(size_kb / base_size_kb)
    current_multiplier = cost_multiplier ** doublings
    
    current_size_bytes = size_kb * 1024
    current_r_cost = base_r_cost * current_multiplier
    current_w_cost = base_w_cost * current_multiplier
    
    mod_dict = copy.deepcopy(cimp_dict)
    mod_dict["memories"]["sram_256KB"]["size"] = current_size_bytes
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
        
        if size_kb == 256:
            bar_plot_cost_model_evaluations_breakdown([best_cme], save_path="figures/sram_256kb_breakdown.png")
        
        results[size_kb] = total_energy
        print(f"{size_kb} KB".ljust(10) + f" | {current_r_cost:<10.2f} | {current_w_cost:<10.2f} | {total_energy:.2f}")
        
    except Exception as e:
        # Catch the hardware failure and keep going!
        print(f"{size_kb} KB".ljust(10) + f" | {current_r_cost:<10.2f} | {current_w_cost:<10.2f} | FAILED: SRAM too small!")
        
    if os.path.exists(temp_yaml):
        os.remove(temp_yaml)

print("-" * 65)
if results:
    best_size = min(results, key=results.get)
    print(f"Optimal SRAM Size (Bottom of U-Curve): {best_size} KB")
    print(f"Minimum System Energy: {results[best_size]:.2f} pJ")

    print("\nGenerating U-Curve Plot...")
    sizes = list(results.keys())
    energies = list(results.values())

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, energies, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    plt.title('System Energy vs. SRAM Capacity (The U-Curve)', fontsize=14)
    plt.xlabel('SRAM Capacity (KB)', fontsize=12)
    plt.ylabel('Total System Energy (pJ)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(sizes) 

    optimal_index = sizes.index(best_size)
    plt.plot(sizes[optimal_index], energies[optimal_index], marker='o', color='red', markersize=10, label='Optimal Size')
    plt.legend()

    plt.tight_layout()
    plot_path = "figures/sram_u_curve.png"
    plt.savefig(plot_path)
    print(f" -> Success! Open '{plot_path}' to see your U-Curve.")
else:
    print("All configurations failed. Check workload size against SRAM capacities.")