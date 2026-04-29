# Graph Report - semron_cimp  (2026-04-29)

## Corpus Check
- 8 files · ~78,221 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 30 nodes · 24 edges · 6 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]

## God Nodes (most connected - your core abstractions)
1. `CIMP_Analyzer` - 5 edges
2. `calculate_Nav_fig10()` - 2 edges
3. `calculate_Etot_Fig14()` - 2 edges
4. `calculate_Nav()` - 2 edges
5. `calculate_energies()` - 2 edges
6. `K_crossover()` - 2 edges
7. `Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw` - 1 edges
8. `Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical` - 1 edges
9. `[CIMP PHYSICS] Calculates the maximum possible Rows (K) before manufacturing var` - 1 edges
10. `Calculates the physics of a specific array configuration.` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.28
Nodes (4): CIMP_Analyzer, Sweeps through the search space to find the best hardware configurations to give, [CIMP PHYSICS] Calculates the maximum possible Rows (K) before manufacturing var, Calculates the physics of a specific array configuration.

### Community 1 - "Community 1"
Cohesion: 0.4
Nodes (3): K_crossover(), Fig. 7 reproduction WITH feasibility shading.  Below each dashed line = infeas, K at which the Sw curve equals threshold_pct. Below this K the     curve is ABO

### Community 2 - "Community 2"
Cohesion: 0.67
Nodes (2): calculate_Nav_fig10(), Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw

### Community 3 - "Community 3"
Cohesion: 0.67
Nodes (2): calculate_Etot_Fig14(), Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical

### Community 4 - "Community 4"
Cohesion: 0.67
Nodes (2): calculate_Nav(), Calculates the Number of Averages (Nav) based on Equation (42)     from Demasiu

### Community 5 - "Community 5"
Cohesion: 0.67
Nodes (2): calculate_energies(), Calculates E_cap and E_tot for a given K and r.     Uses Physical By=10 and Sig

## Knowledge Gaps
- **9 isolated node(s):** `Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw`, `Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical`, `[CIMP PHYSICS] Calculates the maximum possible Rows (K) before manufacturing var`, `Calculates the physics of a specific array configuration.`, `Sweeps through the search space to find the best hardware configurations to give` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 2`** (3 nodes): `calculate_Nav_fig10()`, `Nav_mac_time_10.py`, `Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 3`** (3 nodes): `calculate_Etot_Fig14()`, `Etot_By_Pops.py`, `Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 4`** (3 nodes): `calculate_Nav()`, `Nav_R_K_9.py`, `Calculates the Number of Averages (Nav) based on Equation (42)     from Demasiu`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 5`** (3 nodes): `calculate_energies()`, `Etot_K_Pops.py`, `Calculates E_cap and E_tot for a given K and r.     Uses Physical By=10 and Sig`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Calculates Nav for varying MAC Bitwidths (Sw).     Includes the 'Sw=1 equals Sw`, `Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical`, `[CIMP PHYSICS] Calculates the maximum possible Rows (K) before manufacturing var` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._