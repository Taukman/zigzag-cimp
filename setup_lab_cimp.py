import shutil
import os

print("Setting up lab_cimp...")

# Create the folder structure by copying lab5's inputs
os.makedirs("lab_cimp", exist_ok=True)
shutil.copytree("lab5/inputs", "lab_cimp/inputs", dirs_exist_ok=True)

# Remove the old accelerator.yaml and put our new cimp.yaml inside
if os.path.exists("lab_cimp/inputs/hardware/accelerator.yaml"):
    os.remove("lab_cimp/inputs/hardware/accelerator.yaml")
    
shutil.copy("zigzag/inputs/hardware/cimp.yaml", "lab_cimp/inputs/hardware/cimp.yaml")

# Modify the main.py file to point to the new paths
with open("lab5/main.py", "r") as f:
    code = f.read()

# Replace all occurrences of lab5 with lab_cimp for outputs and inputs
code = code.replace('"lab5/', '"lab_cimp/')
# Update the hardware configuration path
code = code.replace('hardware/accelerator.yaml', 'hardware/cimp.yaml')

with open("lab_cimp/main.py", "w") as f:
    f.write(code)

print("Successfully created lab_cimp! You can now run it.")
