# Graph Report - zigzag  (2026-05-01)

## Corpus Check
- 187 files · ~542,071 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1790 nodes · 6949 edges · 29 communities detected
- Extraction: 30% EXTRACTED · 70% INFERRED · 0% AMBIGUOUS · INFERRED: 4894 edges (avg confidence: 0.55)
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
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]

## God Nodes (most connected - your core abstractions)
1. `LayerNode` - 311 edges
2. `LayerDim` - 267 edges
3. `LayerOperand` - 248 edges
4. `Accelerator` - 194 edges
5. `OADimension` - 176 edges
6. `MemoryOperand` - 141 edges
7. `MappingSingleOADim` - 139 edges
8. `Mapping` - 136 edges
9. `StageCallable` - 126 edges
10. `Stage` - 124 edges

## Surprising Connections (you probably didn't know these)
- `test_api()` --calls--> `get_hardware_performance_zigzag()`  [INFERRED]
  tests/main/test_parserless_apitest_ascend_like.py → zigzag/api.py
- `test_api()` --calls--> `get_hardware_performance_zigzag_imc()`  [INFERRED]
  tests/main/test_imc/test_dimc.py → zigzag/api.py
- `test_api()` --calls--> `get_hardware_performance_zigzag_imc()`  [INFERRED]
  tests/main/test_imc/test_aimc.py → zigzag/api.py
- `test_api()` --calls--> `get_hardware_performance_zigzag_imc()`  [INFERRED]
  tests/main/test_imc/test_cimp.py → zigzag/api.py
- `test_api()` --calls--> `get_hardware_performance_zigzag()`  [INFERRED]
  tests/main/test_origin/test_gemm_l1_l3.py → zigzag/api.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.04
Nodes (120): Accelerator, ! Run the cost model stage by calling the internal zigzag cost model with the co, CostModelEvaluationForIMC, ! This function calculate the Tclk for IMC (In-Memory-Computing), ! Class that stores inputs and runs them through the zigzag cost model.      Ini, ! Simple JSON representation used for saving this object to a simple json file., ! Run the cost model evaluation., Calculate the dynamic MAC energy         Overrides superclass' method (+112 more)

### Community 1 - "Community 1"
Cohesion: 0.02
Nodes (118): AcceleratorParserStage, ! Parse to parse an accelerator from a user-defined yaml file., Overload with type hint, ! ZigZag API: estimates the cost of running the given workload on the given hard, CostModelEvaluation, CostModelEvaluationABC, CumulativeCME, CostModelStage (+110 more)

