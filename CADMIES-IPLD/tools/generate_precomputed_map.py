#!/usr/bin/env python3
"""
Pre-compute node positions using networkx spring_layout.
Generates a mycelium map with preset positions — no client-side force simulation.
First version: 200 nodes for testing on dev site.
"""

import json, sys, math
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

# === PATH SETUP ===
TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from cadmies_concept_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR

# === CONFIG ===
OUTPUT_FILE = PROJECT_ROOT / "mycelium_map_precomputed_test.html"
MAX_NODES = 200

# Same domain config as v2.4.0
CANONICAL_DOMAINS = [
    "Physics", "Philosophy", "Biology", "Mathematics", "Consciousness",
    "Chemistry", "Ethics", "Computer Science", "Psychology", "Spirituality",
    "Neuroscience", "Sociology", "Economics", "Ecology", "Medicine",
]

DOMAIN_COLORS = {
    "Physics": "#4F46E5", "Philosophy": "#6366F1", "Biology": "#10B981",
    "Mathematics": "#1E1B4B", "Consciousness": "#0F172A", "Chemistry": "#F59E0B",
    "Ethics": "#EC4899", "Computer Science": "#3B82F6", "Psychology": "#14B8A6",
    "Spirituality": "#A78BFA", "Neuroscience": "#14B8A6", "Sociology": "#EC4899",
    "Economics": "#F59E0B", "Ecology": "#10B981", "Medicine": "#10B981",
}
DEFAULT_COLOR = "#64748B"

print("Loading concepts from blockstore...")
cids = load_all_concept_cids()
print(f"Found {len(cids)} concept CIDs")

# Load concepts
concepts = []
for cid in cids[:MAX_NODES]:
    try:
        c = load_concept(cid)
        human_id = c.get('human_id', '')
        name = c.get('name', human_id)
        definition = (c.get('definition', '') or '')[:200]
        domain = c.get('domain', 'Unknown')
        
        # Map domain to canonical
        from generate_mycelium_map import DOMAIN_UPWARD_MAP
        canonical_domain = DOMAIN_UPWARD_MAP.get(domain, domain)
        if canonical_domain not in CANONICAL_DOMAINS:
            canonical_domain = "Philosophy"  # default fallback
        
        color = DOMAIN_COLORS.get(canonical_domain, DEFAULT_COLOR)
        
        concepts.append({
            'id': human_id,
            'label': name,
            'definition': definition,
            'domain': canonical_domain,
            'color': color,
        })
    except Exception as e:
        pass

print(f"Parsed {len(concepts)} concepts")

# Build edges from relationships
edges = []
concept_ids = {c['id'] for c in concepts}
for c in concepts:
    try:
        cid = None
        for orig_cid in cids:
            if orig_cid.endswith(c['id']) or c['id'] in orig_cid:
                cid = orig_cid
                break
        if not cid:
            continue
        full = load_concept(cid)
        relationships = full.get('relationships', [])
        for rel in relationships:
            target = rel.get('target', '')
            rel_type = rel.get('type', 'related_to')
            if target in concept_ids:
                edges.append({
                    'source': c['id'],
                    'target': target,
                    'type': rel_type,
                })
    except:
        pass

print(f"Built {len(edges)} edges")

# Pre-compute positions with networkx
import networkx as nx
import random
random.seed(42)

G = nx.Graph()
for c in concepts:
    G.add_node(c['id'])
for e in edges:
    G.add_edge(e['source'], e['target'])

print("Computing spring layout...")
positions = nx.spring_layout(G, k=300, iterations=100, seed=42)

# Scale positions to pixel coordinates
for node_id in positions:
    positions[node_id] = {
        'x': positions[node_id][0] * 4000 + 2000,
        'y': positions[node_id][1] * 4000 + 2000,
    }

print(f"Computed positions for {len(positions)} nodes")

# === GENERATE HTML (simplified from v2.4.0) ===
print("Generating HTML...")
nodes_json = []
for c in concepts:
    pos = positions.get(c['id'], {'x': 2000, 'y': 2000})
    nodes_json.append(
        '{{ data: {{ id: "{}", label: "{}", definition: "{}", domain: "{}", background_color: "{}", x: {}, y: {} }} }}'.format(
            c['id'].replace('"', '\\"'),
            c['label'].replace('"', '\\"'),
            c['definition'].replace('"', '\\"'),
            c['domain'].replace('"', '\\"'),
            c['color'],
            round(pos['x'], 1),
            round(pos['y'], 1),
        )
    )

edges_json = []
for e in edges:
    edges_json.append(
        '{{ data: {{ source: "{}", target: "{}", label: "{}" }} }}'.format(
            e['source'].replace('"', '\\"'),
            e['target'].replace('"', '\\"'),
            e['type']
        )
    )

# Read the v2.4.0 template from dev-stash and modify it
with open(PROJECT_ROOT / 'mycelium_map.html', 'r') as f:
    template = f.read()

# Replace layout: use preset instead of cose
template = template.replace(
    "layout: {\n                name: 'cose',\n                idealEdgeLength: 120,\n                nodeRepulsion: 6000,\n                gravity: 0.15,\n                numIter: 2000,\n                animate: true,\n                animationDuration: 1500,\n                nodeOverlap: 20,\n                nodeDimensionsIncludeLabels: false\n            }",
    "layout: { name: 'preset', animate: false }"
)

# Replace nodes and edges
template = template.replace('__NODES_JSON__', ',\n'.join(nodes_json))
template = template.replace('__EDGES_JSON__', ',\n'.join(edges_json) if edges_json else '')
template = template.replace('__INFO_TEXT__', f'CADMIES Mycelium Map (Pre-computed) | {len(concepts)} nodes | {len(edges)} edges | {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")} | Click node for details | / to search | Esc to reset')

with open(OUTPUT_FILE, 'w') as f:
    f.write(template)

print(f"\nDone! Map saved to {OUTPUT_FILE}")
print(f"Nodes: {len(concepts)}, Edges: {len(edges)}")
