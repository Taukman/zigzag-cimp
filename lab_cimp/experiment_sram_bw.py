import os
import sys
import yaml
import copy
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

# We will sweep SRAM Bandwidth (bits per cycle), expanding up to huge sizes due to 3D array (256*128*256)
bandwidths = [64, 128, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304]

# Fix SRAM at the Optimal 256 KB settings we found earlier!
fixed_size_bits = 256 * 1024 * 8
fixed_r_cost = 416.16
fixed_w_cost = 378.4

with open(base_yaml, "r") as f:
    cimp_dict = yaml.safe_load(f)

print("Starting SRAM Bandwidth 'Roofline' Experiment...")
print("-" * 65)
print(f"{'Bandwidth':<10} | {'SRAM Size':<10} | {'Latency (Cycles)':<16} | {'Energy (pJ)'}")
print("-" * 65)

results = {}

for bw in bandwidths:
    # Deepcopy to safely modify the base architecture dictionary
    mod_dict = copy.deepcopy(cimp_dict)
    
    # 1. Lock in the optimal size and costs
    mod_dict["memories"]["sram_256KB"]["size"] = fixed_size_bits
    mod_dict["memories"]["sram_256KB"]["r_cost"] = fixed_r_cost
    mod_dict["memories"]["sram_256KB"]["w_cost"] = fixed_w_cost
    
    # 2. Modify BOTH the read and write ports to the new bandwidth
    # (Assuming r_port_1 is index 0, and w_port_1 is index 1 in your YAML)
    mod_dict["memories"]["sram_256KB"]["ports"][0]["bandwidth_min"] = bw
    mod_dict["memories"]["sram_256KB"]["ports"][0]["bandwidth_max"] = bw
    mod_dict["memories"]["sram_256KB"]["ports"][1]["bandwidth_min"] = bw
    mod_dict["memories"]["sram_256KB"]["ports"][1]["bandwidth_max"] = bw
    
    # Save modified architecture to a temporary file
    temp_yaml = f"lab_cimp/inputs/hardware/temp_cimp_bw_{bw}.yaml"
    with open(temp_yaml, "w") as f:
        yaml.dump(mod_dict, f, sort_keys=False) # Keep hierarchy intact!
        
    try:
        # Run the ZigZag simulator (optimized for latency this time to see maximum speed!)
        energy, latency, tclk, area, zigzag_results = get_hardware_performance_zigzag(
            accelerator=temp_yaml,
            workload=workload,
            mapping=mapping,
            temporal_mapping_search_engine="loma",
            opt="latency", 
            dump_folder=f"lab_cimp/outputs/exp_sram_bw_{bw}",
            in_memory_compute=True,
        )
        
        # Extract total system latency and energy
        cmes = [result[0] for result in zigzag_results[0][1]]
        best_cme = cmes[0]
        total_latency_cycles = best_cme.latency_total2 # ZigZag's internal total cycle count
        total_energy = best_cme.energy_total
        
        results[bw] = (total_energy, total_latency_cycles)
        print(f"{bw} bits".ljust(10) + f" | 256 KB     | {total_latency_cycles:<16,.0f} | {total_energy:.2f}")
        
    except Exception as e:
        import traceback
        # Catch hardware mapping failures (e.g., bandwidth too low to feed physical loops)
        print(f"{bw} bits".ljust(10) + f" | 256 KB     | FAILED: {str(e)}")
        print(traceback.format_exc())
        
    # Clean up temp file
    if os.path.exists(temp_yaml):
        os.remove(temp_yaml)

print("-" * 65)

# --- PLOT THE ROOFLINE CURVE ---
if results:
    print("\nGenerating Bandwidth Roofline Plots for Latency & Energy...")
    bws = list(results.keys())
    energies = [val[0] for val in results.values()]
    latencies = [val[1] for val in results.values()]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Latency Plot
    ax1.plot(bws, latencies, marker='^', linestyle='-', color='purple', linewidth=2, markersize=8)
    ax1.set_title('System Latency vs. SRAM Bandwidth', fontsize=14)
    ax1.set_xlabel('SRAM Bandwidth (bits/cycle)', fontsize=12)
    ax1.set_ylabel('System Latency (Clock Cycles)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_xscale('log', base=2) 
    ax1.set_xticks(bws)
    ax1.set_xticklabels([f"{b}" for b in bws], rotation=45, ha='right')

    # Energy Plot
    ax2.plot(bws, energies, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    ax2.set_title('System Energy vs. SRAM Bandwidth', fontsize=14)
    ax2.set_xlabel('SRAM Bandwidth (bits/cycle)', fontsize=12)
    ax2.set_ylabel('System Energy (pJ)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_xscale('log', base=2)
    ax2.set_xticks(bws)
    ax2.set_xticklabels([f"{b}" for b in bws], rotation=45, ha='right')

    plt.tight_layout()
    plot_path = "figures/sram_bandwidth_roofline.png"
    plt.savefig(plot_path)
    print(f" -> Success! Open '{plot_path}' to see your bandwidth plots.")
else:
    print("All configurations failed.")