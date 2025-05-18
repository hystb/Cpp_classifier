import os
import subprocess
from pathlib import Path

CPP_ROOT = "data/ProgramData"               # Dossier racine contenant class1/, class2/, etc.
OUT_ROOT = "data/poj104_binaries"     # Où stocker les exécutables

os.makedirs(OUT_ROOT, exist_ok=True)

compilation_log = []

for class_name in os.listdir(CPP_ROOT):
    class_dir = os.path.join(CPP_ROOT, class_name)
    if not os.path.isdir(class_dir):
        continue

    out_class_dir = os.path.join(OUT_ROOT, class_name)
    os.makedirs(out_class_dir, exist_ok=True)

    for file in os.listdir(class_dir):
        if not file.endswith(".cpp"):
            continue

        input_path = os.path.join(class_dir, file)
        output_path = os.path.join(out_class_dir, Path(file).stem)

        cmd = ["clang", "-O0", "-g", input_path, "-o", output_path]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            compilation_log.append(f"✔ Compiled: {input_path}")
        except subprocess.CalledProcessError as e:
            compilation_log.append(f"❌ Failed: {input_path}\n{e.stderr.decode()}")

log_path = "compile_log.txt"
with open(log_path, "w") as f:
    f.write("\n".join(compilation_log))

print(f"✅ Compilation finished. Log saved to {log_path}")
