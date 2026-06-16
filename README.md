# ZigZag-CIMP: Capacitive In-Memory Processing Extension for ZigZag

A hardware–software co-design framework for exploring **capacitive in-memory processing (CIMP)** accelerators, including **3D pillar-based architectures with ADC grouping**. Built on top of [ZigZag](https://github.com/KULeuven-MICAS/zigzag) (KU Leuven), this fork integrates the charge-domain physics of [SEMRON's CapRAM](https://www.nature.com/articles/s41928-021-00649-y) technology directly into ZigZag's architecture modeling, enabling system-level design space exploration with device-level fidelity.

**Based on:**
- L. Mei, P. Houshmand, V. Jain, S. Giraldo, M. Verhelst *"ZigZag: Enlarging Joint Architecture-Mapping Design Space Exploration for DNN Accelerators"*, IEEE Transactions on Computers, vol. 70, no. 8, pp. 1160-1174 (Aug. 2021)
- Demasius, Kirschen & Parkin  *"Energy-efficient memcapacitor devices for neuromorphic computing"*, Nature Electronics 4, 748–756 (2021)
- Demasius, Lowa & Murmann  *"A Blueprint for Accurate, Energy-Efficient DNN Inference via Capacitive In-Memory Processing"*, IEEE CCMCC (2025)

---

## What This Repository Contains

```
zigzag-cimp/
├── zigzag/                    # Modified ZigZag core with CIMP physics engine (2D + 3D)
├── lab_cimp/                  # System-level CIMP evaluation (2D and 3D configurations)
├── semron_cimp/               # Standalone CIMP energy model & figure reproduction
├── figures/                   # System-level analysis plots (SRAM sweeps, rooflines)
└── requirements.txt
```

### `zigzag/` — Modified ZigZag Core

The following ZigZag source files were modified to support CIMP (2D and 3D):

| File | What Changed |
|------|-------------|
| `hardware/architecture/imc_unit.py` | Added `TECH_PARAM_CIMP` with capacitive device constants (C_max, V_in, kT, ON/OFF ratio, manufacturing tech limits, ADC FOM). Constructor loads these when `imc_type: cimp`. Accepts `cimp_adc_grouping` parameter for 3D pillar stacking. |
| `hardware/architecture/imc_array.py` | CIMP branches in `get_tclk()`, `get_area()`, `get_peak_energy_single_cycle()`, and `get_energy_for_a_layer()`. Implements N_av averaging, Walden FOM ADC energy, dual-B_y resolution, manufacturing K_max guardrails, and **3D pillar physics** with K_eff = K × g scaling for ADC grouping. Added `get_macro_level_bit_ops_performance()`. |
| `cost_model/cost_model_imc.py` | Added `system_tops`, `system_topsw`, `system_edp`, `system_delay_ns` properties for true system-level metrics including memory overhead. |
| `parser/accelerator_factory.py` | Parses `cimp_on_off_ratio`, `cimp_manufacturing_tech`, and `cimp_adc_grouping` from YAML and propagates to ImcArray. |
| `parser/accelerator_validator.py` | Validates CIMP-specific YAML fields including `cimp_adc_grouping`. |
| `stages/mapping/spatial_mapping_generation.py` | Guard for `served_dimensions: []` to prevent crash on IMC cells. |

### `lab_cimp/` — System-Level CIMP Evaluation

Run a CIMP accelerator on real DNN workloads through ZigZag's full pipeline: spatial mapping, temporal mapping search (LOMA), memory hierarchy modeling, and energy/latency/area analysis.

```
lab_cimp/
├── main.py                              # 2D CIMP entry point
├── main_3D.py                           # 3D CIMP entry point (pillar-based with ADC grouping)
├── experiment_sram.py                   # Sweep SRAM buffer sizes (3D)
├── experiment_sram_bw.py                # Sweep SRAM bandwidth
├── experiment_dram_bw.py                # Sweep DRAM bandwidth
├── experiment_dram_size.py              # Sweep DRAM configuration
└── inputs/
    ├── hardware/
    │   ├── cimp.yaml                    # 2D CIMP accelerator (4096×128, ON/OFF=100)
    │   └── cimp_3D.yaml                 # 3D CIMP accelerator (64×128×64, g=1)
    ├── mapping/
    │   ├── mapping.yaml                 # 2D weight-stationary dataflow
    │   ├── mapping_3D.yaml              # 3D fixed spatial mapping (K→D1, C→D2, OX→D3)
    │   └── mapping_3D_search.yaml       # 3D auto-search spatial mapping
    └── workload/
        ├── full_utilization.yaml        # 2D ideal workload (128×4096 MVM)
        ├── full_utilization_3d.yaml     # 3D ideal workload (64×128×64 MVM)
        └── resnet18_first_layer.onnx    # ResNet-18 Conv1 (realistic, poorly-fitting)
```

### `semron_cimp/` — Standalone Energy Model & DSE Tool

Device-level analysis independent of ZigZag. Reproduces figures from the CCMCC 2025 paper and provides design space exploration engines for both 2D and 3D architectures.

```
semron_cimp/
├── cimp_analyser.py          # 2D DSE tool: sweeps K, ON/OFF, Sw, M, Lx
├── cimp_analyser_3D.py       # 3D DSE tool: sweeps K, g, M, N → finds optimal ADC grouping
├── limit_7.py                # Fig 7:  Manufacturing feasibility (σ vs K per technology)
├── Nav_R_K_9.py              # Fig 9:  Number of averages vs ON/OFF ratio
├── Nav_R_K_9_128.py          # Fig 9 variant: K=128 focused
├── Nav_mac_time_10.py        # Fig 10: Nav vs MAC bitwidth
├── Ecap_R_Pops_12.py         # Fig 12: Capacitive thermal energy vs ON/OFF ratio
├── Etot_K_Pops.py            # Fig 13: Total energy vs column length K
├── Etot_By_Pops.py           # Fig 14: Total energy vs ADC resolution
├── figures/                  # Generated plots (PNG)
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
```

---

## Quick Start

### 2D CIMP Evaluation

**Step 1: Run the 2D evaluation:**

```bash
python lab_cimp/main.py
```

Toggle between workloads by editing `lab_cimp/main.py`:

```python
workload_name = "full_utilization"              # Ideal workload (128×4096 MVM)
# workload_name = "resnet18_first_layer"        # ResNet-18 Conv1 (realistic)
```

**Step 2: Read the output.** ZigZag will print the peak macro limits compared to the true system-level mapped performance (which includes memory overheads):

```text
[Macro-Level Peak Limits]
29.6 TbOps / 16 = 1.8 TMACs = 3.7 TOPs
(Lx = 4, Sw = 4) → comparing against GPU

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

### 3D CIMP Evaluation (Pillar-Based with ADC Grouping)

The 3D configuration models a vertically stacked array where multiple 2D planes share ADCs through pillar grouping.

**Step 1: Run the 3D evaluation:**

```bash
python lab_cimp/main_3D.py
```

Toggle between workloads, mapping strategies, and hardware in `lab_cimp/main_3D.py`:

```python
# Workload: ideal 3D full-utilization or realistic ResNet-18
workload = "lab_cimp/inputs/workload/full_utilization_3d.yaml"
# workload = "lab_cimp/inputs/workload/resnet18_first_layer.onnx"

# Mapping: fixed spatial hints or auto-search
mapping = "lab_cimp/inputs/mapping/mapping_3D.yaml"           # Fixed: K→D1, C→D2, OX→D3
# mapping = "lab_cimp/inputs/mapping/mapping_3D_search.yaml"  # Auto-search all combos
```

**Step 2: Read the output.** ZigZag prints the optimal loop ordering, followed by system-level and macro-level metrics:

```text
=== ZigZag System-Level Metrics (3D) ===
System MAC TOPS: 0.1233
System TOPS/W: 19.4862
System EDP: 457501869.0662
System Energy (pJ): 53811.17
System Latency (ns): 8501.99

--- Detailed Breakdown ---
Energy Breakdown (pJ): Computation = 2271.21 | Memory Transfer = 51539.97
Cycles Breakdown: Computation = 8.0 | Memory Stalling = 0.0    

=== 3D CIMP Analyser Verification [immersion] ===
Cell Array Area (mm^2): 0.0014
Macro T-put(TbOPS): 29.600
POPS/W/b: 3.7
Etot(fJ/bOP): 0.271
Latency(ns): 283.4
```

**Step 3 (optional): Run memory hierarchy sweeps:**

```bash
python lab_cimp/experiment_sram.py        # Sweep SRAM sizes (32–8192 KB)
python lab_cimp/experiment_sram_bw.py     # Sweep SRAM bandwidth
python lab_cimp/experiment_dram_bw.py     # Sweep DRAM bandwidth
```

These generate plots in the `figures/` directory.

---

## Hardware Configuration

### 2D CIMP Array (`cimp.yaml`)

```yaml
operational_array:
  imc_type: cimp                        # Activates CIMP physics engine
  cimp_on_off_ratio: 100                # Device quality (5–100)
  cimp_manufacturing_tech: "immersion"  # "duv", "immersion", or "sonos"
  input_precision: [4, 4]              # [Lx (activation slices), Sw (weight bits)]
  bit_serial_precision: 1              # Sx: bits processed per cycle
  dimensions: [D1, D2]                 # 2D: columns × rows
  sizes: [4096, 128]                   # [M (columns), K (rows)]
```

### 3D CIMP Pillar Array (`cimp_3D.yaml`)

The 3D configuration adds a vertical stacking dimension and ADC grouping:

```yaml
operational_array:
  imc_type: cimp
  cimp_on_off_ratio: 100
  cimp_manufacturing_tech: "immersion"
  cimp_adc_grouping: 1                 # g: pillars sharing one ADC (1, 2, 4, ...)
  input_precision: [4, 4]             # [Lx, Sw]
  bit_serial_precision: 1
  dimensions: [D1, D2, D3]            # 3D: columns × layers × rows
  sizes: [64, 128, 64]                # [M (cols), K (layers/depth), N (physical rows)]
```

**Dimension mapping:**

| YAML Dimension | Physical Meaning | CIMP Variable |
|---------------|-----------------|---------------|
| D1 | Columns (wordline direction) | M |
| D2 | Layers / vertical depth (bitline direction) | K |
| D3 | Physical rows (bank direction) | N |

**ADC Grouping (`cimp_adc_grouping = g`):**

When `g > 1`, `g` adjacent pillars share a single ADC. This increases the effective bitline length to `K_eff = K × g`, which:
- ✅ Reduces the number of ADCs (saves area and ADC energy)
- ⚠️ Increases noise (longer bitlines → more N_av averaging cycles → higher latency)
- ⚠️ Must satisfy manufacturing feasibility: `K_eff ≤ K_max(tech, Sw)`

ZigZag will raise a `ValueError` if `K_eff` exceeds the manufacturing limit for the chosen technology.

---

## Repository Structure Reference

| Path | Purpose |
|------|---------|
| `lab_cimp/main.py` | 2D CIMP system-level evaluation |
| `lab_cimp/main_3D.py` | 3D CIMP system-level evaluation |
| `lab_cimp/experiment_*.py` | Memory hierarchy parameter sweeps |
| `lab_cimp/inputs/hardware/cimp.yaml` | 2D CIMP hardware definition |
| `lab_cimp/inputs/hardware/cimp_3D.yaml` | 3D CIMP hardware definition |
| `lab_cimp/inputs/workload/` | DNN workloads (YAML or ONNX) |
| `lab_cimp/inputs/mapping/` | Spatial mapping hints (fixed and auto-search) |
| `semron_cimp/cimp_analyser.py` | 2D device-level DSE tool (standalone) |
| `semron_cimp/cimp_analyser_3D.py` | 3D device-level DSE tool with ADC grouping (standalone) |
| `semron_cimp/*.py` | Figure reproduction scripts (standalone) |
| `semron_cimp/figures/` | Generated device-level plots |
| `semron_cimp/report/` | Technical report (3 parts) |
| `figures/` | System-level analysis plots |
| `zigzag/hardware/architecture/imc_unit.py` | CIMP tech parameters & ADC grouping |
| `zigzag/hardware/architecture/imc_array.py` | CIMP energy, latency, area models (2D + 3D) |
| `zigzag/cost_model/cost_model_imc.py` | System-level metric properties |
| `zigzag/parser/accelerator_factory.py` | CIMP YAML parameter parsing |
| `zigzag/parser/accelerator_validator.py` | CIMP YAML schema validation |

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

**Run the 2D design space exploration:**

```bash
python cimp_analyser.py
```

**Run the 3D design space exploration with ADC grouping:**

```bash
python cimp_analyser_3D.py
```

This sweeps across K (layers), g (ADC grouping factor), M (columns), N (rows), ON/OFF ratio, Sw (weight precision), and Lx (input slices), pruning infeasible configurations based on K_eff manufacturing limits. Outputs ranked leaderboards for energy efficiency, speed, minimum ADCs, and EDP.

To explore a specific configuration subset, edit the ranges at the bottom of the analyser scripts:

```python
# cimp_analyser.py (2D)
allowed_Ks = [128, 256, 512]
allowed_rs = [10, 50, 100]
allowed_Sws = [2, 4]
allowed_Ms = [128, 256, 512, 1024]
allowed_Lxs = [4, 8]

# cimp_analyser_3D.py (3D)
allowed_Ks = []           # Empty = full sweep
allowed_Sws = [4]
allowed_rs = [100]
allowed_Ms = [8192]
allowed_Ns = [8192]
allowed_Lxs = [4]
allowed_gs = []           # Empty = full sweep [1,2,4,8,16,32,64]
```

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
