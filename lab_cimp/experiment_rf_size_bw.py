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

# Sweep parameters (Adjusted to avoid 1-element crashes and instant skips)
size_multipliers = [4, 8, 16, 32, 64, 128]
bandwidths_1b = [16, 32, 64, 128, 256, 512, 1024]

rf_1b_base_size = 4
rf_2b_base_size = 16

# Load the base hardware config
with open(base_yaml, "r") as f:
    cimp_dict = yaml.safe_load(f)

# NOTE: We intentionally DO NOT modify SRAM or DRAM. 
# Their base values safely accommodate the array geometry without causing divisor crashes.

print("Starting Register File 2D Sweep (Size Multiplier vs. Bandwidth)...")

results = {}

for mult in size_multipliers:
    current_rf_1b_size = rf_1b_base_size * mult
    current_rf_2b_size = rf_2b_base_size * mult
    
    results[mult] = {'bws': [], 'latencies': [], 'energies': []}
    print(f"\nEvaluating RF Size Multiplier: {mult}x (rf_1B: {current_rf_1b_size}b, rf_2B: {current_rf_2b_size}b)")
    
    for bw_1b in bandwidths_1b:
        # Scale output bandwidth proportionally to avoid 1-element unroll crashes
        bw_2b = bw_1b * 2
        
        # Cap max bandwidths to prevent fetching blocks larger than the array dimensions
        safe_bw_1b = min(bw_1b, 1024)
        safe_bw_2b = min(bw_2b, 4096)

        # Skip physically impossible configurations (bus wider than capacity)
        if safe_bw_1b > current_rf_1b_size or safe_bw_2b > current_rf_2b_size:
            print(f"  BW_1B {bw_1b:4d}: SKIPPED (Bandwidth exceeds Memory Capacity)")
            continue

        temp_dict = copy.deepcopy(cimp_dict)
        
        # Update RF_1B (Inputs, 4-bit)
        temp_dict['memories']['rf_1B']['size'] = current_rf_1b_size
        for port in temp_dict['memories']['rf_1B']['ports']:
            port['bandwidth_min'] = 4   # Allows flexible tiling down to 1 element
            port['bandwidth_max'] = safe_bw_1b
            
        # Update RF_2B (Outputs, 16-bit)
        temp_dict['memories']['rf_2B']['size'] = current_rf_2b_size
        for port in temp_dict['memories']['rf_2B']['ports']:
            port['bandwidth_min'] = 16  # Allows flexible tiling down to 1 element
            port['bandwidth_max'] = safe_bw_2b

        # Write out to a temporary YAML
        temp_yaml = "lab_cimp/inputs/hardware/temp_cimp_3D.yaml"
        with open(temp_yaml, "w") as f:
            yaml.dump(temp_dict, f, default_flow_style=False)

        try:
            # Run ZigZag
            energy, latency, tclk, area, _ = get_hardware_performance_zigzag(
                workload=workload,
                accelerator=temp_yaml,
                mapping=mapping,
                opt="energy"
            )
            results[mult]['bws'].append(bw_1b)
            results[mult]['latencies'].append(latency)
            results[mult]['energies'].append(energy)
            print(f"  BW_1B {bw_1b:4d}: Latency={latency:.0f}, Energy={energy:.0f}")
            
        except Exception as e:
            print(f"  BW_1B {bw_1b:4d}: FAILED ({str(e).splitlines()[-1]})")

# Clean up temp file
if os.path.exists("lab_cimp/inputs/hardware/temp_cimp_3D.yaml"):
    os.remove("lab_cimp/inputs/hardware/temp_cimp_3D.yaml")

# --- Plotting ---
print("\nGenerating 2D Sweep Plots for Latency & Energy...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

has_data = False
for mult, data in results.items():
    if not data['bws']:
        continue
    has_data = True
    bws = data['bws']
    latencies = data['latencies']
    energies = data['energies']
    
    label_str = f"{mult}x (1B:{rf_1b_base_size*mult}b, 2B:{rf_2b_base_size*mult}b)"
    ax1.plot(bws, latencies, marker='^', linestyle='-', linewidth=2, markersize=6, label=label_str)
    ax2.plot(bws, energies, marker='o', linestyle='-', linewidth=2, markersize=6, label=label_str)

if has_data:
    # Latency Plot
    ax1.set_title('System Latency vs. RF_1B Bandwidth', fontsize=14)
    ax1.set_xlabel('RF_1B Bandwidth (bits/cycle)', fontsize=12)
    ax1.set_ylabel('System Latency (ns)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_xscale('log', base=2) 
    ax1.set_yscale('log')
    
    # Legend formatting
    num_lines = len([d for d in results.values() if d['bws']])
    ncol = 2 if num_lines > 5 else 1
    ax1.legend(title="RF Capacity Multiplier", fontsize=8, ncol=ncol)

    # Energy Plot
    ax2.set_title('System Energy vs. RF_1B Bandwidth', fontsize=14)
    ax2.set_xlabel('RF_1B Bandwidth (bits/cycle)', fontsize=12)
    ax2.set_ylabel('System Energy (pJ)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_xscale('log', base=2)
    ax2.legend(title="RF Capacity Multiplier", fontsize=8, ncol=ncol)

    plt.tight_layout()
    plot_path = "figures/rf_2d_sweep.png"
    plt.savefig(plot_path, dpi=300)
    print(f"Plot saved successfully to {plot_path}")
else:
    print("All configurations failed. No plot generated.")