# Graph Report - zigzag  (2026-04-29)

## Corpus Check
- 146 files · ~161,882 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1606 nodes · 6244 edges · 15 communities detected
- Extraction: 31% EXTRACTED · 69% INFERRED · 0% AMBIGUOUS · INFERRED: 4283 edges (avg confidence: 0.56)
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
- [[_COMMUNITY_Community 24|Community 24]]

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
- `! Converts our bespoke linked list to a python list.` --uses--> `LayerDim`  [INFERRED]
  opt/loma/multipermute.py → datatypes.py
- `! Generator providing all multiset permutations of a multiset with constraints.` --uses--> `LayerDim`  [INFERRED]
  opt/loma/multipermute.py → datatypes.py
- `! Generator providing all multiset permutations of a multiset.` --uses--> `LayerDim`  [INFERRED]
  opt/loma/multipermute.py → datatypes.py
- `! Create a new LayerDim instance with is tagged `relevant` and can be distinguis` --uses--> `AcceleratorValidator`  [INFERRED]
  datatypes.py → parser/accelerator_validator.py
- `! Create a new LayerDim instance with is tagged `irrelevant` and can be distingu` --uses--> `AcceleratorValidator`  [INFERRED]
  datatypes.py → parser/accelerator_validator.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (121): AcceleratorParserStage, parse_accelerator(), ! Parse to parse an accelerator from a user-defined yaml file., Initialize Validator object, assign schema and store normalize user-given data, get_hardware_performance_zigzag(), get_hardware_performance_zigzag_imc(), Overload with type hint, ! ZigZag API: estimates the cost of running the given workload on the given hard (+113 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (92): AcceleratorFactory, MemoryFactory, ! Create MemoryInstances and adds them to memory hierarchy., Create the memory ports for the memory instance., Create a new MemoryInstance and add it to the given MemoryHierarchy, The order of the port allocations matches the order of the MemoryOperands., ! Converts valid user-provided accelerator data into an `Accelerator` instance, ! Generate an `Core` instance from the validated user-provided data. (+84 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (114): Accelerator, ! Class that stores inputs and runs them through the zigzag cost model.      Ini, ! Simple JSON representation used for saving this object to a simple json file., ! Run the cost model evaluation., Calculate the dynamic MAC energy         Overrides superclass' method, !         The latency calculation is largely identical to that of the superclass, DataMovePattern, Collects the memory access pattern for each unit memory (memory holding one oper (+106 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (152): arb_grant(), arb_int(), arb_pri(), arb_req(), Arbiter(), Component(), compute_power(), crossbar_ctrline() (+144 more)

### Community 4 - "Community 4"
Cohesion: 0.04
Nodes (67): calculate_mapped_rows_when_diagonal_mapping_found(), LayerAttribute, ! Abstract Base Class to represent any layer attribute, empty(), extract_pr_loop_info(), LayerDimRelation, LayerDimSizes, LayerEquation (+59 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (96): MemoryUtilization, ! Calculate the amount of cycles and bandwidth that are borrowed from the comput, ! Calculate the number of data onloading/offloading cycles.         This functio, ! This function integrates the previous calculated SScomb, data loading and off-, ! Given a memory level and a memory operand, compute the memory's instantaneous, Given a cost model evaluation and a memory level, compute the memory's total ins, Balance c_list towards minimums m_list with a total maximum reduction of s., ! Simple JSON representation used for saving this object to a simple json file. (+88 more)

### Community 6 - "Community 6"
Cohesion: 0.03
Nodes (59): get_arg_parser(), is_pow2(), logtwo(), cleanup(), find_area(), find_cyc(), find_delay(), find_energy() (+51 more)

### Community 7 - "Community 7"
Cohesion: 0.04
Nodes (58): ConvParser, ! Parser for ONNX Conv and QLinearConv nodes into LayerNode., ! Run the parser and return the created LayerNode object, ! Generate the necessary dictionary items required for the LayerNode creation. I, # IMPORTANT: If any of the input loops require padding, they should be defined a, DefaultNodeParser, ! This class parses an ONNX node into a DummyNode., DummyNode (+50 more)

### Community 8 - "Community 8"
Cohesion: 0.04
Nodes (35): CactiConfig, user_input format can be 1 out of these 3:         user_input = ['default'], run_cacti(), Update a single direction value across all attributes., Initialize with a dictionary containing all four DataDirection values, defaultin, Update the value of a specific data direction., ! Create a new LayerDim instance with is tagged `relevant` and can be distinguis, ! Create a new LayerDim instance with is tagged `irrelevant` and can be distingu (+27 more)

### Community 9 - "Community 9"
Cohesion: 0.05
Nodes (12): ! Run the cost model stage by calling the internal zigzag cost model with the co, __get_shared_mem_list(), CostModelEvaluationForIMC, ! This function calculate the Tclk for IMC (In-Memory-Computing), reduce_balanced(), CostModelEvaluation, Set a given attribute using a dictionary of DataDirection values., Retrieve a specific attribute. (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.06
Nodes (15): AcceleratorValidator, Validates a single Zigzag accelerator from a user-provided yaml file. Checks if, ! Validate the user-provided accelerator data. Log a critical warning when inval, Assumes that the multiplier type is IMC, Assumes that the multiplier type is not IMC, OperandABC, ! Abstract Base Class for all dimension- and operand-like classes, Protect the class variable from reassignment (as this would invalidate the store (+7 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (16): clean_results(), find_all_bobs(), find_all_channels(), find_all_memories(), find_bobs_recursive(), find_mems_recursive(), bob_conf(), bw_index() (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (9): ABC, constrainded_permutations(), init(), ListElement, permutations(), ! Converts our bespoke linked list to a python list., ! Generator providing all multiset permutations of a multiset with constraints., ! Generator providing all multiset permutations of a multiset. (+1 more)

### Community 13 - "Community 13"
Cohesion: 0.67
Nodes (2): frequnecy_index(), IOTechParam()

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Returns the user-provided data after normalization by the validator. (Normalizat

## Knowledge Gaps
- **36 isolated node(s):** `Protect the class variable from reassignment (as this would invalidate the store`, `! (for-loop) dimension of a workload layer (e.g. `K`, `C`)`, `! Store constant objects used throughout ZigZag (instead of hardcoding them)`, `! Hashes the input data using SHA-512`, `! Recursively converts objects into a json representation` (+31 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 13`** (4 nodes): `extio_technology.cc`, `extio_technology.h`, `frequnecy_index()`, `IOTechParam()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Returns the user-provided data after normalization by the validator. (Normalizat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LayerNode` connect `Community 2` to `Community 0`, `Community 1`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `ImcArray` connect `Community 1` to `Community 0`, `Community 2`, `Community 5`, `Community 6`, `Community 9`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `Accelerator` connect `Community 2` to `Community 0`, `Community 1`, `Community 4`, `Community 5`, `Community 7`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 228 inferred relationships involving `LayerNode` (e.g. with `MemoryUtilization` and `CostModelEvaluationABC`) actually correct?**
  _`LayerNode` has 228 INFERRED edges - model-reasoned connections that need verification._
- **Are the 207 inferred relationships involving `LayerDim` (e.g. with `AcceleratorValidator` and `Prints a structured representation of a CostModelEvaluation mapping.      :param`) actually correct?**
  _`LayerDim` has 207 INFERRED edges - model-reasoned connections that need verification._
- **Are the 197 inferred relationships involving `LayerOperand` (e.g. with `AcceleratorValidator` and `PortActivity`) actually correct?**
  _`LayerOperand` has 197 INFERRED edges - model-reasoned connections that need verification._
- **Are the 163 inferred relationships involving `Accelerator` (e.g. with `MemoryUtilization` and `CostModelEvaluationABC`) actually correct?**
  _`Accelerator` has 163 INFERRED edges - model-reasoned connections that need verification._