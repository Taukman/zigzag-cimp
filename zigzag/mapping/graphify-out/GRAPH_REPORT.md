# Graph Report - mapping  (2026-05-14)

## Corpus Check
- 8 files · ~7,078 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 179 nodes · 295 edges · 12 communities detected
- Extraction: 74% EXTRACTED · 26% INFERRED · 0% AMBIGUOUS · INFERRED: 78 edges (avg confidence: 0.62)
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
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]

## God Nodes (most connected - your core abstractions)
1. `SpatialMappingInternal` - 26 edges
2. `DataMovePattern` - 21 edges
3. `TemporalMapping` - 21 edges
4. `SpatialMapping` - 21 edges
5. `MappingSingleOADim` - 16 edges
6. `Mapping` - 16 edges
7. `DataMoveAttr` - 14 edges
8. `FourWayDataMoving` - 11 edges
9. `SpatialMappingHint` - 8 edges
10. `decouple_pr_loop()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `! Calculate the effective data size for getting the allowed memory updating wind` --uses--> `DataMoveAttr`  [INFERRED]
  mapping.py → data_movement.py
- `! This function calculates the average & instant required memory bw and the peri` --uses--> `DataMoveAttr`  [INFERRED]
  mapping.py → data_movement.py
- `! Calculate the effective data size for getting the allowed memory updating wind` --uses--> `DataMovePattern`  [INFERRED]
  mapping.py → data_movement.py
- `! This function calculates the average & instant required memory bw and the peri` --uses--> `DataMovePattern`  [INFERRED]
  mapping.py → data_movement.py
- `! Calculate the effective data size for getting the allowed memory updating wind` --uses--> `TemporalMapping`  [INFERRED]
  mapping.py → temporal_mapping.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (20): DataMoveAttr, DataMovePattern, Collects the memory access pattern for each unit memory (memory holding one oper, Mapping, ! This function generates an list "psum_flag" that identify whether an output me, ! This function generates a dictionary that collect data precision for each oper, ! Collect information of a complete mapping (spatial and temporal)      NOTE: Ma, ! Given the combined mapping, generate r/ir loop size list at each level for eac (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.1
Nodes (11): all_contained_layer_dims(), ! Return True iff         1) the instance's OA Dimensions have been initialized, ! Verify         - that the utilization at each OADimension does not exceed the, ! Return the total unroll factor of a given Layer Dimension, over all Operationa, ! Return a value that indicates how well this SpatialMapping is expected to perf, ! Convert all unrollings (pair of LayerDim and UnrollFactor) at all OADimension, ! Return true if the contained dimensions are the same and all MappingSingleOADi, ! Spatial unrollings defined for every operational array dimension (+3 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (15): Update a single direction value across all attributes., Update the value of a specific data direction., decouple_pr_loop(), ! This function replaces all pr loops in a mapping of a single operand with r an, ! This function decouples the pr loops into data size (r loops) and data reuse (, # NOTE: Here we insert the ir loop after/above the r loop, which indicates that, replace_pr_loop_in_mapping(), hw_utilization() (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (12): ! Calculate the effective data size for getting the allowed memory updating wind, ! Calculate total/unique/duplicate unit count per operand per architecture level, ! Class that collect all the info related to spatial mapping., ! Calculate data serve scope, i.e., for input operands, it means that each data, ! Calculate memory bandwidth incremental factor between architectural levels., ! Save the loops that were unrolled spatially in a list without any arch level i, # NOTE: data_serve_scope doesn't include MAC level, thus is one level less than, ! JSON representation of this object to save it to a file. (+4 more)

### Community 4 - "Community 4"
Cohesion: 0.1
Nodes (11): FourWayDataMoving, Set a given attribute using a dictionary of DataDirection values., Retrieve a specific attribute., Represents a standard four-way data moving attribute of a memory interface., Initialize with a dictionary containing all four DataDirection values, defaultin, Retrieve the value associated with a specific data direction., Element-wise addition of two FourWayDataMoving instances., Element-wise multiplication by a scalar. (+3 more)

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (3): MappingSingleOADim, ! Spatial unrolling for a single OADimension, ! Return true iff the contained LayerDims are the same and all unrollings are th

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (8): AccessEnergy, MemoryAccesses, Represents the number of memory accesses in four directions., Element-wise addition of two AccessEnergy instances., Element-wise multiplication by a scalar., Represents the memory access energy in four directions., Element-wise addition of two AccessEnergy instances., Element-wise multiplication by a scalar.

### Community 7 - "Community 7"
Cohesion: 0.2
Nodes (6): LayerAttribute, empty(), ! Suggested LayerDims to be unrolled for every OADimension, Check the hints at all contained OADimension. If the OADimension doesn't contain, For all OADimensions in `oa_dim_sizes` that are not already in this SpatialMappi, SpatialMappingHint

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): ! Returns the `hardware utilization`, i.e. the product of all unrolled dimension

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): ! Returns the `hardware utilization`, i.e. the product of all unrolled dimension

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): ! Return a set containing all the LayerDims contained in the mapping at any OA D

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): ! Return a list with all of the MappingSingleOADims contained in this instance.

## Knowledge Gaps
- **53 isolated node(s):** `! This function decouples the pr loops into data size (r loops) and data reuse (`, `! This function replaces all pr loops in a mapping of a single operand with r an`, `# NOTE: Here we insert the ir loop after/above the r loop, which indicates that`, `Represents a standard four-way data moving attribute of a memory interface.`, `Initialize with a dictionary containing all four DataDirection values, defaultin` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 9`** (1 nodes): `! Returns the `hardware utilization`, i.e. the product of all unrolled dimension`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (1 nodes): `! Returns the `hardware utilization`, i.e. the product of all unrolled dimension`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `! Return a set containing all the LayerDims contained in the mapping at any OA D`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `! Return a list with all of the MappingSingleOADims contained in this instance.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SpatialMappingInternal` connect `Community 3` to `Community 0`, `Community 4`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Why does `FourWayDataMoving` connect `Community 4` to `Community 2`, `Community 6`?**
  _High betweenness centrality (0.173) - this node is a cross-community bridge._
- **Why does `SpatialMapping` connect `Community 1` to `Community 2`, `Community 4`, `Community 7`?**
  _High betweenness centrality (0.172) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `SpatialMappingInternal` (e.g. with `Mapping` and `! Collect information of a complete mapping (spatial and temporal)      NOTE: Ma`) actually correct?**
  _`SpatialMappingInternal` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `DataMovePattern` (e.g. with `Mapping` and `! Collect information of a complete mapping (spatial and temporal)      NOTE: Ma`) actually correct?**
  _`DataMovePattern` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `TemporalMapping` (e.g. with `Mapping` and `! Collect information of a complete mapping (spatial and temporal)      NOTE: Ma`) actually correct?**
  _`TemporalMapping` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `! This function decouples the pr loops into data size (r loops) and data reuse (`, `! This function replaces all pr loops in a mapping of a single operand with r an`, `# NOTE: Here we insert the ir loop after/above the r loop, which indicates that` to the rest of the system?**
  _53 weakly-connected nodes found - possible documentation gaps or missing edges._