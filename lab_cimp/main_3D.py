import logging as _logging
import os
import sys

sys.path.insert(0, os.getcwd())
from zigzag.api import get_hardware_performance_zigzag
from zigzag.visualization.results.plot_cme import (
    bar_plot_cost_model_evaluations_breakdown,
)
from zigzag.visualization.results.print_mapping import print_mapping

# Initialize the logger
_logging_level = _logging.INFO
_logging_format = "%(asctime)s - %(funcName)s +%(lineno)s - %(levelname)s - %(message)s"
_logging.basicConfig(level=_logging_level, format=_logging_format)
logger = _logging.getLogger(__name__)

# --- WORKLOAD TOGGLE: uncomment ONE of the two lines below ---
workload_name = "full_utilization_3d"            # <-- YAML manual 3D workload
#workload_name = "resnet18_first_layer"            # <-- ONNX ResNet-18 layer 1
# --- END WORKLOAD TOGGLE ---
hw_name = "accelerator1_3D"
experiment_id = f"{hw_name}-{workload_name}"
pickle_name = f"{experiment_id}-saved_list_of_cmes"

accelerator = "lab_cimp/inputs/hardware/cimp_3D.yaml"

# --- WORKLOAD PATH TOGGLE: uncomment ONE of the two lines below ---
#workload = "lab_cimp/inputs/workload/full_utilization_3d.yaml"    # <-- YAML manual 3D workload
workload = "lab_cimp/inputs/workload/resnet18_first_layer.onnx"  # <-- ONNX ResNet-18 layer 1
# --- END WORKLOAD PATH TOGGLE ---

# --- MAPPING PATH TOGGLE: uncomment ONE of the two lines below ---
#mapping = "lab_cimp/inputs/mapping/mapping_3D.yaml"          # <-- Specific spatial mapping hint
mapping = "lab_cimp/inputs/mapping/mapping_3D_search.yaml"   # <-- Auto-search spatial mapping
# --- END MAPPING PATH TOGGLE ---

# Define other inputs of api call
temporal_mapping_search_engine = "loma"
optimization_criterion = "latency"
dump_folder = f"lab_cimp/outputs/{experiment_id}"
pickle_filename = f"lab_cimp/outputs/{pickle_name}.pickle"


# Get the hardware performance through api call
energy, latency, tclk, area, results = get_hardware_performance_zigzag(
    accelerator=accelerator,
    workload=workload,
    mapping=mapping,
    temporal_mapping_search_engine=temporal_mapping_search_engine,
    opt=optimization_criterion,
    dump_folder=dump_folder,
    pickle_filename=pickle_filename,
    in_memory_compute=True,
)

# Save a bar plot of the cost model evaluations breakdown
cmes = [result[0] for result in results[0][1]]
save_path = "lab_cimp/outputs/breakdown_3D.png"
bar_plot_cost_model_evaluations_breakdown(cmes, save_path=save_path)
print_mapping(cmes[0])

# Get the top CME result
best_cme = cmes[0]

# All math is now natively handled by ZigZag's core classes!
logger.info("=== ZigZag System-Level Metrics (3D) ===")
logger.info("System MAC TOPS: %.4f", best_cme.system_tops)
logger.info("System TOPS/W: %.4f", best_cme.system_topsw)
logger.info("System EDP: %.4f", best_cme.system_edp)
logger.info("System Energy (pJ): %.2f", best_cme.energy_total)
logger.info("System Latency (ns): %.2f", best_cme.system_delay_ns)

# Detailed Breakdown
mac_energy = best_cme.mac_energy
mem_energy = best_cme.mem_energy
logger.info("--- Detailed Breakdown ---")
logger.info("Energy Breakdown (pJ): Computation = %.2f | Memory Transfer = %.2f", mac_energy, mem_energy)

mac_cycles = best_cme.ideal_temporal_cycle
mem_stall_cycles = best_cme.stall_slack_comb
logger.info("Cycles Breakdown: Computation = %.1f | Memory Stalling = %.1f", mac_cycles, mem_stall_cycles)

# Extract macro metrics directly from the ImcArray
imc_macro = best_cme.accelerator.operational_array
tbops, pops, etot = imc_macro.get_macro_level_bit_ops_performance()

logger.info("=== 3D CIMP Analyser Verification [%s] ===", imc_macro.tech_param.get("cimp_manufacturing_tech", "unknown"))
cell_array_area_mm2 = (imc_macro.wordline_dim_size * imc_macro.nb_of_banks * imc_macro.cells_area) / 1e6
logger.info("Cell Array Area (mm^2): %.4f", cell_array_area_mm2)
logger.info("Macro T-put(TbOPS): %.3f", tbops)
logger.info("POPS/W/b: %.1f", pops)
Lx = imc_macro.activation_precision / imc_macro.bit_serial_precision
Sw = imc_macro.weight_precision
mac_tops_w = (pops * 1000) / (Lx * Sw) * 2
logger.info("MAC TOPS/W: %.1f", mac_tops_w)

logger.info("Etot(fJ/bOP): %.3f", etot)
logger.info("Latency(ns): %.1f", imc_macro.tclk * (imc_macro.activation_precision / imc_macro.bit_serial_precision))

logger.info("=== MAC Energy Breakdown ===")
logger.info("Capacitor Array (pJ): %.2f", imc_macro.energy_breakdown.get("mults", 0))
logger.info("ADCs (pJ): %.2f", imc_macro.energy_breakdown.get("adcs", 0))
logger.info("DACs (pJ): %.2f", imc_macro.energy_breakdown.get("dacs", 0))

exit()
