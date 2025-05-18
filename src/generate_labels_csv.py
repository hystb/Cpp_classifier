import os
import csv
import sys

DATASET_DIR = sys.argv[1] if len(sys.argv) > 1 else None
if not DATASET_DIR:
    raise ValueError("Le chemin du répertoire de données n'est pas spécifié.")
print(f"✔ dataset dir: {DATASET_DIR}")
OUTPUT_CSV = "data/labels.csv"

def generate_labels_csv():
    entries = []
    for label in os.listdir(DATASET_DIR):
        label_path = os.path.join(DATASET_DIR, label)
        if not os.path.isdir(label_path):
            continue
        for filename in os.listdir(label_path):
            if filename.endswith(".cpp"):
                relative_path = os.path.join(label, filename)
                entries.append((relative_path, label))

    with open(OUTPUT_CSV, mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filepath", "label"])
        writer.writerows(entries)
    
    print(f"✔ labels {len(entries)}.")

if __name__ == "__main__":
    generate_labels_csv()