### Community 2 - "Community 2"
Cohesion: 0.03
Nodes (103): AcceleratorFactory, MemoryFactory, ! Create MemoryInstances and adds them to memory hierarchy., ! Create MemoryInstances and adds them to memory hierarchy., ! Create MemoryInstances and adds them to memory hierarchy., Create the memory ports for the memory instance., Create the memory ports for the memory instance., Create the memory ports for the memory instance. (+95 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (155): arb_grant(), arb_int(), arb_pri(), arb_req(), Arbiter(), Component(), compute_power(), crossbar_ctrline() (+147 more)

### Community 4 - "Community 4"
Cohesion: 0.04
Nodes (147): LayerDim, LayerOperand, OADimension, ! (for-loop) dimension of a workload layer (e.g. `K`, `C`), ! get area of IMC macros (cells, mults, adders, adders_pv, accumulators. Exclude, ! get area of IMC macros (cells, mults, adders, adders_pv, accumulators. Exclude, ! get area of IMC macros (cells, mults, adders, adders_pv, accumulators. Exclude, single DAC cost calculation (+139 more)

### Community 5 - "Community 5"
Cohesion: 0.04
Nodes (77): ABC, LayerAttribute, ! Abstract Base Class to represent any layer attribute, empty(), extract_pr_loop_info(), LayerDimRelation, LayerDimSizes, LayerEquation (+69 more)

### Community 6 - "Community 6"
Cohesion: 0.02
Nodes (44): CactiConfig, user_input format can be 1 out of these 3:         user_input = ['default'], run_cacti(), Update a single direction value across all attributes., Initialize with a dictionary containing all four DataDirection values, defaultin, Update the value of a specific data direction., ! Create a new LayerDim instance with is tagged `relevant` and can be distinguis, ! Create a new LayerDim instance with is tagged `irrelevant` and can be distingu (+36 more)

### Community 7 - "Community 7"
Cohesion: 0.03
Nodes (58): ConvParser, ! Parser for ONNX Conv and QLinearConv nodes into LayerNode., ! Run the parser and return the created LayerNode object, ! Generate the necessary dictionary items required for the LayerNode creation. I, # IMPORTANT: If any of the input loops require padding, they should be defined a, DefaultNodeParser, ! This class parses an ONNX node into a DummyNode., DummyNode (+50 more)

### Community 8 - "Community 8"
Cohesion: 0.03
Nodes (33): parse_accelerator(), AcceleratorValidator, Validates a single Zigzag accelerator from a user-provided yaml file. Checks if, Initialize Validator object, assign schema and store normalize user-given data, ! Validate the user-provided accelerator data. Log a critical warning when inval, Assumes that the multiplier type is IMC, Returns the user-provided data after normalization by the validator. (Normalizat, OperandABC (+25 more)

### Community 9 - "Community 9"
Cohesion: 0.05
Nodes (48): get_arg_parser(), is_pow2(), logtwo(), cleanup(), find_area(), find_cyc(), find_delay(), find_energy() (+40 more)

### Community 10 - "Community 10"
Cohesion: 0.05
Nodes (22): get_hardware_performance_zigzag(), get_hardware_performance_zigzag_imc(), test_api(), accelerator(), mapping(), test_api(), test_api(), test_api() (+14 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (16): clean_results(), find_all_bobs(), find_all_channels(), find_all_memories(), find_bobs_recursive(), find_mems_recursive(), bob_conf(), bw_index() (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.28
Nodes (4): CIMP_Analyzer, Sweeps through the search space to find the best hardware configurations to give, [CIMP PHYSICS] Calculates the maximum possible Rows (K) before manufacturing var, Calculates the physics of a specific array configuration.

### Community 13 - "Community 13"
Cohesion: 0.4
Nodes (3): K_crossover(), Fig. 7 reproduction WITH feasibility shading.  Below each dashed line = infeas, K at which the Sw curve equals threshold_pct. Below this K the     curve is ABO

### Community 15 - "Community 15"
Cohesion: 0.67
Nodes (2): frequnecy_index(), IOTechParam()

### Community 16 - "Community 16"
Cohesion: 0.67
Nodes (2): calculate_Nav_fig10(), Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw

### Community 17 - "Community 17"
Cohesion: 0.67
Nodes (2): calculate_Etot_Fig14(), Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical

### Community 18 - "Community 18"
Cohesion: 0.67
Nodes (2): calculate_Nav(), Calculates the Number of Averages (Nav) based on Equation (42)     from Demasiu

### Community 19 - "Community 19"
Cohesion: 0.67
Nodes (2): calculate_energies(), Calculates E_cap and E_tot for a given K and r.     Uses Physical By=10 and Sig

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (1): Returns the user-provided data after normalization by the validator. (Normalizat

### Community 59 - "Community 59"
Cohesion: 1.0
Nodes (1): Initialize Validator object, assign schema and store normalize user-given data

### Community 60 - "Community 60"
Cohesion: 1.0
Nodes (1): ! Validate the user-provided accelerator data. Log a critical warning when inval

### Community 61 - "Community 61"
Cohesion: 1.0
Nodes (1): Assumes that the multiplier type is IMC

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (1): Assumes that the multiplier type is not IMC

### Community 63 - "Community 63"
Cohesion: 1.0
Nodes (1): Returns the user-provided data after normalization by the validator. (Normalizat

### Community 64 - "Community 64"
Cohesion: 1.0
Nodes (1): Initialize Validator object, assign schema and store normalize user-given data

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (1): ! Validate the user-provided accelerator data. Log a critical warning when inval

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (1): Assumes that the multiplier type is IMC

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (1): Assumes that the multiplier type is not IMC

## Knowledge Gaps
- **54 isolated node(s):** `Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw`, `Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical`, `[CIMP PHYSICS] Calculates the maximum possible Rows (K) before manufacturing var`, `Calculates the physics of a specific array configuration.`, `Sweeps through the search space to find the best hardware configurations to give` (+49 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 15`** (4 nodes): `frequnecy_index()`, `IOTechParam()`, `extio_technology.cc`, `extio_technology.h`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (3 nodes): `calculate_Nav_fig10()`, `Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw`, `Nav_mac_time_10.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (3 nodes): `calculate_Etot_Fig14()`, `Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical`, `Etot_By_Pops.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (3 nodes): `calculate_Nav()`, `Calculates the Number of Averages (Nav) based on Equation (42)     from Demasiu`, `Nav_R_K_9.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (3 nodes): `calculate_energies()`, `Calculates E_cap and E_tot for a given K and r.     Uses Physical By=10 and Sig`, `Etot_K_Pops.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `Returns the user-provided data after normalization by the validator. (Normalizat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (1 nodes): `Initialize Validator object, assign schema and store normalize user-given data`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (1 nodes): `! Validate the user-provided accelerator data. Log a critical warning when inval`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (1 nodes): `Assumes that the multiplier type is IMC`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (1 nodes): `Assumes that the multiplier type is not IMC`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (1 nodes): `Returns the user-provided data after normalization by the validator. (Normalizat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (1 nodes): `Initialize Validator object, assign schema and store normalize user-given data`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (1 nodes): `! Validate the user-provided accelerator data. Log a critical warning when inval`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (1 nodes): `Assumes that the multiplier type is IMC`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (1 nodes): `Assumes that the multiplier type is not IMC`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LayerNode` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Why does `ImcArray` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `Accelerator` connect `Community 0` to `Community 1`, `Community 2`, `Community 4`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 294 inferred relationships involving `LayerNode` (e.g. with `MemoryUtilization` and `CostModelEvaluationABC`) actually correct?**
  _`LayerNode` has 294 INFERRED edges - model-reasoned connections that need verification._
- **Are the 261 inferred relationships involving `LayerDim` (e.g. with `AcceleratorValidator` and `Prints a structured representation of a CostModelEvaluation mapping.      :param`) actually correct?**
  _`LayerDim` has 261 INFERRED edges - model-reasoned connections that need verification._
- **Are the 243 inferred relationships involving `LayerOperand` (e.g. with `AcceleratorValidator` and `PortActivity`) actually correct?**
  _`LayerOperand` has 243 INFERRED edges - model-reasoned connections that need verification._
- **Are the 178 inferred relationships involving `Accelerator` (e.g. with `MemoryUtilization` and `CostModelEvaluationABC`) actually correct?**
  _`Accelerator` has 178 INFERRED edges - model-reasoned connections that need verification._