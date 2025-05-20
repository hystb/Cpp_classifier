import os
import json
import angr
from tqdm import tqdm
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

BINARIES_DIR = "data/binaries/"
OUTPUT_DIR = "data/cfg_json/"
os.makedirs(OUTPUT_DIR, exist_ok=True)
NUM_WORKERS = os.cpu_count() or 4


def extract_ssa_features(vex_block):
    ops = Counter()
    if vex_block is None:
        return ops

    try:
        for stmt in vex_block.statements:
            opname = stmt.__class__.__name__
            ops[opname] += 1

        if vex_block.jumpkind:
            ops["jumpkind_" + str(vex_block.jumpkind)] += 1

        if hasattr(vex_block, "next") and hasattr(vex_block.next, "op"):
            ops["exit_op_" + str(vex_block.next.op)] += 1
    except Exception as e:
        ops["error"] = str(e)

    return dict(ops)


def extract_and_save(binary_path, json_path):
    try:
        project = angr.Project(binary_path, auto_load_libs=False)
        cfg = project.analyses.CFGFast(normalize=True)

        nodes = []
        edges = []
        id_map = {}

        for i, node in enumerate(cfg.graph.nodes):
            id_map[node] = i
            ir = ""
            ssa_features = {}

            try:
                if hasattr(node, "block") and node.block is not None:
                    vex = node.block.vex
                    ir = vex.pp() if vex else ""
                    ssa_features = extract_ssa_features(vex)
            except Exception as e:
                ssa_features = {"error": str(e)}

            nodes.append({
                "id": i,
                "addr": hex(node.addr) if hasattr(node, "addr") else None,
                "label": node.__class__.__name__,
                "ir": ir,
                "ssa_features": ssa_features
            })

        for src, dst in cfg.graph.edges:
            if src in id_map and dst in id_map:
                edges.append([id_map[src], id_map[dst]])

        with open(json_path, "w") as f:
            json.dump({"nodes": nodes, "edges": edges}, f, indent=2)

        return f"✔ {binary_path}"
    except Exception as e:
        return f"❌ {binary_path}\n{e}"

all_tasks = []

for class_name in os.listdir(BINARIES_DIR):
    class_path = os.path.join(BINARIES_DIR, class_name)
    if not os.path.isdir(class_path):
        continue

    out_class_path = os.path.join(OUTPUT_DIR, class_name)
    os.makedirs(out_class_path, exist_ok=True)

    for bin_file in os.listdir(class_path):
        if not bin_file:
            continue

        binary_path = os.path.join(class_path, bin_file)
        json_path = os.path.join(out_class_path, bin_file + ".json")

        if os.path.exists(json_path):
            continue  # Skip already done
        all_tasks.append((binary_path, json_path))

log = []

with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    futures = {
        executor.submit(extract_and_save, binary, json_path): binary
        for binary, json_path in all_tasks
    }

    for future in tqdm(as_completed(futures), total=len(futures), desc="Extracting CFGs + SSA"):
        result = future.result()
        log.append(result)


with open("cfg_extraction_log.txt", "w") as f:
    f.write("\n".join(log))

print("✅ CFG + SSA extraction finished.")
