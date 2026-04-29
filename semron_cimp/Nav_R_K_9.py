import math
import numpy as np
import matplotlib.pyplot as plt

def calculate_Nav(K, r):
    """
    Calculates the Number of Averages (Nav) based on Equation (42)
    from Demasius et al., CCMCC 2025.
    """
    Cmax = 1e-15       # 1 fF Maximum capacitance
    Vin = 0.4          # 400 mV Input read voltage
    Sw = 4             # 4-bit weights
    Sx = 1             # 1-bit input slices
    T = 330            # 330 K 
    
    k_boltzmann = 1.380649e-23
    kT = k_boltzmann * T
    
    # Dynamic ADC Resolution Calculation
    By = 10 + math.log2(K / 128)
    
    # Capacitance Derivations
    Cmin = Cmax / r
    Cpar = K * Cmin
    
    # Active capacitive cells (Ncap)
    Ncap = (2**By) / ((2**Sw) * (2**Sx))
    
    # Total Array Capacitance (Ctot)
    Ctot = (K * Cmin) + Cpar + (Ncap * Cmax)
    
    # Equation 42 Formulation
    term1 = 36 * kT * Ctot
    term2 = ((2**(Sw - 1) - 1)**2) * ((2**Sx - 1)**2)
    term3 = ((Cmax - Cmin)**2) * (Vin**2)
    
    Nav = (term1 * term2) / term3
    return Nav

# ==========================================
# Generate Data for Plotting
# ==========================================
r_values = np.linspace(5, 100, 500)
K_values = [128, 256, 512, 1024, 2048, 4096, 8192]

# ==========================================
# Plotting Setup
# ==========================================
fig, ax1 = plt.subplots(figsize=(9, 6))

cmap = plt.cm.magma
colors = [cmap(i/(len(K_values)-1)) for i in range(len(K_values))]
colors.reverse()

# Plot the primary Nav lines
for i, K in enumerate(K_values):
    nav_values = [calculate_Nav(K, r) for r in r_values]
    ax1.plot(r_values, nav_values, label=f'K={K}', color=colors[i], linewidth=2.5)

# Primary Y-Axis Formatting (Nav)
ax1.set_yscale('log')
ax1.set_xlim(0, 100)
ax1.set_ylim(10**0, 10**3)
ax1.set_xlabel('ON/OFF Ratio', fontsize=12)
ax1.set_ylabel('Number of Averages -- $N_{av}$', fontsize=12)

# Secondary Y-Axis Formatting (Time)
ax2 = ax1.twinx()
ax2.set_yscale('log')
# Time is 40ns per average
ax2.set_ylim(10**0 * 40e-9, 10**3 * 40e-9)
ax2.set_ylabel('Time (Seconds)', fontsize=12)

# Custom tick formatting for Time axis (FIXED SYNTAX WARNING)
ticks = [40e-9, 400e-9, 4e-6, 40e-6]
labels = ['40 ns', '400 ns', r'4 $\mu$s', r'40 $\mu$s']
ax2.set_yticks(ticks)
ax2.set_yticklabels(labels)

ax1.set_title('Fig. 9 Reproduction with Time Axis', fontsize=14)
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend(loc='center right', title="Matrix Size", fontsize=10)

plt.tight_layout()
#plt.show()
plt.savefig('figures/Nav_R_K_9.png', dpi=300)