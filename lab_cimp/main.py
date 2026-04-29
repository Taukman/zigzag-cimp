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

# Define the experiment id and pickle name
hw_name = "accelerator1"
workload_name = "resnet18_first_layer"
experiment_id = f"{hw_name}-{workload_name}"
pickle_name = f"{experiment_id}-saved_list_of_cmes"

# Define main input paths
accelerator = "lab_cimp/inputs/hardware/cimp.yaml"
workload = "lab_cimp/inputs/workload/full_utilization.yaml"
mapping = "lab_cimp/inputs/mapping/mapping.yaml"

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
save_path = "lab_cimp/outputs/breakdown.png"
bar_plot_cost_model_evaluations_breakdown(cmes, save_path=save_path)
print_mapping(cmes[0])

# Get the top CME result
best_cme = cmes[0]

# All math is now natively handled by ZigZag's core classes!
logger.info("=== ZigZag System-Level Metrics ===")
logger.info("System MAC TOPS: %.4f", best_cme.system_tops)
logger.info("System TOPS/W: %.4f", best_cme.system_topsw)
logger.info("System EDP: %.4f", best_cme.system_edp)
logger.info("System Energy (pJ): %.2f", best_cme.energy_total)
logger.info("System Latency (ns): %.2f", best_cme.system_delay_ns)

# Extract macro metrics directly from the ImcArray
imc_macro = best_cme.accelerator.operational_array
tbops, pops, etot = imc_macro.get_macro_level_bit_ops_performance()

logger.info("=== CIMP Analyser Verification [%s] ===", imc_macro.tech_param.get("cimp_manufacturing_tech", "unknown"))
logger.info("Macro T-put(TbOPS): %.3f", tbops)
logger.info("POPS/W/b: %.1f", pops)
logger.info("Etot(fJ/bOP): %.3f", etot)
logger.info("Latency(ns): %.1f", imc_macro.tclk * (imc_macro.activation_precision / imc_macro.bit_serial_precision))

exit()
