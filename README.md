# ZigZag-CIMP: Capacitive In-Memory Processing Extension for ZigZag

A hardware–software co-design framework for exploring **capacitive in-memory processing (CIMP)** accelerators. Built on top of [ZigZag](https://github.com/KULeuven-MICAS/zigzag) (KU Leuven), this fork integrates the charge-domain physics of [SEMRON's CapRAM](https://www.nature.com/articles/s41928-021-00649-y) technology directly into ZigZag's architecture modeling, enabling system-level design space exploration with device-level fidelity.

**Based on:**
- Demasius, Kirschen & Parkin — *"Energy-efficient memcapacitor devices for neuromorphic computing"*, Nature Electronics 4, 748–756 (2021)
- Demasius, Lowa & Murmann — *"A Blueprint for Accurate, Energy-Efficient DNN Inference via Capacitive In-Memory Processing"*, IEEE CCMCC (2025)

---

## What This Repository Contains

```
zigzag-cimp/
├── zigzag/                    # Modified ZigZag core with CIMP physics engine
├── lab_cimp/                  # System-level CIMP evaluation (like ZigZag Lab 5)
├── semron_cimp/               # Standalone CIMP energy model & figure reproduction
├── lab5/                      # Original ZigZag SRAM-IMC lab (for comparison)
├── figures/                   # System-level analysis plots (SRAM sweeps, rooflines)
├── setup_lab_cimp.py          # Setup script for lab_cimp
├── requirements.txt
└── pyproject.toml
```

### `zigzag/` — Modified ZigZag Core

The following ZigZag source files were modified to support CIMP:

| File | What Changed |
|------|-------------|
| `hardware/architecture/imc_unit.py` | Added `TECH_PARAM_CIMP` with capacitive device constants (C_max, V_in, kT, ON/OFF ratio, manufacturing tech limits). Constructor loads these when `imc_type: cimp`. |
| `hardware/architecture/imc_array.py` | CIMP branches in `get_tclk()`, `get_area()`, `get_peak_energy_single_cycle()`, and `get_energy_for_a_layer()`. Implements N_av averaging, Walden FOM ADC energy, dual-B_y resolution, and manufacturing K_max guardrails. Added `get_macro_level_bit_ops_performance()`. |
| `cost_model/cost_model_imc.py` | Added `system_tops`, `system_topsw`, `system_edp`, `system_delay_ns` properties for true system-level metrics including memory overhead. |
| `parser/accelerator_factory.py` | Parses `cimp_on_off_ratio` and `cimp_manufacturing_tech` from YAML and propagates to ImcArray. |
| `parser/accelerator_validator.py` | Validates CIMP-specific YAML fields. |
| `stages/mapping/spatial_mapping_generation.py` | Guard for `served_dimensions: []` to prevent crash on IMC cells. |

### `lab_cimp/` — System-Level CIMP Evaluation

Run a CIMP accelerator on real DNN workloads through ZigZag's full pipeline: spatial mapping, temporal mapping search (LOMA), memory hierarchy modeling, and energy/latency/area analysis.

```
lab_cimp/
├── main.py                         # Main entry point (toggle between workloads)
├── experiment_sram.py              # Sweep SRAM buffer sizes
├── experiment_sram_bw.py           # Sweep SRAM bandwidth
├── experiment_dram_bw.py           # Sweep DRAM bandwidth
├── experiment_dram_size.py         # Sweep DRAM configuration
└── inputs/
    ├── hardware/cimp.yaml          # CIMP accelerator definition (128×8192, ON/OFF=100)
    ├── mapping/mapping.yaml        # Weight-stationary dataflow mapping
    └── workload/
        ├── full_utilization.yaml   # Ideal workload (128×8192 MVM, batch=2)
        └── resnet18_first_layer.onnx  # ResNet-18 Conv1 (realistic, poorly-fitting)
```

### `semron_cimp/` — Standalone Energy Model & DSE Tool

Device-level analysis independent of ZigZag. Reproduces figures from the CCMCC 2025 paper and provides a design space exploration engine.

```
semron_cimp/
├── cimp_analyser.py          # DSE tool: sweeps K, ON/OFF, Sw, M, Lx → finds optimal configs
├── limit_7.py                # Fig 7:  Manufacturing feasibility (σ vs K per technology)
├── Nav_R_K_9.py              # Fig 9:  Number of averages vs ON/OFF ratio
├── Nav_R_K_9_128.py          # Fig 9 variant: K=128 focused
├── Nav_mac_time_10.py        # Fig 10: Nav vs MAC bitwidth
├── Ecap_R_Pops_12.py         # Fig 12: Capacitive thermal energy vs ON/OFF ratio
├── Etot_K_Pops.py            # Fig 13: Total energy vs column length K
├── Etot_By_Pops.py           # Fig 14: Total energy vs ADC resolution
├── figures/                  # Generated plots (PNG)
├── papers/                   # Reference papers (PDF)
└── report/                   # Technical report (3 parts, PDF)
```

---

## Installation

### Prerequisites

- Python ≥ 3.11
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Taukman/zigzag-cimp.git
cd zigzag-cimp

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install the package in development mode
pip install -e .
```

---

## Quick Start

### Running the CIMP System-Level Evaluation (`lab_cimp`)

This is the primary entry point for evaluating a CIMP accelerator on a DNN workload.

**Step 1: Choose a workload.** Open `lab_cimp/main.py` and toggle the workload:

```python
# For the ideal full-utilization workload (128×8192 MVM):
workload_name = "full_utilization"
workload = "lab_cimp/inputs/workload/full_utilization.yaml"

# For ResNet-18 Conv1 (realistic, poorly-fitting layer):
# workload_name = "resnet18_first_layer"
# workload = "lab_cimp/inputs/workload/resnet18_first_layer.onnx"
```

**Step 2: Run from the repository root:**

```bash
python lab_cimp/main.py
```

**Step 3: Read the output.** ZigZag will print the optimal temporal loop ordering found by LOMA, followed by system-level and macro-level metrics:

```
=== ZigZag System-Level Metrics ===
System MAC TOPS: 0.2268
System TOPS/W: 19.2889
System EDP: 4020977852.4093
System Energy (pJ): 217446.30
System Latency (ns): 18491.82

=== CIMP Analyser Verification [immersion] ===
Macro T-put(TbOPS): 59.200
POPS/W/b: 3.7
Etot(fJ/bOP): 0.271
Latency(ns): 283.4
```

Outputs are saved to `lab_cimp/outputs/`.

**Step 4 (optional): Run the memory hierarchy sweeps:**

```bash
python lab_cimp/experiment_sram.py        # Sweep SRAM sizes (64–1024 KB)
python lab_cimp/experiment_sram_bw.py     # Sweep SRAM bandwidth
python lab_cimp/experiment_dram_bw.py     # Sweep DRAM bandwidth
python lab_cimp/experiment_dram_size.py   # Sweep DRAM configuration
```

These generate plots in the `figures/` directory.

### Modifying the CIMP Hardware

Edit `lab_cimp/inputs/hardware/cimp.yaml` to change:

```yaml
operational_array:
  imc_type: cimp                     # Activates CIMP physics engine
  cimp_on_off_ratio: 100             # Device quality (5–100)
  cimp_manufacturing_tech: "immersion"  # "duv", "immersion", or "sonos"
  input_precision: [4, 4]            # [activation_bits, weight_bits]
  bit_serial_precision: 1            # Sx: bits processed per cycle
  sizes: [128, 8192]                 # [columns (K), rows (M)]
```

ZigZag will raise a `ValueError` if you set array dimensions that exceed the manufacturing feasibility limit for your chosen technology.

---

### Running the Standalone Energy Model (`semron_cimp`)

These scripts reproduce figures from the CCMCC 2025 paper and do not require ZigZag.

**Reproduce individual figures:**

```bash
cd semron_cimp

python limit_7.py              # → figures/figure7_feasibility.png
python Nav_R_K_9.py            # → figures/Nav_R_K_9.png
python Nav_mac_time_10.py      # → figures/Nav_mac_time_10.png
python Ecap_R_Pops_12.py       # → figures/Ecap_R_Pops_12.png
python Etot_K_Pops.py          # → figures/Etot_K_Pops.png
python Etot_By_Pops.py         # → figures/Etot_By_Pops.png
```

**Run the full design space exploration:**

```bash
python cimp_analyser.py
```

This sweeps across all combinations of array size (K), ON/OFF ratio (r), weight precision (Sw), column count (M), and input slices (Lx), pruning infeasible configurations based on manufacturing limits. It outputs ranked leaderboards for energy efficiency, speed, EDP, and throughput. A full sweep can take several minutes.

To explore a specific configuration subset, edit the ranges at the bottom of `cimp_analyser.py`:

```python
allowed_Ks = [128, 256, 512]         # Empty list [] = full sweep
allowed_rs = [10, 50, 100]
allowed_Sws = [2, 4]
allowed_Ms = [128, 256, 512, 1024]
allowed_Lxs = [4, 8]
```

---

## Repository Structure Reference

| Path | Purpose |
|------|---------|
| `lab_cimp/main.py` | System-level CIMP evaluation on DNN layers |
| `lab_cimp/experiment_*.py` | Memory hierarchy parameter sweeps |
| `lab_cimp/inputs/hardware/cimp.yaml` | CIMP accelerator hardware definition |
| `lab_cimp/inputs/workload/` | DNN workloads (YAML or ONNX) |
| `semron_cimp/cimp_analyser.py` | Device-level DSE tool (standalone) |
| `semron_cimp/*.py` | Figure reproduction scripts (standalone) |
| `semron_cimp/figures/` | Generated device-level plots |
| `semron_cimp/report/` | Technical report (3 parts) |
| `semron_cimp/papers/` | Reference papers |
| `lab5/` | Original ZigZag SRAM-IMC lab (baseline comparison) |
| `figures/` | System-level analysis plots |
| `zigzag/hardware/architecture/imc_unit.py` | CIMP tech parameters |
| `zigzag/hardware/architecture/imc_array.py` | CIMP energy, latency, area models |
| `zigzag/cost_model/cost_model_imc.py` | System-level metric properties |
| `zigzag/parser/accelerator_factory.py` | CIMP YAML parameter parsing |

---

## Key Results

**Macro-level (CIMP Analyser, peak):**

| Metric | Value |
|--------|-------|
| Throughput | 59.2 TbOPS |
| Energy Efficiency | 3.7 POPS/W/b |
| Energy per bit-op | 0.271 fJ/bOP |
| MVM Latency | 283.4 ns |

**System-level (ZigZag, on 128 × 8192 array, immersion, ON/OFF = 100):**

| Metric | Full Utilization Layer | ResNet-18 Conv1 |
|--------|----------------------|-----------------|
| System MAC TOPS | 0.2268 | 0.0273 |
| System TOPS/W | 19.29 | 2.06 |
| System Energy (pJ) | 217,446 | 114,510,562 |
| System Latency (ns) | 18,492 | 8,651,621 |
| System EDP | 4.02 × 10⁹ | 9.91 × 10¹⁴ |
| Spatial Utilization | 100% | <1% |

The **527× energy gap** and **9.4× TOPS/W gap** between the two workloads on identical hardware demonstrates that workload–array dimension matching — not device physics — is the dominant system-level optimization target.

---

## Technical Report

The [`semron_cimp/report/`](semron_cimp/report/) folder contains a three-part technical report:

- **[Part 1 — CIMP Energy Model](semron_cimp/report/r1.pdf)**: Device-level energy model implementation, dual-B_y discovery, figure reproduction from CCMCC 2025, and `cimp_analyser` DSE tool
- **[Part 2 — ZigZag-CIMP Integration](semron_cimp/report/r2_v2.pdf)**: System-level findings, loop ordering analysis, peak-to-system gap (527× energy, 9.4× TOPS/W), and actionable recommendations for SEMRON
- **[Part 3 — Future Work](semron_cimp/report/r3.pdf)**: Heterogeneous multi-core CIMP via [Stream](https://github.com/kuleuven-micas/stream), A2Q+ quantization-aware training for ADC reduction, and the combined co-design vision

---

## Citation

If you use this work, please cite the underlying papers:

```bibtex
@article{demasius2021energy,
  title={Energy-efficient memcapacitor devices for neuromorphic computing},
  author={Demasius, Kai-Uwe and Kirschen, Aron and Parkin, Stuart},
  journal={Nature Electronics},
  volume={4},
  pages={748--756},
  year={2021}
}

@inproceedings{demasius2025blueprint,
  title={A Blueprint for Accurate, Energy-Efficient DNN Inference via Capacitive In-Memory Processing},
  author={Demasius, Kai-Uwe and Lowa, Alexander and Murmann, Boris},
  booktitle={IEEE Cross-Disciplinary Conference on Memory-Centric Computing (CCMCC)},
  year={2025}
}
```

For the ZigZag framework itself:

```bibtex
@article{symons2024zigzag,
  title={ZigZag: Enlarging Joint Architecture-Mapping Design Space Exploration for DNN Accelerators},
  author={Symons, Arne and Mei, Linyan and others},
  journal={IEEE Transactions on Computers},
  year={2024}
}
```

---

## License

MIT — see [LICENSE](LICENSE).
