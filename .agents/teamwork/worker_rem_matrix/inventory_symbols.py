import os
import glob
import json

def get_files(base_dir, pattern="*"):
    matches = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            matches.append(os.path.relpath(os.path.join(root, f), ".").replace("\\", "/"))
    return matches

print("--- Python Files in code/python/src/mub ---")
mub_files = [f for f in get_files("code/python/src/mub") if f.endswith(".py")]
for f in sorted(mub_files):
    print(f)

print("\n--- Python Files in code/python/tests ---")
test_files = [f for f in get_files("code/python/tests") if f.endswith(".py")]
for f in sorted(test_files):
    print(f)

print("\n--- Python Files in code/python/src/majorana ---")
maj_files = [f for f in get_files("code/python/src/majorana") if f.endswith(".py")]
for f in sorted(maj_files):
    print(f)

print("\n--- Python Files in code/python/src/fsp ---")
fsp_files = [f for f in get_files("code/python/src/fsp") if f.endswith(".py")]
for f in sorted(fsp_files):
    print(f)
