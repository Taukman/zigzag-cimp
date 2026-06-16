import math
import numpy as np
import matplotlib.pyplot as plt

def calculate_energies(K, r):
    """
    Calculates E_cap and E_tot for a given K and r.
    Uses Physical By=10 and Signal By=8 logic for K=128 base.
    """
    # 1. Physical Constants
    Cmax, Vin, Sw, Sx, T = 1e-15, 0.4, 4, 1, 330
    kT = 1.380649e-23 * T
    
    # 2. Dual By Logic
    By_phys = 10 + math.log2(K / 128)
    By_sig = 8 + math.log2(K / 128)
    
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
    
    # 5. ADC Energy (Walden FOM Baseline from text)
    Eadc_fJ_bOP = 0.25
    
    Etot_fJ_bOP = Ecap_fJ_bOP + Eadc_fJ_bOP
    
    return Ecap_fJ_bOP, Etot_fJ_bOP

# ==========================================
# Generate Data
# ==========================================
K_axis = np.linspace(128, 8192, 100)
r_list = [5, 10, 20, 50, 100]

fig, ax1 = plt.subplots(figsize=(10, 7))

# Setup Colormap
cmap = plt.cm.viridis
colors = [cmap(i/(len(r_list)-1)) for i in range(len(r_list))]

# Plot Ecap (dashed) and Etot (solid) for each ON/OFF ratio
for i, r in enumerate(r_list):
    results = [calculate_energies(K, r) for K in K_axis]
    ecap_vals = [res[0] for res in results]
    etot_vals = [res[1] for res in results]
    
    # Solid line for Total Energy
    ax1.plot(K_axis, etot_vals, color=colors[i], lw=2.5, label=f'ON/OFF={r}')
    # Dashed line for Capacitive Thermal Energy
    ax1.plot(K_axis, ecap_vals, color=colors[i], lw=1.5, ls='--')

# Plot the Walden FOM Baseline
ax1.axhline(0.25, color='black', lw=2, label='Walden FOM')

# ==========================================
# Formatting (Updated Limits)
# ==========================================
ax1.set_yscale('log')
ax1.set_xlim(0, 8192)
# UPDATED Y-LIMITS
ax1.set_ylim(0.01, 10) 
ax1.set_xlabel(r'Column Length $K$', fontsize=12)
ax1.set_ylabel(r'$E_{tot}$ (fJ $\cdot$ b / OP)', fontsize=12)
ax1.grid(True, which='both', ls='--', alpha=0.4)

# POPS/W/b Secondary Axis
ax2 = ax1.twinx()
ax2.set_yscale('log')
# UPDATED RECIPROCAL LIMITS (1/0.01=100, 1/10=0.1)
ax2.set_ylim(100, 0.1) 
ax2.set_ylabel('POPS/W/b', fontsize=12)

ax1.set_title(r'Figure 13 Reproduction: Energy efficiency vs. Column Length $K$', fontsize=14)
ax1.legend(loc='upper left', fontsize=10, ncol=2)

plt.tight_layout()
#plt.show()
plt.savefig('figures/Etot_K_Pops.png', dpi=300)  