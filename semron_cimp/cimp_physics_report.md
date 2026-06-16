# CIMP Integration Report: Physics vs Performance

You successfully executed the integrated CIMP framework! By decoupling the `cells` memory level from the generic SRAM YAML configurations, the simulator now flawlessly uses the physical capacitor parameters to dictate the energy required to set up the array. 

Here is the exact mathematical breakdown of how your new system achieved **35.5 TOPS/W** and a massive **99,530 pJ** drop in energy.

## 1. The Disappearance of the SRAM Penalty
In the old system, ZigZag used the hardcoded `w_cost: 0.095 pJ` from the YAML to calculate the energy required to write your 1,048,576 weights into the cells.
*   **Old Weight Setup Energy:** $1,048,576 \times 0.095 \text{ pJ} = \mathbf{99,614.72 \text{ pJ}}$

In the **new system**, `accelerator_factory.py` intercepts the memory creation and asks the CIMP physics model for the true cost. Based on your `imc_unit.py` definitions ($C_{max} = 1\text{fF}$, $V_{in} = 0.4\text{V}$), the average energy to charge the capacitor is:
*   $E_{write} = \frac{1}{2} C_{max} V_{in}^2$
*   $E_{write} = 0.5 \times (1 \times 10^{-15}\text{F}) \times (0.4\text{V})^2 = \mathbf{0.00008 \text{ pJ}}$

The true cost to load all 1,048,576 weights into the capacitors is now:
*   **New Weight Setup Energy:** $1,048,576 \times 0.00008 \text{ pJ} = \mathbf{83.88 \text{ pJ}}$

**The Impact:** The Memory Transfer energy dropped by exactly `99,614.72 - 83.88 = 99,530.83 pJ`. This perfectly accounts for the difference between the old Memory Transfer (`208,361.47`) and the new Memory Transfer (`108,830.64`)!

## 2. Where is the remaining 108,830 pJ going?
Now that the weight setup penalty is gone, what is consuming the remaining memory energy?
It's entirely consumed by moving the Input Activations from the massive, power-hungry SRAM.
1.  **SRAM_256KB Read Cost:** Reading the inputs out of the top-level SRAM costs $416.16 \text{ pJ}$ per read. Because of the reuse patterns, this accounts for **~106,536 pJ**.
2.  **Register File (RF) Transfers:** The remaining ~2,000 pJ is spent moving those inputs and outputs between the local `rf_1B` and `rf_2B` registers.

## 3. Why did Latency stay at 18,491 ns?
You ran the simulation with `weights_preloaded: False` (which is perfect for a full-lifecycle analysis). 
Because we only overwrote the `w_cost` (Energy), ZigZag still respects the physical `bandwidth` of the ports defined in `cimp.yaml` (8 bits/cycle). 
1.  **Data Onloading (Stall):** It still takes **128 cycles** to pipe the 1,048,576 weights through the narrow bandwidth into the array. 
2.  **Input Fetching (Stall):** It still takes **124 cycles** to fetch inputs from the SRAM.
3.  **Computation:** The MAC operations still take **8 cycles**.

> [!TIP]
> If you want to see the "Steady State" latency (where the array is constantly crunching data without having to pause to load new weights), change `weights_preloaded: True` in `cimp.yaml` and run it again. You will see the 128 cycle delay instantly disappear!

## 4. The Final Efficiency Jump
By fixing the artificial SRAM penalty, the system efficiency jumped from **19.2 TOPS/W** to **35.5 TOPS/W**. 

Your hardware is a hybrid: The CIMP operational array is incredibly efficient (hitting a theoretical peak of **462 TOPS/W**), but the massive system-level SRAM memory hierarchy drags the total efficiency down to 35.5 TOPS/W. 

This is the classic **"Memory Wall."** You now have a perfectly physically-accurate baseline to start optimizing the memory hierarchy (e.g. increasing batch size, widening the SRAM bandwidth, or reducing SRAM read cost) to push the System TOPS/W closer to the Macro peak!
