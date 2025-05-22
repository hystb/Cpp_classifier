import json
from pathlib import Path
from sklearn.model_selection import train_test_split

DATASET_ROOT = Path("data/CodeNet_C++_1000/CodeNet_C++1000")
OUTPUT_JSONL = Path("data/c++_1000_jsonl")
OUTPUT_JSONL.mkdir(parents=True, exist_ok=True)

samples = []
label_map = {}
label_idx = 0

for label_dir in sorted(DATASET_ROOT.iterdir()):
    if label_dir.is_dir():
        label = label_dir.name
        if label not in label_map:
            label_map[label] = label_idx
            label_idx += 1

        for f in label_dir.glob("*.cpp"):
            code = f.read_text(encoding="utf-8")
            samples.append({
                "func": code,
                "label": label_map[label]
            })

train, temp = train_test_split(samples, test_size=0.2, random_state=42,
                               stratify=[s['label'] for s in samples])
valid, test = train_test_split(temp, test_size=0.5, random_state=42,
                               stratify=[s['label'] for s in temp])

with open(OUTPUT_JSONL / "train.jsonl", "w") as f:
    for ex in train:
        f.write(json.dumps(ex) + "\n")

with open(OUTPUT_JSONL / "valid.jsonl", "w") as f:
    for ex in valid:
        f.write(json.dumps(ex) + "\n")

with open(OUTPUT_JSONL / "test.jsonl", "w") as f:
    for ex in test:
        f.write(json.dumps(ex) + "\n")

with open("label_map.json", "w") as f:
    json.dump(label_map, f, indent=2)

print(f"✅ {len(train)} train | {len(valid)} val | \
    {len(test)} test | labels: {label_map}")
