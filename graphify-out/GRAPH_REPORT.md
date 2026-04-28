# Graph Report - zigzag  (2026-04-27)

## Corpus Check
- 189 files · ~354,123 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1678 nodes · 5971 edges · 28 communities detected
- Extraction: 34% EXTRACTED · 66% INFERRED · 0% AMBIGUOUS · INFERRED: 3949 edges (avg confidence: 0.56)
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
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 46|Community 46]]

## God Nodes (most connected - your core abstractions)
1. `LayerNode` - 230 edges
2. `LayerDim` - 209 edges
3. `LayerOperand` - 190 edges
4. `Accelerator` - 175 edges
5. `MemoryOperand` - 127 edges
6. `SpatialMappingInternal` - 121 edges
7. `StageCallable` - 109 edges
8. `Stage` - 107 edges
9. `Constants` - 105 edges
10. `OADimension` - 99 edges

## Surprising Connections (you probably didn't know these)
- `make_capram()` --calls--> `parse_accelerator()`  [INFERRED]
  capram/extended_analysis.py → zigzag/stages/parser/accelerator_parser.py
- `Extended CapRAM Analysis ========================= Now that we've reproduced 29,` --uses--> `AcceleratorParserStage`  [INFERRED]
  capram/extended_analysis.py → zigzag/stages/parser/accelerator_parser.py
- `Test CapRAM extension — reproduce SEMRON's 29,600 TOPS/W =======================` --uses--> `AcceleratorParserStage`  [INFERRED]
  capram/test_capram.py → zigzag/stages/parser/accelerator_parser.py
- `CapRAM Extension for ZigZag — CORRECTED VERSION ================================` --uses--> `ImcArray`  [INFERRED]
  capram/capram_array.py → zigzag/hardware/architecture/imc_array.py
- `CapRAM IMC array using Paper 1's SPICE-calibrated energies.` --uses--> `ImcArray`  [INFERRED]
  capram/capram_array.py → zigzag/hardware/architecture/imc_array.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.03
Nodes (183): Accelerator, ! Class that stores inputs and runs them through the zigzag cost model.      Ini, ! Simple JSON representation used for saving this object to a simple json file., ! Run the cost model evaluation., Calculate the dynamic MAC energy         Overrides superclass' method, !  Calculate latency in 4 steps          1) As we already calculated the ideal d, MemoryUtilization, ! Calculate the amount of cycles and bandwidth that are borrowed from the comput (+175 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (102): AcceleratorFactory, MemoryFactory, ! Create MemoryInstances and adds them to memory hierarchy., Create a new MemoryInstance and add it to the given MemoryHierarchy, The order of the port allocations matches the order of the MemoryOperands., ! Converts valid user-provided accelerator data into an `Accelerator` instance, ! Generate an `Core` instance from the validated user-provided data., ! Create a Core instance from the user-provided data.         NOTE the memory in (+94 more)

