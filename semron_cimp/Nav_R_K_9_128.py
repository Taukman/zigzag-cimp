import math
import numpy as np
import matplotlib.pyplot as plt

def calculate_Nav(K, r):
    Cmax = 1e-15       
    Vin = 0.4          
    Sw = 4             
    Sx = 1             
    T = 330            
    
    k_boltzmann = 1.380649e-23
    kT = k_boltzmann * T
    
    By = 10 + math.log2(K / 128)
    Cmin = Cmax / r
    Cpar = K * Cmin
    
    Ncap = (2**By) / ((2**Sw) * (2**Sx))
    Ctot = (K * Cmin) + Cpar + (Ncap * Cmax)
    
    term1 = 36 * kT * Ctot
    term2 = ((2**(Sw - 1) - 1)**2) * ((2**Sx - 1)**2)
    term3 = ((Cmax - Cmin)**2) * (Vin**2)
    
    return (term1 * term2) / term3

K = 128

# 1. Continuous Line Data
r_line = np.linspace(5, 100, 500)
nav_line = [calculate_Nav(K, r) for r in r_line]

# 2. Discrete Data Points (Every 5)
r_points = np.arange(5, 105, 5)
nav_points = [calculate_Nav(K, r) for r in r_points]

# 3. Calculate reference time at r=5 for percentage improvement
ref_nav = nav_points[0]
ref_time = ref_nav * 40e-9

# ==========================================
# Plotting Setup
# ==========================================
fig, ax1 = plt.subplots(figsize=(12, 7)) # Widened to give text more room

ax1.plot(r_line, nav_line, label=f'K={K}', color='indigo', linewidth=2.5)
ax1.scatter(r_points, nav_points, color='crimson', zorder=5, label='Points every 5')

# 4. Add text annotations to each point
for r, nav in zip(r_points, nav_points):
    time_s = nav * 40e-9
    time_ns = time_s * 1e9
    
    # Calculate percentage improvement
    improvement = ((ref_time - time_s) / ref_time) * 100
    
    # Format the label string
    if improvement > 0:
        label_text = f"{time_ns:.1f}ns\n(+{improvement:.1f}%)"
    else:
        label_text = f"{time_ns:.1f}ns\n(ref)"
    
    # Draw the annotation on the plot
    ax1.annotate(label_text, 
                 xy=(r, nav), 
                 xytext=(0, 8),               # Shift text slightly up
                 textcoords="offset points", 
                 ha='center', 
                 va='bottom', 
                 fontsize=9, 
                 rotation=45)                 # Angled to prevent overlap

# Primary Y-Axis (Nav)
ax1.set_yscale('log')
ax1.set_xlim(0, 105)
ax1.set_ylim(10**0, 10**1) # Adjusted for K=128 visibility
ax1.set_xlabel('ON/OFF Ratio', fontsize=12)
ax1.set_ylabel('Number of Averages -- $N_{av}$', fontsize=12)

# Secondary Y-Axis (Time)
ax2 = ax1.twinx()
ax2.set_yscale('log')
ax2.set_ylim(10**0 * 40e-9, 10**1 * 40e-9)
ax2.set_ylabel('Time (Seconds)', fontsize=12)

ticks = [40e-9, 100e-9, 200e-9, 400e-9]
labels = ['40 ns', '100 ns', '200 ns', '400 ns']
ax2.set_yticks(ticks)
ax2.set_yticklabels(labels)

ax1.set_title('Fig. 9 Sub-plot (K=128) with Time & Improvement Annotations', fontsize=14)
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend(loc='upper right', fontsize=10)

plt.tight_layout()
#plt.show()
plt.savefig('figures/Nav_R_K_9_128.png', dpi=300)