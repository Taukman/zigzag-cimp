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

base_yaml = "lab_cimp/inputs/hardware/cimp_3D.yaml"
workload = "lab_cimp/inputs/workload/full_utilization_3d.yaml"
mapping = "lab_cimp/inputs/mapping/mapping_3D.yaml"

# We will sweep DRAM sizes in Megabytes (MB)
sizes_mb = [1, 10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
base_size_mb = 10000 # 10 GB is the baseline in your YAML
base_r_cost = 700.0
base_w_cost = 750.0

# Cost increases by 1.4x each time capacity doubles
cost_multiplier = 1.4 

with open(base_yaml, "r") as f:
    cimp_dict = yaml.safe_load(f)

print("Starting DRAM Capacity Experiment...")
print("-" * 65)
print(f"{'DRAM Size':<10} | {'r_cost':<10} | {'w_cost':<10} | {'Energy (pJ)':<15} | {'Latency (Cycles)'}")
print("-" * 65)

results = {}

for size_mb in sizes_mb:
    # Calculate scaling factor based on doublings from the 10GB baseline
    doublings = math.log2(size_mb / base_size_mb)
    current_multiplier = cost_multiplier ** doublings
    
    # Convert MB to Bits for the simulator (ZigZag uses bits)
    current_size_bits = size_mb * 1024 * 1024 * 8
    current_r_cost = base_r_cost * current_multiplier
    current_w_cost = base_w_cost * current_multiplier
    
    # Deepcopy to safely modify the base architecture dictionary
    mod_dict = copy.deepcopy(cimp_dict)
    mod_dict["memories"]["dram"]["size"] = current_size_bits
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
        
        # Extract total system energy and latency
        cmes = [result[0] for result in zigzag_results[0][1]]
        best_cme = cmes[0]
        total_energy = best_cme.energy_total
        total_latency = best_cme.latency_total2
        
        results[size_mb] = (total_energy, total_latency)
        print(f"{size_mb} MB".ljust(10) + f" | {current_r_cost:<10.2f} | {current_w_cost:<10.2f} | {total_energy:<15.2f} | {total_latency:,.0f}")
        
    except Exception as e:
        # Catch the hardware failure if DRAM is too small for the dataset
        import traceback
        print(f"{size_mb} MB".ljust(10) + f" | {current_r_cost:<10.2f} | {current_w_cost:<10.2f} | FAILED: {str(e)}")
        print(traceback.format_exc())
        
    # Clean up temp file
    if os.path.exists(temp_yaml):
        os.remove(temp_yaml)

print("-" * 65)

# --- PLOT THE DRAM LINE ---
if results:
    print("\nGenerating DRAM Latency & Energy Plots...")
    sizes = list(results.keys())
    energies = [val[0] for val in results.values()]
    latencies = [val[1] for val in results.values()]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Energy Plot
    ax1.plot(sizes, energies, marker='s', linestyle='-', color='green', linewidth=2, markersize=8)
    ax1.set_title('System Energy vs. DRAM Capacity', fontsize=14)
    ax1.set_xlabel('DRAM Capacity (MB)', fontsize=12)
    ax1.set_ylabel('Total System Energy (pJ)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_xscale('log', base=10) 
    # Removed forced xticks to allow clean, default log scaling

    # Latency Plot
    ax2.plot(sizes, latencies, marker='^', linestyle='-', color='purple', linewidth=2, markersize=8)
    ax2.set_title('System Latency vs. DRAM Capacity', fontsize=14)
    ax2.set_xlabel('DRAM Capacity (MB)', fontsize=12)
    ax2.set_ylabel('Total System Latency (Cycles)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_xscale('log', base=10)
    # Removed forced xticks to allow clean, default log scaling

    plt.tight_layout()
    plot_path = "figures/dram_size_plots.png"
    plt.savefig(plot_path)
    print(f" -> Success! Open '{plot_path}' to see the plots.")
else:
    print("All configurations failed. Check workload size against DRAM capacities.")