import os
import sys
import yaml
import copy
import math
import logging
import matplotlib.pyplot as plt 

# Ensure zigzag is in the path
sys.path.insert(0, os.getcwd())
from zigzag.api import get_hardware_performance_zigzag

# Suppress overly verbose ZigZag logging
logging.getLogger("zigzag").setLevel(logging.WARNING)

# Create figures directory
if not os.path.exists("figures"):
    os.makedirs("figures")

base_yaml = "lab_cimp/inputs/hardware/cimp.yaml"
workload = "lab_cimp/inputs/workload/full_utilization.yaml"
mapping = "lab_cimp/inputs/mapping/mapping.yaml"

# We will sweep DRAM sizes in Megabytes (MB)
sizes_mb = [1, 10, 100, 1000, 10000]
base_size_mb = 10000 # 10 GB is the baseline in your YAML
base_r_cost = 700.0
base_w_cost = 750.0

# Cost increases by 1.4x each time capacity doubles
cost_multiplier = 1.4 

with open(base_yaml, "r") as f:
    cimp_dict = yaml.safe_load(f)

print("Starting DRAM Capacity Experiment...")
print("-" * 65)
print(f"{'DRAM Size':<10} | {'r_cost':<10} | {'w_cost':<10} | {'System Energy (pJ)'}")
print("-" * 65)

results = {}

for size_mb in sizes_mb:
    # Calculate scaling factor based on doublings from the 10GB baseline
    doublings = math.log2(size_mb / base_size_mb)
    current_multiplier = cost_multiplier ** doublings
    
    # Convert MB to Bytes for the simulator
    current_size_bytes = size_mb * 1024 * 1024 
    current_r_cost = base_r_cost * current_multiplier
    current_w_cost = base_w_cost * current_multiplier
    
    # Deepcopy to safely modify the base architecture dictionary
    mod_dict = copy.deepcopy(cimp_dict)
    mod_dict["memories"]["dram"]["size"] = current_size_bytes
    mod_dict["memories"]["dram"]["r_cost"] = current_r_cost
    mod_dict["memories"]["dram"]["w_cost"] = current_w_cost
    
    # Save modified architecture to a temporary file
    temp_yaml = f"lab_cimp/inputs/hardware/temp_cimp_dram_{size_mb}MB.yaml"
    with open(temp_yaml, "w") as f:
        yaml.dump(mod_dict, f, sort_keys=False) 
        
    try:
        # Run the ZigZag simulator (optimized for energy)
        energy, latency, tclk, area, zigzag_results = get_hardware_performance_zigzag(
            accelerator=temp_yaml,
            workload=workload,
            mapping=mapping,
            temporal_mapping_search_engine="loma",
            opt="energy",
            dump_folder=f"lab_cimp/outputs/exp_dram_{size_mb}MB",
            in_memory_compute=True,
        )
        
        # Extract total system energy
        cmes = [result[0] for result in zigzag_results[0][1]]
        best_cme = cmes[0]
        total_energy = best_cme.energy_total
        
        results[size_mb] = total_energy
        print(f"{size_mb} MB".ljust(10) + f" | {current_r_cost:<10.2f} | {current_w_cost:<10.2f} | {total_energy:.2f}")
        
    except Exception as e:
        # Catch the hardware failure if DRAM is too small for the dataset
        print(f"{size_mb} MB".ljust(10) + f" | {current_r_cost:<10.2f} | {current_w_cost:<10.2f} | FAILED: DRAM too small!")
        
    # Clean up temp file
    if os.path.exists(temp_yaml):
        os.remove(temp_yaml)

print("-" * 65)

# --- PLOT THE DRAM LINE ---
if results:
    print("\nGenerating DRAM Energy Plot...")
    sizes = list(results.keys())
    energies = list(results.values())

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, energies, marker='s', linestyle='-', color='green', linewidth=2, markersize=8)
    plt.title('System Energy vs. DRAM Capacity', fontsize=14)
    plt.xlabel('DRAM Capacity (MB)', fontsize=12)
    plt.ylabel('Total System Energy (pJ)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Using a log scale for the X-axis because the sizes jump dramatically (1 -> 10 -> 100...)
    plt.xscale('log', base=10) 
    plt.xticks(sizes, [f"{s} MB" for s in sizes]) 

    plt.tight_layout()
    plot_path = "figures/dram_energy_line.png"
    plt.savefig(plot_path)
    print(f" -> Success! Open '{plot_path}' to see the curve.")
else:
    print("All configurations failed. Check workload size against DRAM capacities.")