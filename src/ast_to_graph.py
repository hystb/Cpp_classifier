import json
import os
from typing import List, Dict, Tuple

def load_ast(filepath: str) -> Dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_graph_from_ast(ast_json: Dict) -> Tuple[List[Dict], List[Tuple[int, int]]]:
    nodes = []
    edges = []

    def visit(node, parent_id=None):
        node_id = len(nodes)
        nodes.append({
            "id": node_id,
            "type": node.get("kind"),
            "name": node.get("spelling") or ""
        })

        if parent_id is not None:
            edges.append((parent_id, node_id))

        for child in node.get("children", []):
            visit(child, node_id)

    visit(ast_json)
    return nodes, edges

def save_graph(graph, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2)

def convert_all_asts(ast_dir="data/parsed_ast", out_dir="data/graphs"):
    os.makedirs(out_dir, exist_ok=True)
    for label in os.listdir(ast_dir):
        label_dir = os.path.join(ast_dir, label)
        if not os.path.isdir(label_dir):
            continue
        output_label_dir = os.path.join(out_dir, label)
        os.makedirs(output_label_dir, exist_ok=True)

        for file in os.listdir(label_dir):
            if file.endswith(".json"):
                ast_path = os.path.join(label_dir, file)
                nodes, edges = build_graph_from_ast(load_ast(ast_path))
                graph = {"nodes": nodes, "edges": edges}
                out_file = os.path.join(output_label_dir, file)
                save_graph(graph, out_file)
                print(f"✔ Converted: {ast_path}")

if __name__ == "__main__":
    convert_all_asts()