### Community 2 - "Community 2"
Cohesion: 0.03
Nodes (103): AcceleratorParserStage, ! Parse to parse an accelerator from a user-defined yaml file., get_hardware_performance_zigzag(), get_hardware_performance_zigzag_imc(), Overload with type hint, ! ZigZag API: estimates the cost of running the given workload on the given hard, CostModelEvaluation, CostModelEvaluationABC (+95 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (150): arb_grant(), arb_int(), arb_pri(), arb_req(), Arbiter(), Component(), compute_power(), crossbar_ctrline() (+142 more)

### Community 4 - "Community 4"
Cohesion: 0.03
Nodes (54): CactiConfig, user_input format can be 1 out of these 3:         user_input = ['default'], CapRamArray, CapRAM Extension for ZigZag — CORRECTED VERSION ================================, Override: use Paper 1's SPICE-calibrated per-cell energies., Override with SEMRON's pulse-count encoding (142 periods per MVM).          KEY, CapRAM IMC array using Paper 1's SPICE-calibrated energies., Clock period depends on array size (Paper 1 Table 1 interpolation). (+46 more)

### Community 5 - "Community 5"
Cohesion: 0.03
Nodes (51): ABC, ! Format used in the original ZigZag version, ! Return the total amount of times this memory interface is read from to the lev, ! Return the total amount of times this memory interface is read from to the lev, ! Return the total amount of times this memory interface is written to from the, ! Return the total amount of times this memory interface is written to from the, DiGraph, !         @return (self): Directed Graph with nodes the layers and edges the con (+43 more)

### Community 6 - "Community 6"
Cohesion: 0.04
Nodes (48): ConvParser, ! Parser for ONNX Conv and QLinearConv nodes into LayerNode., ! Run the parser and return the created LayerNode object, ! Generate the necessary dictionary items required for the LayerNode creation. I, # IMPORTANT: If any of the input loops require padding, they should be defined a, DefaultNodeParser, ! This class parses an ONNX node into a DummyNode., Enum (+40 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (50): get_arg_parser(), is_pow2(), logtwo(), cleanup(), find_area(), find_cyc(), find_delay(), find_energy() (+42 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (27): parse_accelerator(), Initialize Validator object, assign schema and store normalize user-given data, DNNWorkload, Return a copy. DNNWorkloads don't contain DummyNodes in the first place., Extends the ABC for workloads. For user-defined workloads (from yaml), the Dummy, MappingValidator, Class to validate user-given mappings from yaml file, ! Validate the user-provided accelerator data. Log a critical warning when inval (+19 more)

### Community 9 - "Community 9"
Cohesion: 0.07
Nodes (17): LomaEngine, =====================================================================   Title:, ! Get all loops that have to be temporally scheduled given layer and spatial map, ! Class that handles optimization of temporal mapping given a:     - layer     -, ! Initialize the engine with the given:         - LayerNode         - SpatialMap, ! Call the necessary methods, start the processes and collect the best temporal, ! Run a simulated annealing optimization on the loop ordering using a loma memor, SalsaEngine (+9 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (15): AcceleratorValidator, Validates a single Zigzag accelerator from a user-provided yaml file. Checks if, ! Validate the user-provided accelerator data. Log a critical warning when inval, Assumes that the multiplier type is IMC, Assumes that the multiplier type is not IMC, OperandABC, ! Abstract Base Class for all dimension- and operand-like classes, Protect the class variable from reassignment (as this would invalidate the store (+7 more)

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (13): CactiParser, !  Class that provides the interface between ZigZag and CACTI., ! This functions checks first if the memory with the provided parameters was alr, ! This function checks whether the provided memory configuration was already use, ! This function simulates a new item by calling CACTI7 based on the provided par, ! Update the memory size of this instance., ! JSON Representation of this class to save it to a json file., Wether using this instance will result in the same estimations as using the othe (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (16): clean_results(), find_all_bobs(), find_all_channels(), find_all_memories(), find_bobs_recursive(), find_mems_recursive(), bob_conf(), bw_index() (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.28
Nodes (4): CIMP_Analyzer, Sweeps through the search space to find the best hardware configurations to give, [CIMP PHYSICS] Calculates the maximum possible Rows (K) before manufacturing var, Calculates the physics of a specific array configuration.

### Community 14 - "Community 14"
Cohesion: 0.6
Nodes (3): accelerator(), mapping(), test_api()

### Community 15 - "Community 15"
Cohesion: 0.6
Nodes (3): accelerator(), mapping(), test_api()

### Community 16 - "Community 16"
Cohesion: 0.6
Nodes (3): accelerator(), mapping(), test_api()

### Community 17 - "Community 17"
Cohesion: 0.6
Nodes (3): accelerator(), mapping(), test_api()

### Community 18 - "Community 18"
Cohesion: 0.6
Nodes (3): accelerator(), mapping(), test_api()

### Community 19 - "Community 19"
Cohesion: 0.33
Nodes (2): Bank(), Component()

### Community 20 - "Community 20"
Cohesion: 0.4
Nodes (3): K_crossover(), Fig. 7 reproduction WITH feasibility shading.  Below each dashed line = infeas, K at which the Sw curve equals threshold_pct. Below this K the     curve is ABO

### Community 21 - "Community 21"
Cohesion: 0.67
Nodes (2): frequnecy_index(), IOTechParam()

### Community 22 - "Community 22"
Cohesion: 0.67
Nodes (2): calculate_Nav_fig10(), Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw

### Community 23 - "Community 23"
Cohesion: 0.67
Nodes (2): calculate_Etot_Fig14(), Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical

### Community 24 - "Community 24"
Cohesion: 0.67
Nodes (2): calculate_Nav(), Calculates the Number of Averages (Nav) based on Equation (42)     from Demasiu

### Community 25 - "Community 25"
Cohesion: 0.67
Nodes (2): calculate_energies(), Calculates E_cap and E_tot for a given K and r.     Uses Physical By=10 and Sig

### Community 26 - "Community 26"
Cohesion: 0.67
Nodes (1): CapRAM Energy Model — Reproducing SEMRON's 29,600 TOPS/W =======================

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): Returns the user-provided data after normalization by the validator. (Normalizat

## Knowledge Gaps
- **45 isolated node(s):** `Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw`, `Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical`, `[CIMP PHYSICS] Calculates the maximum possible Rows (K) before manufacturing var`, `Calculates the physics of a specific array configuration.`, `Sweeps through the search space to find the best hardware configurations to give` (+40 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 19`** (6 nodes): `Bank()`, `Component()`, `compute_delays()`, `compute_power_energy()`, `bank.cc`, `bank.h`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (4 nodes): `frequnecy_index()`, `IOTechParam()`, `extio_technology.cc`, `extio_technology.h`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (3 nodes): `calculate_Nav_fig10()`, `Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw`, `Nav_mac_time_10.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (3 nodes): `calculate_Etot_Fig14()`, `Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical`, `Etot_By_Pops.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (3 nodes): `calculate_Nav()`, `Calculates the Number of Averages (Nav) based on Equation (42)     from Demasiu`, `Nav_R_K_9.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (3 nodes): `calculate_energies()`, `Calculates E_cap and E_tot for a given K and r.     Uses Physical By=10 and Sig`, `Etot_K_Pops.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (3 nodes): `semron_energy_model.py`, `CapRAM Energy Model — Reproducing SEMRON's 29,600 TOPS/W =======================`, `semron_energy_model.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `Returns the user-provided data after normalization by the validator. (Normalizat`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LayerNode` connect `Community 0` to `Community 1`, `Community 2`, `Community 4`, `Community 5`, `Community 6`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `ImcArray` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 11`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `cacti_interface()` connect `Community 7` to `Community 3`, `Community 12`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 213 inferred relationships involving `LayerNode` (e.g. with `MemoryUtilization` and `CostModelEvaluationABC`) actually correct?**
  _`LayerNode` has 213 INFERRED edges - model-reasoned connections that need verification._
- **Are the 203 inferred relationships involving `LayerDim` (e.g. with `AcceleratorValidator` and `# TODO documentation, split this up into multiple, sensible functions`) actually correct?**
  _`LayerDim` has 203 INFERRED edges - model-reasoned connections that need verification._
- **Are the 185 inferred relationships involving `LayerOperand` (e.g. with `AcceleratorValidator` and `PortActivity`) actually correct?**
  _`LayerOperand` has 185 INFERRED edges - model-reasoned connections that need verification._
- **Are the 159 inferred relationships involving `Accelerator` (e.g. with `MemoryUtilization` and `CostModelEvaluationABC`) actually correct?**
  _`Accelerator` has 159 INFERRED edges - model-reasoned connections that need verification._