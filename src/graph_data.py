import os
import json
import torch
from typing import List, Dict, Tuple
from collections import Counter
import hashlib

GRAPH_DIR = "data/graphs"
OUTPUT_DIR = "data/graphs_with_features"
TOP_K_SPELLINGS = 1000

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Step 1: Build vocabularies
def build_vocab(graph_dir: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    type_counter = Counter()
    spelling_counter = Counter()

    for label in os.listdir(graph_dir):
        for file in os.listdir(os.path.join(graph_dir, label)):
            with open(os.path.join(graph_dir, label, file), 'r') as f:
                graph = json.load(f)
                for node in graph['nodes']:
                    type_counter[node['type']] += 1
                    if node['name']:
                        spelling_counter[node['name']] += 1

    type_vocab = {t: i for i, t in enumerate(sorted(type_counter))}
    most_common_spellings = [s for s, _ in spelling_counter.most_common(TOP_K_SPELLINGS)]
    spelling_vocab = {s: i+1 for i, s in enumerate(most_common_spellings)}  # +1 for UNK=0

    return type_vocab, spelling_vocab

# Step 2: Convert a graph with enriched features
def convert_graph(graph_json: Dict, type_vocab: Dict[str, int], spelling_vocab: Dict[str, int]) -> Dict:
    def encode_spelling(s):
        return spelling_vocab.get(s, 0)  # 0 = UNK

    def is_operator(t):
        return int("OPERATOR" in t)

    def is_literal(t):
        return int("LITERAL" in t)

    nodes = graph_json['nodes']
    edges = graph_json['edges']

    new_nodes = []
    for node in nodes:
        type_id = type_vocab.get(node['type'], 0)
        spelling_id = encode_spelling(node['name'])
        operator_flag = is_operator(node['type'])
        literal_flag = is_literal(node['type'])

        new_nodes.append([type_id, spelling_id, operator_flag, literal_flag])

    return {
        "x": new_nodes,
        "edge_index": edges
    }

# Step 3: Process all graphs
def process_all(graph_dir: str, output_dir: str):
    type_vocab, spelling_vocab = build_vocab(graph_dir)

    for label in os.listdir(graph_dir):
        in_dir = os.path.join(graph_dir, label)
        out_dir = os.path.join(output_dir, label)
        os.makedirs(out_dir, exist_ok=True)

        for file in os.listdir(in_dir):
            with open(os.path.join(in_dir, file), 'r') as f:
                graph = json.load(f)

            processed = convert_graph(graph, type_vocab, spelling_vocab)
            with open(os.path.join(out_dir, file), 'w') as out_f:
                json.dump(processed, out_f)

    print(f"✔ Processed graphs saved to: {output_dir}")

if __name__ == "__main__":
    process_all(GRAPH_DIR, OUTPUT_DIR)
