"""
Fig. 7 reproduction WITH feasibility shading.

Below each dashed line = infeasible with that technology.
Every curve segment sitting BELOW the 0.11% line cannot be manufactured
with immersion lithography alone.

All formulas from [11]:
  Eq. (32):  sigma_C,pgr / (Cmax - Cmin) = 1 / (6 * sqrt(K) * (2^(Sw-1) - 1))
  Refs:   0.71%  = dry DUV         (Eq. 27 [11])
          0.11%  = immersion lith. (Sec. IV-A [11])
          0.062% = SONOS prog.     (Eq. 31 [11])
"""

import numpy as np
import matplotlib.pyplot as plt

def sigma_required_pct(K, Sw):
    Sw_eff = 2 if Sw == 1 else Sw              # Fig. 7 caption [11]
    return 100.0 / (6.0 * np.sqrt(K) * (2**(Sw_eff - 1) - 1))

def K_crossover(threshold_pct, Sw):
    """K at which the Sw curve equals threshold_pct. Below this K the
    curve is ABOVE the line (feasible); above this K it's BELOW (infeasible)."""
    Sw_eff = 2 if Sw == 1 else Sw
    return (100.0 / (threshold_pct * 6.0 * (2**(Sw_eff - 1) - 1)))**2

DRY_DUV, IMMERSION, SONOS = 0.71, 0.11, 0.062

K_axis  = np.arange(128, 8192 + 1, 32)
Sw_list = [1, 2, 3, 4, 5, 6]

fig, ax = plt.subplots(figsize=(9, 6))
cmap   = plt.cm.viridis
colors = [cmap(i / (len(Sw_list) - 1)) for i in range(len(Sw_list))]

# Shade the three infeasibility zones (below each dashed line)
ax.axhspan(0.01,       SONOS,     facecolor='red',    alpha=0.06)
ax.axhspan(SONOS,      IMMERSION, facecolor='orange', alpha=0.06)
ax.axhspan(IMMERSION,  DRY_DUV,   facecolor='yellow', alpha=0.06)

# Sw curves + mark immersion-feasibility crossover
for Sw, c in zip(Sw_list, colors):
    y = np.array([sigma_required_pct(K, Sw) for K in K_axis])
    ax.plot(K_axis, y, color=c, lw=2, label=f'$S_w={Sw}$')

    Kcross = K_crossover(IMMERSION, Sw)
    if 128 <= Kcross <= 8192:
        ax.plot(Kcross, IMMERSION, 'o', color=c, ms=9, mec='black', mew=1)
        ax.annotate(f'$S_w={Sw}$\n  max $K\\!\\approx${int(Kcross)}',
                    xy=(Kcross, IMMERSION),
                    xytext=(Kcross + 200, IMMERSION * 2.0),
                    fontsize=9, color=c,
                    arrowprops=dict(arrowstyle='->', color=c, lw=1))
    elif Kcross < 128:
        # Curve already below immersion at K=128 -> infeasible everywhere
        ax.annotate(f'$S_w={Sw}$: infeasible\n  for all $K\\geq 128$',
                    xy=(180, sigma_required_pct(180, Sw)),
                    xytext=(1500, sigma_required_pct(180, Sw) * 0.55),
                    fontsize=9, color=c,
                    arrowprops=dict(arrowstyle='->', color=c, lw=1))

# Reference dashed lines (from paper [11])
ax.axhline(DRY_DUV,   color='black', ls='--', lw=1.2)
ax.axhline(IMMERSION, color='black', ls='--', lw=1.2)
ax.axhline(SONOS,     color='black', ls='--', lw=1.2)
ax.text(6400, DRY_DUV   * 1.10, 'dry DUV lith.',        fontsize=9)
ax.text(6400, IMMERSION * 1.10, 'immersion lith.',      fontsize=9)
ax.text(6400, SONOS     * 1.10, 'SONOS prog. accuracy', fontsize=9)

ax.set_yscale('log')
ax.set_xlim(0, 8192)
ax.set_ylim(0.015, 3)
ax.set_xlabel('Column Length  $K$', fontsize=12)
ax.set_ylabel(r'$\sigma_{C,\mathrm{pgr}}/(C_{\max}-C_{\min})$ (%)', fontsize=12)
ax.grid(True, which='both', alpha=0.3)
ax.legend(title='$S_w=$', loc='lower left', fontsize=10, ncol=2)
ax.set_title('Fig. 7 reproduction with feasibility zones\n'
             'shaded = infeasible for that technology',
             fontsize=10)

plt.tight_layout()
plt.savefig('figures/figure7_feasibility.png', dpi=300)
#plt.show()
