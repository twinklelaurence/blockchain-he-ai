# File: generate_context.py

import os
import tenseal as ts

# Step 1: Create context
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.global_scale = 2 ** 40
context.generate_galois_keys()
context.make_context_public()  # Public key for clients

# Step 2: Define output path
output_path = os.path.abspath("C:/Users/Hevert/AppData/Local/Programs/Python/Python312/encryption/tenseal_context.tenseal")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Step 3: Save context with secret key
with open(output_path, "wb") as f:
    f.write(context.serialize(save_secret_key=True))

print("✅ TenSEAL context generated and saved with secret key.")
print(f"📁 Path: {output_path}")



