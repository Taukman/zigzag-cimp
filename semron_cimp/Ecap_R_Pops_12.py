import math
import numpy as np
import matplotlib.pyplot as plt

def calculate_Ecap_dual_By(K, r):
    # Fixed Physical Constants
    Cmax = 1e-15       # 1 fF
    Vin = 0.4          # 400 mV
    Sw = 4             # 4-bit weights
    Sx = 1             # 1-bit input slices
    T = 330            # 330 K
    k_boltzmann = 1.380649e-23
    kT = k_boltzmann * T
    
    # Dual By Logic:
    # 1. Physical By (Determines noise/Nav)
    By_phys = 10 + math.log2(K / 128)
    
    # 2. Signal By (Determines active charge movement energy)
    By_sig = 8 + math.log2(K / 128)
    
    # Capacitance Derivations (from physical hardware layout)
    Cmin = Cmax / r
    Cpar = K * Cmin
    Ncap = (2**By_phys) / ((2**Sw) * (2**Sx))
    Ctot = (K * Cmin) + Cpar + (Ncap * Cmax)
    
    # Equation 42: Calculate Nav based on physical array characteristics
    term1_nav = 36 * kT * Ctot
    term2_nav = ((2**(Sw - 1) - 1)**2) * ((2**Sx - 1)**2)
    term3_nav = ((Cmax - Cmin)**2) * (Vin**2)
    Nav_theo = (term1_nav * term2_nav) / term3_nav
    
    # Enforce hardware limit: minimum 1 average cycle
    Nav = max(Nav_theo, 1.0)
    
    # Equation 35: Q_LSB
    Q_LSB = ((Cmax - Cmin) / (2**(Sw - 1) - 1)) * (Vin / (2**Sx - 1))
    
    # Equation 43: Ecap (Joules)
    energy_signal = (8 * Nav * Q_LSB * Vin * (2**By_sig)) / K
    energy_wasted = 8 * Nav * Cmin * (Vin**2)
    Ecap_J = energy_signal + energy_wasted
    
    # Normalize to fJ and divide by total bit-operations (32 bits per MAC)
    Ecap_fJ_bOP = (Ecap_J * 1e15) / 32
    
    return Ecap_fJ_bOP

# Generate data
r_axis = np.linspace(5, 100, 500)
K_list = [128, 256, 512, 1024, 2048, 4096, 8192]

fig, ax1 = plt.subplots(figsize=(10, 7))
cmap = plt.cm.magma
colors = [cmap(i/(len(K_list)-1)) for i in range(len(K_list))]
colors.reverse()

for i, K in enumerate(K_list):
    y_vals = [calculate_Ecap_dual_By(K, r) for r in r_axis]
    ax1.plot(r_axis, y_vals, label=f'K={K}', color=colors[i], lw=2.5)

# Axis 1 Formatting (Ecap) - FIXED STRINGS HERE
ax1.set_yscale('log')
ax1.set_xlim(0, 100)
ax1.set_ylim(0.01, 10)
ax1.set_xlabel(r'ON/OFF Ratio $C_{\max}/C_{\min}$', fontsize=12)
ax1.set_ylabel(r'$E_{cap}$ (fJ $\cdot$ b / OP)', fontsize=12)
ax1.grid(True, which='both', ls='--', alpha=0.4)

# Axis 2 Formatting (Efficiency)
ax2 = ax1.twinx()
ax2.set_yscale('log')
ax2.set_ylim(1/0.01, 1/10) 
ax2.set_ylabel('POPS/W/b', fontsize=12)

ax1.set_title('Figure 12 Reproduction: Energy efficiency vs. ON/OFF Ratio\n'
             r'(Dual $B_y$ Logic: Physical=10, Signal=8 for K=128)', fontsize=14)
ax1.legend(title='Matrix size $K$', loc='center right', bbox_to_anchor=(0.95, 0.5))

plt.tight_layout()
#plt.show()
plt.savefig('figures/Ecap_R_Pops_12.png', dpi=300)  