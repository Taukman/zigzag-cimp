# Graph Report - zigzag  (2026-04-29)

## Corpus Check
- 171 files · ~208,244 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1661 nodes · 6315 edges · 21 communities detected
- Extraction: 32% EXTRACTED · 68% INFERRED · 0% AMBIGUOUS · INFERRED: 4294 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 35|Community 35]]

## God Nodes (most connected - your core abstractions)
1. `LayerNode` - 245 edges
2. `LayerDim` - 213 edges
3. `LayerOperand` - 202 edges
4. `Accelerator` - 179 edges
5. `MemoryOperand` - 133 edges
6. `SpatialMappingInternal` - 124 edges
7. `StageCallable` - 119 edges
8. `Stage` - 117 edges
9. `Constants` - 107 edges
10. `OADimension` - 102 edges

## Surprising Connections (you probably didn't know these)
- `test_api()` --calls--> `get_hardware_performance_zigzag()`  [INFERRED]
  tests/main/test_parserless_apitest_ascend_like.py → zigzag/api.py
- `test_api()` --calls--> `get_hardware_performance_zigzag_imc()`  [INFERRED]
  tests/main/test_imc/test_dimc.py → zigzag/api.py
- `test_api()` --calls--> `get_hardware_performance_zigzag_imc()`  [INFERRED]
  tests/main/test_imc/test_aimc.py → zigzag/api.py
- `test_api()` --calls--> `get_hardware_performance_zigzag()`  [INFERRED]
  tests/main/test_origin/test_gemm_l1_l3.py → zigzag/api.py
