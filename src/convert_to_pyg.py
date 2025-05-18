import os
import json
import torch
from torch_geometric.data import Data

GRAPH_DIR = "data/graphs_with_features"
OUTPUT_PATH = "data/pyg_graphs.pt"

def load_graph(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
        x = torch.tensor(data['x'], dtype=torch.long)  # shape [num_nodes, feature_dim]
        edge_index = torch.tensor(data['edge_index'], dtype=torch.long).t().contiguous()  # shape [2, num_edges]
        return x, edge_index

def convert_all(graph_dir: str, output_path: str):
    data_list = []

    for label in sorted(os.listdir(graph_dir)):
        label_path = os.path.join(graph_dir, label)
        if not os.path.isdir(label_path):
            continue

        try:
            y = int(label) - 1
        except ValueError:
            print(f"Skipping unexpected label name: {label}")
            continue

        for file in os.listdir(label_path):
            if not file.endswith(".json"):
                continue

            graph_path = os.path.join(label_path, file)
            try:
                x, edge_index = load_graph(graph_path)
                data = Data(x=x, edge_index=edge_index, y=torch.tensor([y], dtype=torch.long))
                data_list.append(data)
            except Exception as e:
                print(f"⚠️ Failed to process {graph_path}: {e}")

    torch.save(data_list, output_path)
    print(f"✔ Saved {len(data_list)} graphs to {output_path}")

if __name__ == "__main__":
    convert_all(GRAPH_DIR, OUTPUT_PATH)
