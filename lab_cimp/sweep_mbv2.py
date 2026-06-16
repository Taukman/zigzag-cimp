import os
import sys
import re
import logging

sys.path.insert(0, os.getcwd())
from zigzag.api import get_hardware_performance_zigzag

logging.getLogger().setLevel(logging.ERROR)

def run_2d_sweep(size):
    hw_template_path = "lab_cimp/inputs/hardware/cimp_2D.yaml"
    # =====================================================================
    # WORKLOAD DEFINITION
    # Change this path to test different models!
    # For example, for MobileNetV2 use:
    workload = "zigzag/inputs/workload/mobilenetv2.onnx"
    # =====================================================================
    #workload = "zigzag/inputs/workload/resnet18.onnx"
    mapping = "lab_cimp/inputs/mapping/mapping.yaml"

    with open(hw_template_path, 'r') as f: hw_template = f.read()

    hw_str = re.sub(r'sizes:\s*\[\d+,\s*\d+\]', f'sizes: [{size}, {size}]', hw_template)

    temp_hw = f"lab_cimp/inputs/hardware/cimp_2D_sweep_mnv2.yaml"
    
    with open(temp_hw, 'w') as f: f.write(hw_str)
        
    try:
        energy, latency, tclk, area, res = get_hardware_performance_zigzag(
            accelerator=temp_hw, workload=workload, mapping=mapping,
            temporal_mapping_search_engine="loma", opt="latency",
            dump_folder=f"lab_cimp/outputs/sweep_mnv2_2D_{size}",
            pickle_filename=f"lab_cimp/outputs/sweep_mnv2_2D_{size}.pickle",
            in_memory_compute=True, loma_show_progress_bar=False,
        )
        
        total_mac_ops = 0
        total_energy_pj = 0
        total_latency_ns = 0
        
        for layer_res in res[0][1]:
            cme = layer_res[0]
            total_mac_ops += cme.layer.total_mac_count * 2
            total_energy_pj += cme.energy_total
            total_latency_ns += cme.system_delay_ns
            
        sys_tops = (total_mac_ops / total_latency_ns) / 1000 if total_latency_ns > 0 else 0
        sys_topsw = (total_mac_ops / total_energy_pj) if total_energy_pj > 0 else 0
        
        # Macro metrics are constant for the hardware, so we can just grab from the first layer
        imc_macro = res[0][1][0][0].accelerator.operational_array
        
        cell_area_mm2 = (size * size * imc_macro.cells_area) / 1e6
        
        tbops, pops, etot = imc_macro.get_macro_level_bit_ops_performance()
        Lx = imc_macro.activation_precision / imc_macro.bit_serial_precision
        Sw = imc_macro.weight_precision
        mac_tops = (tbops * 1000) / (Lx * Sw) * 2
        mac_topsw = (pops * 1000) / (Lx * Sw) * 2
        
        sys_tops_mm = sys_tops / cell_area_mm2 if cell_area_mm2 else 0
        mac_tops_mm = mac_tops / cell_area_mm2 if cell_area_mm2 else 0
    except Exception as e:
        print(f"Error in 2D: {e}")
        sys_tops = mac_tops = sys_topsw = mac_topsw = cell_area_mm2 = sys_tops_mm = mac_tops_mm = 0

    if os.path.exists(temp_hw): os.remove(temp_hw)
    return sys_tops, mac_tops, sys_topsw, mac_topsw, cell_area_mm2, sys_tops_mm, mac_tops_mm

