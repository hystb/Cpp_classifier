import os
import csv
import json
from clang import cindex

DATASET_DIR = "data/ProgramData"
LABELS_CSV = "data/labels.csv"
OUTPUT_DIR = "data/parsed_ast"

CLANG_LIB_PATH = "my_venv/lib/python3.11/site-packages/clang/native/libclang.so"

cindex.Config.set_library_file(CLANG_LIB_PATH)

def parse_ast(file_path):
    index = cindex.Index.create()
    translation_unit = index.parse(file_path, args=['-std=c++14'])

    def node_to_dict(node):
        return {
            'kind': str(node.kind).split('.')[-1],
            'spelling': node.spelling,
            'children': [node_to_dict(c) for c in node.get_children()]
        }

    return node_to_dict(translation_unit.cursor)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(LABELS_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filepath = row["filepath"]
            label = row["label"]
            full_path = os.path.join(DATASET_DIR, filepath)

            try:
                ast_dict = parse_ast(full_path)
                output_label_dir = os.path.join(OUTPUT_DIR, label)
                os.makedirs(output_label_dir, exist_ok=True)

                filename = os.path.splitext(os.path.basename(filepath))[0]
                output_file = os.path.join(output_label_dir, f"{filename}.json")

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(ast_dict, f, indent=2)
                
                print(f"✔ Parsed: {filepath}")
            except Exception as e:
                print(f"✘ Failed to parse {filepath}: {e}")

if __name__ == "__main__":
    main()
