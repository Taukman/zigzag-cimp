import math
import numpy as np
import matplotlib.pyplot as plt

def calculate_Etot_Fig14(By_sig, r):
    """
    Calculates Etot for a fixed K=8192 array, dynamically adjusting the physical
    array size (+2 bits of headroom) and ADC energy as the signal resolution drops.
    """
    # 1. Physical Constants
    K = 8192
    Cmax, Vin, Sw, Sx, T = 1e-15, 0.4, 4, 1, 330
    kT = 1.380649e-23 * T
    
    # 2. Dual By Logic
    # The physical array maintains 2 bits of headroom above the signal
    By_phys = By_sig + 2
    
    # 3. Nav Calculation (Physical constraints)
    Cmin = Cmax / r
    Cpar = K * Cmin
    Ncap = (2**By_phys) / ((2**Sw) * (2**Sx))
    Ctot = (K * Cmin) + Cpar + (Ncap * Cmax)
    
    term1_nav = 36 * kT * Ctot
    term2_nav = ((2**(Sw - 1) - 1)**2) * ((2**Sx - 1)**2)
    term3_nav = ((Cmax - Cmin)**2) * (Vin**2)
    Nav = max((term1_nav * term2_nav) / term3_nav, 1.0)
    
    # 4. Ecap Calculation (Signal constraints)
    Q_LSB = ((Cmax - Cmin) / (2**(Sw - 1) - 1)) * (Vin / (2**Sx - 1))
    energy_signal = (8 * Nav * Q_LSB * Vin * (2**By_sig)) / K
    energy_wasted = 8 * Nav * Cmin * (Vin**2)
    Ecap_fJ_bOP = ((energy_signal + energy_wasted) * 1e15) / 32
    
    # 5. ADC Energy (Scales with 2^By)
    # The 0.25 fJ baseline represents the standard optimized resolution (By=14)
    Eadc_fJ_bOP = 0.25 * (2**By_sig / 2**14)
    
    Etot_fJ_bOP = Ecap_fJ_bOP + Eadc_fJ_bOP
    
    return Etot_fJ_bOP

# ==========================================
# Generate Data
# ==========================================
By_range = np.linspace(10, 14, 100)
r_list = [5, 10, 20, 50, 100]

fig, ax1 = plt.subplots(figsize=(10, 7))

# Setup Colormap
cmap = plt.cm.viridis
colors = [cmap(i/(len(r_list)-1)) for i in range(len(r_list))]

# Calculate and plot for each ON/OFF ratio
for i, r in enumerate(r_list):
    etot_vals = [calculate_Etot_Fig14(b, r) for b in By_range]
    
    # Make the r=50 "sweet spot" line slightly thicker to stand out
    lw = 3.5 if r == 50 else 2.0
    
    ax1.plot(By_range, etot_vals, color=colors[i], lw=lw, label=f'ON/OFF={r}')

# ==========================================
# Formatting
# ==========================================
# Primary Y-Axis (Energy)
ax1.set_yscale('log')
ax1.set_xlim(10, 14)
ax1.set_ylim(0.01, 100) # Scaled to capture the r=5 spike at 14-bit
ax1.set_xlabel(r'ADC Resolution $B_y$ (bit)', fontsize=12)
ax1.set_ylabel(r'Total Energy $E_{tot}$ (fJ $\cdot$ b / OP)', fontsize=12)
ax1.grid(True, which='both', ls='--', alpha=0.4)

# Custom X-axis ticks to match the paper exactly
ax1.set_xticks([10, 11, 12, 13, 14])

# Secondary Y-Axis (POPS/W/b Efficiency)
ax2 = ax1.twinx()
ax2.set_yscale('log')
ax2.set_ylim(1/0.01, 1/100) # Exact reciprocal of left axis limits
ax2.set_ylabel('POPS/W/b', fontsize=12)

# Title and Legend
ax1.set_title(r'Figure 14 Reproduction: $E_{tot}$ vs. ADC Resolution ($K=8192$)', fontsize=14)
ax1.legend(loc='upper left', title="ON/OFF Ratio", fontsize=10)

plt.tight_layout()
#plt.show()
plt.savefig('figures/Etot_By_Pops.png', dpi=300)  