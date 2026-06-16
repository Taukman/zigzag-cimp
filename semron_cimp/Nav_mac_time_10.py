import math
import numpy as np
import matplotlib.pyplot as plt

def calculate_Nav_fig10(K, Sw):
    """
    Calculates Nav for varying MAC Bitwidths (Sw).
    Includes the 'Sw=1 equals Sw=2' non-differential rule.
    """
    Cmax = 1e-15       
    Vin = 0.4          
    Sx = 1             
    r = 10             # Locked to ON/OFF = 10 for Fig 10
    T = 330            
    
    k_boltzmann = 1.380649e-23
    kT = k_boltzmann * T
    
    # Apply the non-differential flatline rule
    Sw_eff = max(Sw, 2)
    
    # ADC bitwidth remains strictly tied to K
    By = 10 + math.log2(K / 128)
    
    # Capacitances
    Cmin = Cmax / r
    Cpar = K * Cmin    
    
    # Ncap balloons as Sw drops, offsetting some of the Nav reduction
    Ncap = (2**By) / ((2**Sw_eff) * (2**Sx))
    Ctot = (K * Cmin) + Cpar + (Ncap * Cmax)
    
    # Equation 42 Formulation
    term1 = 36 * kT * Ctot
    term2 = ((2**(Sw_eff - 1) - 1)**2) * ((2**Sx - 1)**2)
    term3 = ((Cmax - Cmin)**2) * (Vin**2)
    
    Nav = (term1 * term2) / term3
    return Nav

# ==========================================
# Generate Data for Plotting
# ==========================================
mac_bitwidths = np.linspace(1, 6, 500)
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
    nav_values = [calculate_Nav_fig10(K, sw) for sw in mac_bitwidths]
    ax1.plot(mac_bitwidths, nav_values, label=f'K={K}', color=colors[i], linewidth=2.5)

# Primary Y-Axis Formatting (Nav)
ax1.set_yscale('log')
ax1.set_xlim(1, 6)
# START from 10^-1, END at 4*10^3
ax1.set_ylim(10**-1, 4*10**3) 
ax1.set_xlabel('MAC Bitwidth -- $S_w S_x$ (bit)', fontsize=12)
ax1.set_ylabel('Number of Averages -- $N_{av}$', fontsize=12)

# Secondary Y-Axis Formatting (Time)
ax2 = ax1.twinx()
ax2.set_yscale('log')
# ALIGNED scaling bounds for proper visual matching
ax2.set_ylim(10**-1 * 40e-9, 4*10**3 * 40e-9)
ax2.set_ylabel('Time (Seconds)', fontsize=12)

# Custom tick formatting includes 4 ns at the bottom (uses raw strings 'r' to prevent warnings)
ticks = [4e-9, 40e-9, 400e-9, 4e-6, 40e-6]
labels = ['4 ns', '40 ns', '400 ns', r'4 $\mu$s', r'40 $\mu$s']
ax2.set_yticks(ticks)
ax2.set_yticklabels(labels)

ax1.set_title('Fig. 10 Reproduction (Nav & Time vs. Bitwidth)', fontsize=14)
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend(loc='upper left', title="Matrix Size", fontsize=10)

plt.tight_layout()
#plt.show()
plt.savefig('figures/Nav_mac_time_10.png', dpi=300)