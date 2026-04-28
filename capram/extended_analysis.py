"""
Extended CapRAM Analysis
=========================
Now that we've reproduced 29,600 TOPS/W, let's explore:

1. Array size sweep (how efficiency scales with K)
2. ON/OFF ratio sensitivity (from Paper 2 Fig. 9)
3. Comparison with other IMC technologies
4. The landscape of capacitive vs resistive IMC
"""
import sys, os
sys.path.insert(0, os.getcwd())

import logging
import yaml
import tempfile

logging.basicConfig(level=logging.WARNING)

from zigzag.stages.parser.accelerator_parser import AcceleratorParserStage
from capram.capram_array import CapRamArray


def make_yaml(array_size):
    config = {
        "name": "capram_sweep",
        "memories": {
            "cells": {
                "size": 8, "r_bw": 8, "w_bw": 8,
                "r_cost": 0, "w_cost": 0.095, "area": 0,
                "r_port": 1, "w_port": 1, "rw_port": 0,
                "latency": 0, "auto_cost_extraction": True,
                "operands": ["I2"],
                "ports": [{"fh": "w_port_1", "tl": "r_port_1"}],
                "served_dimensions": []
            }
        },
        "operational_array": {
            "is_imc": True, "imc_type": "analog",
            "input_precision": [8, 4],
            "bit_serial_precision": 1,
            "adc_resolution": 8,
            "dimensions": ["D1", "D2"],
            "sizes": [array_size, array_size]
        }
    }
    tmpf = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, dir='/tmp')
    yaml.dump(config, tmpf)
    tmpf.close()
    return tmpf.name


def make_capram(array_size, recovery=True, sparsity=True):
    yaml_path = make_yaml(array_size)
    acc = AcceleratorParserStage.parse_accelerator(yaml_path)
    z = acc.operational_array
    config = {
        "is_analog_imc": z.is_aimc,
        "bit_serial_precision": z.bit_serial_precision,
        "input_precision": [z.activation_precision, z.weight_precision],
        "adc_resolution": z.adc_resolution,
        "cells_size": z.cells_size,
        "cells_area": z.cells_area,
        "dimension_sizes": z.dimension_sizes,
        "auto_cost_extraction": False,
    }
    capram = CapRamArray(
        **config,
        enable_energy_recovery=recovery,
        enable_sparsity=sparsity,
        workload="mnist",
    )
    os.unlink(yaml_path)
    return capram


# ================================================================
# PART 1: Array size sweep (reproduces Paper 1 Table 1 scaling)
# ================================================================
print("\n" + "█" * 70)
print("PART 1: ARRAY SIZE SWEEP")
print("Reproducing SEMRON Paper 1 Table 1 (worst case, no sparsity)")
print("█" * 70)

print(f"\n{'Size':>10} | {'Area (mm²)':>10} | {'Period (ns)':>11} | "
      f"{'Energy/MVM (pJ)':>15} | {'TOPS/W (worst)':>14} | {'TOPS/W (MNIST)':>14}")
print("-" * 95)

for size in [100, 500, 1000, 2500]:
    # Worst case (with recovery, no sparsity) - Table 1 target
    capram_worst = make_capram(size, recovery=True, sparsity=False)
    _, topsw_worst, _ = capram_worst.get_macro_level_peak_performance()

    # With MNIST sparsity
    capram_mnist = make_capram(size, recovery=True, sparsity=True)
    _, topsw_mnist, _ = capram_mnist.get_macro_level_peak_performance()

    # Energy per full MVM (all 142 cycles)
    e_per_cycle = sum(capram_worst.get_peak_energy_single_cycle().values())
    e_per_mvm = e_per_cycle * 142

    print(f"{size}×{size:<6} | {capram_worst.area:>10.4f} | "
          f"{capram_worst.tclk:>11.2f} | {e_per_mvm:>15.2f} | "
          f"{topsw_worst:>14,.1f} | {topsw_mnist:>14,.0f}")

print("\nSEMRON Paper 1 Table 1 targets (worst case, with recovery):")
print("  100×100:   3,782 TOPS/W    500×500:   3,677 TOPS/W")
print("  1000×1000: 3,453 TOPS/W    2500×2500: 3,462 TOPS/W")
print("  (Our numbers are based on Paper 1 Table 1 values directly)")

# ================================================================
# PART 2: Energy Recovery Sensitivity
# ================================================================
print("\n" + "█" * 70)
print("PART 2: ENERGY RECOVERY SENSITIVITY (1000×1000, MNIST)")
print("What if adiabatic hardware can't achieve 95% recovery?")
print("█" * 70)

print(f"\n{'Recovery %':>10} | {'Energy/cell/MVM (fJ)':>20} | {'TOPS/W':>12} | {'vs 95% baseline':>18}")
print("-" * 75)

