"""
Test CapRAM extension — reproduce SEMRON's 29,600 TOPS/W
==========================================================
Uses the 1000×1000 array (Paper 1 Table 1) with W4A8, Sx=1.

Progressive enhancement:
1. Baseline ZigZag (SRAM-based AIMC model)
2. CapRAM physics (no recovery, no sparsity) — worst case
3. + 95% energy recovery (adiabatic) — Paper 1 Table 1 worst case
4. + MNIST sparsity (4.29×) — Paper 1 Supplementary Section 6 target
"""
import sys, os
sys.path.insert(0, os.getcwd())

import logging
import yaml
import tempfile

logging.basicConfig(level=logging.WARNING)

from zigzag.hardware.architecture.imc_array import ImcArray
from zigzag.stages.parser.accelerator_parser import AcceleratorParserStage
from capram.capram_array import CapRamArray


def make_yaml(array_size):
    config = {
        "name": "capram_test",
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


def evaluate(imc, label):
    tops, topsw, topsmm2 = imc.get_macro_level_peak_performance()
    eb = imc.get_peak_energy_single_cycle()
    total_e = sum(eb.values())

    print(f"\n{'='*70}")
    print(f"{label}")
    print(f"{'='*70}")
    print(f"Array:         {imc.wordline_dim_size} × {imc.bitline_dim_size}")
    print(f"Config:        W{imc.weight_precision}A{imc.activation_precision}, "
          f"Sx={imc.bit_serial_precision}, ADC={imc.adc_resolution} bit")
    print(f"Area:          {imc.area:.4f} mm²")
    print(f"Tclk:          {imc.tclk:.4f} ns")
    print(f"Energy/cycle:  {total_e:.6f} pJ")
    if total_e > 0:
        nonzero = {k: v for k, v in eb.items() if v > 0}
        print(f"Breakdown:     " + ", ".join(f"{k}={v:.4f}" for k, v in nonzero.items()))
    print(f"")
    print(f"  → TOP/s:     {tops:.4f}")
    print(f"  → TOP/s/W:   {topsw:,.1f}")
    print(f"  → TOP/s/mm²: {topsmm2:.4f}")
    return tops, topsw, topsmm2


array_size = 1000
yaml_path = make_yaml(array_size)

print("\n" + "█" * 70)
print(f"REPRODUCING SEMRON's 29,600 TOPS/W on {array_size}×{array_size} ARRAY")
print("█" * 70)

accelerator = AcceleratorParserStage.parse_accelerator(yaml_path)
zigzag_imc = accelerator.operational_array

config = {
    "is_analog_imc": zigzag_imc.is_aimc,
    "bit_serial_precision": zigzag_imc.bit_serial_precision,
    "input_precision": [zigzag_imc.activation_precision, zigzag_imc.weight_precision],
    "adc_resolution": zigzag_imc.adc_resolution,
    "cells_size": zigzag_imc.cells_size,
    "cells_area": zigzag_imc.cells_area,
    "dimension_sizes": zigzag_imc.dimension_sizes,
    "auto_cost_extraction": False,
}

_, topsw_0, _ = evaluate(zigzag_imc, "1. ZigZag BASELINE (SRAM-based AIMC model)")

capram_worst = CapRamArray(**config, enable_energy_recovery=False, enable_sparsity=False)
_, topsw_1, _ = evaluate(capram_worst, "2. CapRAM physics (NO recovery, NO sparsity)")

capram_rec = CapRamArray(**config, enable_energy_recovery=True, enable_sparsity=False)
_, topsw_2, _ = evaluate(capram_rec, "3. CapRAM + 95% ENERGY RECOVERY")

capram_full = CapRamArray(**config, enable_energy_recovery=True, enable_sparsity=True, workload="mnist")
_, topsw_3, _ = evaluate(capram_full, "4. CapRAM + recovery + MNIST sparsity → target: 29,600 TOPS/W")

print("\n" + "█" * 70)
print("SUMMARY — Progressive enhancement toward SEMRON's 29,600 TOPS/W")
print("█" * 70)
print(f"\n{'Configuration':<60} {'TOP/s/W':>12}")
print("-" * 75)
print(f"{'1. ZigZag SRAM-based AIMC baseline':<60} {topsw_0:>12,.1f}")
print(f"{'2. + CapRAM capacitive physics (no recovery)':<60} {topsw_1:>12,.1f}")
print(f"{'3. + 95% energy recovery (adiabatic charging)':<60} {topsw_2:>12,.1f}")
print(f"{'4. + MNIST sparsity (4.29x from 77% zero inputs)':<60} {topsw_3:>12,.1f}")
print("-" * 75)
print(f"{'SEMRON Paper 1 target (Supplementary Section 6)':<60} {'29,600':>12}")
print(f"\nBoost factors:")
print(f"  CapRAM physics vs ZigZag SRAM:  {topsw_1/topsw_0:>7.1f}x")
print(f"  Energy recovery:                {topsw_2/topsw_1:>7.1f}x")
print(f"  MNIST sparsity:                 {topsw_3/topsw_2:>7.1f}x")
print(f"  TOTAL vs ZigZag baseline:       {topsw_3/topsw_0:>7.0f}x")
print(f"\nMatch vs SEMRON Paper 1 target: {topsw_3/29600*100:.1f}%")
print(f"Absolute error: {abs(topsw_3 - 29600):.0f} TOPS/W")

os.unlink(yaml_path)
