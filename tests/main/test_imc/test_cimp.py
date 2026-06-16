import pytest

from zigzag.api import get_hardware_performance_zigzag_imc

workloads = (
    "zigzag/inputs/workload/resnet18.onnx",
    "zigzag/inputs/workload/resnet18.yaml",
)

# We will just print these out first to see what CIMP gives us,
# then we can assert. For now we just let it run.
@pytest.fixture
def mapping():
    return "zigzag/inputs/mapping/default_imc.yaml"


@pytest.fixture
def accelerator():
    return "zigzag/inputs/hardware/cimp.yaml"


@pytest.mark.parametrize("workload", workloads)
def test_api(workload: str, accelerator: str, mapping: str):  # pylint: disable=W0621
    energy, latency, tclk, area, _ = get_hardware_performance_zigzag_imc(workload, accelerator, mapping)
    print(f"\\n--- CIMP RESULTS for {workload} ---")
    print(f"Energy (pJ): {energy}")
    print(f"Latency (cycles): {latency}")
    print(f"Tclk (ns): {tclk}")
    print(f"Area: {area}")
    
    assert energy > 0
    assert latency > 0
    assert tclk > 0
    assert area == 0  # CIMP area is explicitly set to 0 for now