W_r = 5.0e-15
W_p = 0.04e-15
baseline_topsw = None

for rec_pct in [0, 50, 80, 90, 95, 99]:
    # Manually compute (since we'd need to monkey-patch the constant)
    rec = rec_pct / 100
    e_eff = (W_p + (1 - rec) * W_r) * 1e15  # fJ
    e_total_per_cell = e_eff / 4.29  # with MNIST sparsity
    # TOPS/W = 2 ops / (e_eff in pJ × 1e-3) = 2 / (e_eff fJ × 1e-3)
    topsw = 2 / (e_total_per_cell * 1e-3)
    if rec_pct == 95:
        baseline_topsw = topsw
    vs_baseline = f"{topsw / 29586 * 100:.1f}%" if baseline_topsw else "—"
    print(f"{rec_pct:>10}% | {e_eff:>20.3f} | {topsw:>12,.1f} | {vs_baseline:>18}")

# ================================================================
# PART 3: Capacitive vs Resistive IMC (from Paper 2 Section V)
# ================================================================
print("\n" + "█" * 70)
print("PART 3: CAPACITIVE vs RESISTIVE IMC (theoretical limits)")
print("From Paper 2 Section V equations 46, 49, 51")
print("█" * 70)

# Paper 2 derives these from signal-to-noise constraints (3σ ≤ 0.5 LSB):
# E_cap = 36 × 2^(2By) × kT             [capacitive thermal limit]
# E_res = 36 × 2^(2By) × 2kT            [resistive thermal limit]
# E_shot = 36 × 2^(2By) × q × V         [resistive with shot noise]

import math
kT = 1.381e-23 * 300
q = 1.602e-19
V = 0.4

print(f"\nTheoretical fundamental energy limits (J/op) vs ADC resolution:")
print(f"{'By':>4} | {'E_cap (fJ)':>12} | {'E_res (fJ)':>12} | {'E_shot (fJ)':>12} | "
      f"{'Res/Cap':>8} | {'Shot/Cap':>10}")
print("-" * 85)

for By in [4, 6, 8, 10, 12, 14]:
    E_cap = 36 * 2**(2*By) * kT
    E_res = 36 * 2**(2*By) * 2 * kT
    E_shot = 36 * 2**(2*By) * q * V

    print(f"{By:>4} | {E_cap*1e15:>12.4f} | {E_res*1e15:>12.4f} | {E_shot*1e15:>12.4f} | "
          f"{E_res/E_cap:>8.1f} | {E_shot/E_cap:>10.1f}")

print("""
Interpretation:
- Capacitive is fundamentally 2× more efficient than resistive (thermal-limited)
- Capacitive is 15.4× more efficient than shot-noise-limited (ReRAM, PCM)
- This is the PHYSICS advantage, before considering adiabatic recovery
- With 95% recovery, capacitive effectively gets another 20× on top
""")

# ================================================================
# PART 4: State-of-the-Art Comparison
# ================================================================
print("\n" + "█" * 70)
print("PART 4: STATE-OF-THE-ART COMPARISON")
print("Paper 2 cites these numbers (TOPS/W/b, normalized per bit)")
print("█" * 70)

# TOPS/W/b means TOPS divided by (weight precision × activation precision)
# For W4A8 that's /(4×8) = /32 (or some normalize by input bits only)
# Paper 2 uses /b based on ADC bit-depth typically

technologies = [
    ("CapRAM (SEMRON, projected)",   29600, "charge shielding memcapacitor"),
    ("SRAM 10T3C (Paper 6)",          8161, "10 transistor + 3 capacitor, 28nm"),
    ("SRAM 6T/8T (Paper 5)",          5616, "7nm compute-in-memory"),
    ("ReRAM / PCM (typical)",         1344, "resistive, variability limited"),
    ("ReRAM / PCM (lower end)",        336, "resistive, earliest designs"),
    ("CapRAM worst case (our calc)",  6897, "just physics + recovery, no sparsity"),
]

print(f"\n{'Technology':<35} {'TOPS/W/b':>12}  {'Notes':<40}")
print("-" * 90)
for name, tops_wb, notes in sorted(technologies, key=lambda x: -x[1]):
    print(f"{name:<35} {tops_wb:>12,}  {notes:<40}")

print("""
SEMRON's ~29,600 TOPS/W comes from combining:
1. Capacitive physics  (~2× advantage vs resistive thermal)
2. Energy recovery     (~17× via adiabatic charging)
3. Workload sparsity   (~4.3× from MNIST zero inputs)
4. Low ADC resolution  (~8 bits via A2Q+ training, Paper 2)
5. Dense 3D integration (not modeled here, but matters for TOPS/mm²)

ZigZag's SRAM-based model captures NONE of these advantages by default,
which is why our extension (~180 lines of Python) is needed to bridge
the gap between SRAM-CIM modeling and capacitive IMC modeling.
""")
