# ZigZag-CIMP Lab (`lab_cimp`)

This directory contains the system-level integration of **capacitive in-memory processing (CIMP)** models into the ZigZag DNN accelerator design space exploration framework. Built to support the charge-domain physics of **SEMRON's CapRAM** technology, this lab enables accurate evaluation of both 2D and **3D pillar-based CIMP architectures with ADC grouping**.

## Overview

The `lab_cimp` project evaluates CIMP accelerators on real DNN workloads through ZigZag's full pipeline: spatial mapping, temporal mapping search (LOMA), memory hierarchy modeling, and system-level energy/latency/area analysis. 

Key modeling features include:
* **Capacitive CIMP Physics**: Calculates maximum possible physical Rows (K) before manufacturing variation impacts feasibility (`K_crossover`), and computes energies (`E_cap`, `E_tot`) for SEMRON-like charge-domain arrays.
* **3D Pillar Architectures & ADC Grouping**: Supports vertical 3D arrays where multiple planes share ADCs through pillar grouping (`cimp_adc_grouping = g`). Accurately models the noise, increased N_av (Number of Averages) cycles, and latency trade-offs of long bitlines.
* **System-Level Evaluation**: Combines macro-level CIMP array computational energy with hierarchical memory transfer costs to give an accurate system EDP (Energy-Delay Product), latency, and TOPS/W.

## Usage

### 2D CIMP Evaluation
Run the standard 2D CIMP evaluation to test an ideal `full_utilization` workload or a realistic ONNX model (like ResNet-18) on a 2D CapRAM array:

```bash
# Activate your environment
source .venv/bin/activate  

# Run the 2D evaluation
python lab_cimp/main.py
```

### 3D CIMP Evaluation (ADC Grouping)
Run the 3D pillar-based evaluation, which includes vertical stacking (`D3` dimension) and ADC grouping:

```bash
python lab_cimp/main_3D.py
```

### Configuring the Run
Inside `main.py` and `main_3D.py`, you can toggle between workloads, hardware architectures (`cimp.yaml` vs `cimp_3D.yaml`), and mapping strategies (fixed vs. auto-search). 

## Example Output Metrics

When running the scripts, the engine will output detailed peak CIMP macro performance limits and compare them against the true system-level mapped performance. 

*Example log excerpt from a 2D full utilization test (`main.py`):*
```text
=== CIMP Analyser Verification [immersion] ===
29.6 TbOps / 16 = 1.8 TMACs = 3.7 TOPs
3.7 POPS/W/b = 3,693 TOPS/W/b
3,693 / 16 (Lx×Sw = 4×4) × 2 (MAC) = 461.7 TOPS/W
→ absolute max TOPS/W possible to achieve

=== ZigZag System-Level Metrics ===
System MAC TOPS: 0.2277
System TOPS/W: 38.1918
System EDP: 505757438.0701
System Energy (pJ): 54911.05
System Latency (ns): 9210.49

--- Detailed Breakdown ---
Energy Breakdown (pJ): Computation = 4542.41 | Memory Transfer = 50368.64
Latency(ns): 283.4
```

*Note that while the macro's absolute maximum efficiency limit may be extremely high (~461 TOPS/W), real-world system utilization bounded by memory transfers, spatial mapping constraints, and ADC grouping brings the achievable system efficiency to a realistic metric (e.g., ~38 TOPS/W).*

## Memory Hierarchy Sweeps

For detailed design space sweeps of the memory hierarchy, use the provided standalone experiment scripts:
- `experiment_sram.py`: Sweep SRAM sizes (32–8192 KB) for 3D architectures
- `experiment_sram_bw.py`: Sweep SRAM bandwidth
- `experiment_dram_size.py` & `experiment_dram_bw.py`: Sweep DRAM configurations
- `experiment_rf_size_bw.py`: Sweep register file bandwidths
- `experiment_dram_size_bw.py` & `experiment_sram_size_bw.py`: Combined sweeps

These scripts generate analysis plots inside the `figures/` directory.