- `test_api()` --calls--> `get_hardware_performance_zigzag()`  [INFERRED]
  tests/main/test_origin/test_gemm_l1.py → zigzag/api.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (174): AcceleratorFactory, MemoryFactory, ! Create MemoryInstances and adds them to memory hierarchy., Create the memory ports for the memory instance., Create a new MemoryInstance and add it to the given MemoryHierarchy, The order of the port allocations matches the order of the MemoryOperands., ! Converts valid user-provided accelerator data into an `Accelerator` instance, ! Generate an `Core` instance from the validated user-provided data. (+166 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (127): ABC, Set a given attribute using a dictionary of DataDirection values., Element-wise addition of two FourWayDataMoving instances., Element-wise multiplication by a scalar., JSON-friendly representation., Represents the number of memory accesses in four directions., Represents the memory access energy in four directions., Element-wise multiplication by a scalar. (+119 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (121): Accelerator, CostModelStage, !  Pipeline stage that calls a cost model to evaluate a mapping on a HW config., ! Run the cost model stage by calling the internal zigzag cost model with the co, CostModelEvaluationForIMC, ! Class that stores inputs and runs them through the zigzag cost model.      Ini, ! Simple JSON representation used for saving this object to a simple json file., ! Run the cost model evaluation. (+113 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (153): arb_grant(), arb_int(), arb_pri(), arb_req(), Arbiter(), Component(), compute_power(), crossbar_ctrline() (+145 more)

### Community 4 - "Community 4"
Cohesion: 0.02
Nodes (42): CactiConfig, user_input format can be 1 out of these 3:         user_input = ['default'], run_cacti(), Update a single direction value across all attributes., Update the value of a specific data direction., DiGraph, !         @return (self): Directed Graph with nodes the layers and edges the con, CactiConfig (+34 more)

### Community 5 - "Community 5"
Cohesion: 0.03
Nodes (63): ConvParser, ! Parser for ONNX Conv and QLinearConv nodes into LayerNode., ! Run the parser and return the created LayerNode object, ! Generate the necessary dictionary items required for the LayerNode creation. I, # IMPORTANT: If any of the input loops require padding, they should be defined a, DefaultNodeParser, ! This class parses an ONNX node into a DummyNode., DummyNode (+55 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (22): CactiParser, !  Class that provides the interface between ZigZag and CACTI., ! This functions checks first if the memory with the provided parameters was alr, ! This function checks whether the provided memory configuration was already use, ! This function simulates a new item by calling CACTI7 based on the provided par, CostModelEvaluation, __get_shared_mem_list(), ! This function calculate the Tclk for IMC (In-Memory-Computing) (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (49): get_arg_parser(), logtwo(), cleanup(), find_area(), find_cyc(), find_delay(), find_energy(), uca_org_t() (+41 more)

### Community 8 - "Community 8"
Cohesion: 0.05
Nodes (28): parse_accelerator(), DNNWorkload, Return a copy. DNNWorkloads don't contain DummyNodes in the first place., Extends the ABC for workloads. For user-defined workloads (from yaml), the Dummy, MappingValidator, Class to validate user-given mappings from yaml file, ! Validate the user-provided accelerator data. Log a critical warning when inval, # TODO check that there are no OADimensions that are not defined in the architec (+20 more)

### Community 9 - "Community 9"
Cohesion: 0.06
Nodes (21): get_hardware_performance_zigzag(), get_hardware_performance_zigzag_imc(), test_api(), accelerator(), mapping(), test_api(), test_api(), accelerator() (+13 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (23): ImcArray, ! get area of IMC macros (cells, mults, adders, adders_pv, accumulators. Exclude, definition of an Analog/Digital In-SRAM-Computing (A/DIMC) core     constraint:, ! get clock cycle time of imc macros (worst path: dacs -> mults -> adcs -> adder, ! macro-level one-cycle energy of imc arrays (fully utilization, no weight updat, ! macro-level peak performance of imc arrays (fully utilization, no weight updat, single ADC and analog accumulation cost calculation, single DAC cost calculation (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.06
Nodes (19): AcceleratorValidator, Validates a single Zigzag accelerator from a user-provided yaml file. Checks if, Initialize Validator object, assign schema and store normalize user-given data, ! Validate the user-provided accelerator data. Log a critical warning when inval, Assumes that the multiplier type is IMC, Assumes that the multiplier type is not IMC, OperandABC, ! Abstract Base Class for all dimension- and operand-like classes (+11 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (16): clean_results(), find_all_bobs(), find_all_channels(), find_all_memories(), find_bobs_recursive(), find_mems_recursive(), bob_conf(), bw_index() (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.15
Nodes (3): ! JSON Representation of this class to save it to a json file., json_repr_handler(), ! Recursively converts objects into a json representation

### Community 14 - "Community 14"
Cohesion: 0.67
Nodes (2): frequnecy_index(), IOTechParam()

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): @param real_cycle Within each period, the actual number of cycles used for trans

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): Readable string representation of the class.

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Element-wise addition of two AccessEnergy instances.

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Element-wise addition of two AccessEnergy instances.

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Element-wise multiplication by a scalar.

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Returns the user-provided data after normalization by the validator. (Normalizat

## Knowledge Gaps
- **36 isolated node(s):** `Protect the class variable from reassignment (as this would invalidate the store`, `! (for-loop) dimension of a workload layer (e.g. `K`, `C`)`, `! Store constant objects used throughout ZigZag (instead of hardcoding them)`, `! Hashes the input data using SHA-512`, `! Recursively converts objects into a json representation` (+31 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 14`** (4 nodes): `frequnecy_index()`, `IOTechParam()`, `extio_technology.cc`, `extio_technology.h`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (2 nodes): `.__init__()`, `@param real_cycle Within each period, the actual number of cycles used for trans`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (2 nodes): `.__repr__()`, `Readable string representation of the class.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (2 nodes): `.__add__()`, `Element-wise addition of two AccessEnergy instances.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (2 nodes): `.__add__()`, `Element-wise addition of two AccessEnergy instances.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (2 nodes): `.__mul__()`, `Element-wise multiplication by a scalar.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Returns the user-provided data after normalization by the validator. (Normalizat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LayerNode` connect `Community 2` to `Community 0`, `Community 1`, `Community 4`, `Community 5`, `Community 6`, `Community 8`, `Community 10`, `Community 13`?**
  _High betweenness centrality (0.150) - this node is a cross-community bridge._
- **Why does `ImcArray` connect `Community 10` to `Community 0`, `Community 2`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `LayerOperand` connect `Community 1` to `Community 0`, `Community 2`, `Community 4`, `Community 6`, `Community 8`, `Community 10`, `Community 11`, `Community 16`, `Community 18`, `Community 19`, `Community 20`, `Community 21`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 228 inferred relationships involving `LayerNode` (e.g. with `MemoryUtilization` and `CostModelEvaluationABC`) actually correct?**
  _`LayerNode` has 228 INFERRED edges - model-reasoned connections that need verification._
- **Are the 207 inferred relationships involving `LayerDim` (e.g. with `AcceleratorValidator` and `Prints a structured representation of a CostModelEvaluation mapping.      :param`) actually correct?**
  _`LayerDim` has 207 INFERRED edges - model-reasoned connections that need verification._
- **Are the 197 inferred relationships involving `LayerOperand` (e.g. with `AcceleratorValidator` and `PortActivity`) actually correct?**
  _`LayerOperand` has 197 INFERRED edges - model-reasoned connections that need verification._
- **Are the 163 inferred relationships involving `Accelerator` (e.g. with `MemoryUtilization` and `CostModelEvaluationABC`) actually correct?**
  _`Accelerator` has 163 INFERRED edges - model-reasoned connections that need verification._