def run_3d_sweep(d1, d2, d3):
    hw_template_path = "lab_cimp/inputs/hardware/cimp_3D.yaml"
    # =====================================================================
    # WORKLOAD DEFINITION
    # Change this path to test different models!
    # For example, for MobileNetV2 use:
    workload = "zigzag/inputs/workload/mobilenetv2.onnx"
    # =====================================================================
    #workload = "zigzag/inputs/workload/resnet18.onnx"
    mapping = "lab_cimp/inputs/mapping/mapping_3D.yaml"

    with open(hw_template_path, 'r') as f: hw_template = f.read()

    hw_str = re.sub(r'sizes:\s*\[\d+,\s*\d+,\s*\d+\]', f'sizes: [{d1}, {d2}, {d3}]', hw_template)
    hw_str = re.sub(r'cimp_adc_grouping:\s*\d+', f'cimp_adc_grouping: {d3}', hw_str)
    
    temp_hw = f"lab_cimp/inputs/hardware/cimp_3D_sweep_mnv2.yaml"
    
    with open(temp_hw, 'w') as f: f.write(hw_str)
        
    try:
        energy, latency, tclk, area, res = get_hardware_performance_zigzag(
            accelerator=temp_hw, workload=workload, mapping=mapping,
            temporal_mapping_search_engine="loma", opt="latency",
            dump_folder=f"lab_cimp/outputs/sweep_mnv2_3D_{d1}",
            pickle_filename=f"lab_cimp/outputs/sweep_mnv2_3D_{d1}.pickle",
            in_memory_compute=True, loma_show_progress_bar=False,
        )
        
        total_mac_ops = 0
        total_energy_pj = 0
        total_latency_ns = 0
        
        for layer_res in res[0][1]:
            cme = layer_res[0]
            total_mac_ops += cme.layer.total_mac_count * 2
            total_energy_pj += cme.energy_total
            total_latency_ns += cme.system_delay_ns
            
        sys_tops = (total_mac_ops / total_latency_ns) / 1000 if total_latency_ns > 0 else 0
        sys_topsw = (total_mac_ops / total_energy_pj) if total_energy_pj > 0 else 0
        
        # Macro metrics are constant for the hardware, so we can just grab from the first layer
        imc_macro = res[0][1][0][0].accelerator.operational_array
        
        cell_area_mm2 = (d1 * d3 * imc_macro.cells_area) / 1e6
        
        tbops, pops, etot = imc_macro.get_macro_level_bit_ops_performance()
        Lx = imc_macro.activation_precision / imc_macro.bit_serial_precision
        Sw = imc_macro.weight_precision
        mac_tops = (tbops * 1000) / (Lx * Sw) * 2
        mac_topsw = (pops * 1000) / (Lx * Sw) * 2
        
        sys_tops_mm = sys_tops / cell_area_mm2 if cell_area_mm2 else 0
        mac_tops_mm = mac_tops / cell_area_mm2 if cell_area_mm2 else 0
    except Exception as e:
        print(f"Error in 3D: {e}")
        sys_tops = mac_tops = sys_topsw = mac_topsw = cell_area_mm2 = sys_tops_mm = mac_tops_mm = 0

    if os.path.exists(temp_hw): os.remove(temp_hw)
    return sys_tops, mac_tops, sys_topsw, mac_topsw, cell_area_mm2, sys_tops_mm, mac_tops_mm

combinations = [
    (32, 32, 8, 4),
    (64, 64, 8, 8),
    (128, 128, 16, 8),
    (256, 256, 16, 16)
]

labels = []
results_2d = []
results_3d = []

for s2d, d1, d2, d3 in combinations:
    print(f"Running ResNet18 for {s2d}x{s2d} vs {d1}x{d2}x{d3}...")
    res_2d = run_2d_sweep(s2d)
    res_3d = run_3d_sweep(d1, d2, d3)
    
    labels.append(f"{s2d}x{s2d} ({d2}x{d3})")
    results_2d.append(res_2d)
    results_3d.append(res_3d)

print("\n=== MobileNetV2 Real Workload: 2D vs 3D Comparison Table ===")
print(f"| {'Size':<16} | {'Metric':<14} | {'2D Baseline':<12} | {'3D Model':<12} | {'Advantage':<10} |")
print("|------------------|----------------|--------------|--------------|------------|")

for i, label in enumerate(labels):
    s_tops2, m_tops2, s_topsw2, m_topsw2, area2, s_tops_mm2, m_tops_mm2 = results_2d[i]
    s_tops3, m_tops3, s_topsw3, m_topsw3, area3, s_tops_mm3, m_tops_mm3 = results_3d[i]
    
    print(f"| {label:<16} | {'Area (mm²)':<14} | {area2:<12.6f} | {area3:<12.6f} | {area2/area3 if area3 else 0:>9.2f}x |")
    print(f"| {'':<16} | {'Sys TOPS':<14} | {s_tops2:<12.4f} | {s_tops3:<12.4f} | {s_tops3/s_tops2 if s_tops2 else 0:>9.2f}x |")
    print(f"| {'':<16} | {'Mac TOPS':<14} | {m_tops2:<12.2f} | {m_tops3:<12.2f} | {m_tops3/m_tops2 if m_tops2 else 0:>9.2f}x |")
    print(f"| {'':<16} | {'Sys TOPS/W':<14} | {s_topsw2:<12.2f} | {s_topsw3:<12.2f} | {s_topsw3/s_topsw2 if s_topsw2 else 0:>9.2f}x |")
    print(f"| {'':<16} | {'Mac TOPS/W':<14} | {m_topsw2:<12.2f} | {m_topsw3:<12.2f} | {m_topsw3/m_topsw2 if m_topsw2 else 0:>9.2f}x |")
    print(f"| {'':<16} | {'Sys TOPS/mm²':<14} | {s_tops_mm2:<12.2f} | {s_tops_mm3:<12.2f} | {s_tops_mm3/s_tops_mm2 if s_tops_mm2 else 0:>9.2f}x |")
    print(f"| {'':<16} | {'Mac TOPS/mm²':<14} | {m_tops_mm2:<12.2f} | {m_tops_mm3:<12.2f} | {m_tops_mm3/m_tops_mm2 if m_tops_mm2 else 0:>9.2f}x |")
    print("|------------------|----------------|--------------|--------------|------------|")
