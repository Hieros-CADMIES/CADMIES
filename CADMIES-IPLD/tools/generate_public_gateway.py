#!/usr/bin/env python3
---
System: CADMIES / tools
Document_ID: CA-2026-029-TOOL
Version: 3.2.1
Classification: INTERNAL
Author: The Gardener
Reviewers: [The Gardener, DeepSeek]
Status: ACTIVE
Created: 2026-08-12
Modified: 2026-08-12
Related_Docs: [paths.py, generate_mycelium_map.py]
---
"""
File: generate_public_gateway.py
Tool: CADMIES Public Mycelium Gateway Generator
Version: 3.2.1
System: CADMIES / tools
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Generates a single-page public-facing website from the blockstore.
         All concepts rendered as filterable, searchable cards on one page.
         Includes JSON-LD structured data feed and XML sitemap.

         Domain filter pills now actually filter the concept cards.
         Subdomain tier is designed but not yet implemented.

         translate.js integration — client-side multilingual support.
         Toggle placed left of the CADMIES title. Language preference stored in localStorage.
         Default: disabled. User clicks to activate translation dropdown.

         No personal information. No internal tooling references.
         Just the knowledge the mycelium wants to share with the world.

Usage:
    python tools/generate_public_gateway.py

Output:
    ../docs/ — static site served by web server

Version History:
  v3.2.1 (2026-08-12): Added scientific documentation YAML metadata block.
      Made version display dynamic via VERSION constant.
      Switched to paths.py DOCS_DIR for output directory.
      Removed terminal emoji for scientific rigor compliance.
      Gateway UI emojis retained (🌐 🌱).
  v3.2.0 (2026-08-09): Added translate.js integration — client-side multilingual support.
      Toggle left of CADMIES title. localStorage language persistence.
      Privacy note in footer. Default disabled.
  v3.1.2 (2026-07-31): Added ORCID iD to stats bar (0009-0000-8877-2731).
  v3.1.1 (2026-07-29): Updated SITE_URL to project-hierion.org. Final migration from DuckDNS to official domain.
  v3.1.0 (2026-07-27): Domain filter pills now functional. Added domain and
      canonical_domain fields to concepts.json. JavaScript filter logic now
      hides/shows cards based on selected domain. Results counter updates.
      Subdomain tier placeholder added for future expansion.
  v3.0.0 (2026-06-24): Project renamed from Hieros to Hierion. Updated all
      URLs and references to reflect new project identity and domain.
  v2.0.1 (2026-05-27): Fixed OUTPUT_DIR from public_concepts_gateway/ to ../docs/.
      Updated SITE_URL. Updated deploy message to reference /docs folder.
  v2.0.0 (2026-05-15): Initial public gateway release with filterable concept cards,
      interactive map, JSON-LD feed, and XML sitemap.
"""

import json, sys
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

# === PATH SETUP ===
TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "agents" / "code"))
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "core"))

from cadmies_concept_reader import load_concept, load_all_concept_cids
from paths import BLOCKS_DIR, DOCS_DIR

VERSION = "3.2.1"
OUTPUT_DIR = DOCS_DIR
SITE_URL = "https://project-hierion.org"

# === CANONICAL 15-DOMAIN TAXONOMY ===
CANONICAL_DOMAINS = [
    "Physics",
    "Philosophy",
    "Biology",
    "Mathematics",
    "Consciousness",
    "Chemistry",
    "Ethics",
    "Computer Science",
    "Psychology",
    "Spirituality",
    "Neuroscience",
    "Sociology",
    "Economics",
    "Ecology",
    "Medicine",
]

# === DOMAIN UPWARD MAP (from generate_mycelium_map.py) ===
DOMAIN_UPWARD_MAP = {
    "Theoretical Physics": "Physics",
    "Cosmology": "Physics",
    "Complexity_Science": "Physics",
    "Astrophysics": "Physics",
    "Physics (String Theory)": "Physics",
    "Physics, Quantum Field Theory": "Physics",
    "Quantum Mechanics, Philosophy": "Physics",
    "Quantum Physics and Philosophy": "Physics",
    "Quantum Physics, Consciousness Studies": "Physics",
    "Physics and Philosophy": "Physics",
    "Physics & Philosophy": "Physics",
    "Physics, Philosophy": "Physics",
    "Philosophy, Physics": "Philosophy",
    "Physics, Metaphysics": "Physics",
    "Metaphysics, Philosophy": "Philosophy",
    "Physics, Philosophy, Consciousness": "Physics",
    "Physics, Philosophy, Biology": "Physics",
    "Physics, Biology, Ecology": "Physics",
    "Physics, Biology, Computer Science": "Physics",
    "Neurology and Quantum Physics": "Neuroscience",
    "Epistemology": "Philosophy",
    "Metaphysics": "Philosophy",
    "Buddhist_Philosophy": "Philosophy",
    "Philosophy of Art": "Philosophy",
    "Art, Philosophy": "Philosophy",
    "Art & Philosophy": "Philosophy",
    "Philosophy of Daily Life": "Philosophy",
    "Philosophy of Technology": "Philosophy",
    "Technology, Philosophy": "Philosophy",
    "Technology & Philosophy": "Philosophy",
    "Philosophy of Science & Spirituality": "Philosophy",
    "Philosophy of Science": "Philosophy",
    "Philosophy of Science & Nature": "Philosophy",
    "Philosophy of Physics": "Philosophy",
    "Philosophy of Language": "Philosophy",
    "Philosophy of Mind": "Philosophy",
    "Philosophy of Religion": "Philosophy",
    "Philosophy of Law": "Philosophy",
    "Philosophy of Perception & Sound": "Philosophy",
    "Philosophy of Perception & Scent": "Philosophy",
    "Philosophy, Meditation": "Philosophy",
    "Philosophy & Neuroscience": "Philosophy",
    "Philosophy & Psychology": "Philosophy",
    "Metaphysics & Philosophy of Mind": "Philosophy",
    "Literature & Philosophy": "Philosophy",
    "Symbolism, Philosophy": "Philosophy",
    "Science & Philosophy": "Philosophy",
    "Science, Philosophy": "Philosophy",
    "MolecularBiology": "Biology",
    "Genomics": "Biology",
    "Biology, Philosophy": "Biology",
    "Evolutionary Biology": "Biology",
    "Botany": "Biology",
    "Biology & Marketing": "Biology",
    "Biology & Business": "Biology",
    "Biology and Philosophy of Mind": "Biology",
    "Computer Science, Biology": "Computer Science",
    "Cognitive_Science": "Psychology",
    "Cognitive Science": "Psychology",
    "Cognitive Processes": "Psychology",
    "ConsciousnessStudies": "Consciousness",
    "Psychology, Physics": "Psychology",
    "Psychology and Neuroscience": "Psychology",
    "Neuroscience & Philosophy": "Neuroscience",
    "Consciousness & Philosophy": "Consciousness",
    "Climate Ethics": "Ethics",
    "Ethics, Social Science": "Ethics",
    "Ethics & Philosophy of Mind": "Ethics",
    "Law and Business Ethics": "Ethics",
    "Law and Philosophy": "Philosophy",
    "Philanthropy": "Ethics",
    "Project Management, Ethics": "Ethics",
    "Project Management, Philosophy": "Philosophy",
    "Artificial Intelligence": "Computer Science",
    "AI": "Computer Science",
    "Computer Science, Philosophy": "Computer Science",
    "Science & Technology": "Computer Science",
    "Technology & Society": "Sociology",
    "Politics and Law": "Sociology",
    "Governance": "Sociology",
    "Communication": "Sociology",
    "Cultural Movement": "Sociology",
    "Creativity, Collaboration": "Sociology",
    "Food & Language": "Sociology",
    "Project Management": "Sociology",
    "Project Management, Governance": "Sociology",
    "Project Financing": "Economics",
    "Linguistics": "Philosophy",
    "Knowledge Management": "Sociology",
    "Buddhism": "Spirituality",
    "Biomysticism": "Philosophy",
    "Quantum Physics & Philosophy": "Physics",
    "Philosophy, Religion, Physics": "Philosophy",
    "Neuroscience & Quantum Physics": "Neuroscience",
    "Philosophy, Psychology": "Philosophy",
    "Philosophy, Consciousness": "Philosophy",
    "Astrobiology": "Biology",
    "Philosophy/Quantum Physics": "Physics",
    "Metaphysics & Philosophy": "Philosophy",
    "Neuroscience/Philosophy": "Neuroscience",
    "Genetics": "Biology",
    "Quantum Physics": "Physics",
    "Thermodynamics": "Physics",
    "Geology": "Physics",
    "Biochemistry": "Chemistry",
    "Environmental Science": "Ecology",
    "Microbiology": "Biology",
    "Earth Sciences": "Physics",
    "Cell Biology": "Biology",
    "Science": "Philosophy",
    "Cell Biology, Physiology": "Biology",
    "Chemistry & Biology": "Chemistry",
    "Molecular Biology, Genetics": "Biology",
    "Neuroscience, Chemistry, Psychology": "Neuroscience",
    "Physics & Atmospheric Science": "Physics",
}

# Domain display names
DOMAIN_DISPLAY = {
    "Physics": "Physics",
    "Philosophy": "Philosophy",
    "Biology": "Biology",
    "Mathematics": "Mathematics",
    "Consciousness": "Consciousness Studies",
    "Chemistry": "Chemistry",
    "Ethics": "Ethics",
    "Computer Science": "Computer Science",
    "Psychology": "Psychology",
    "Spirituality": "Spirituality",
    "Neuroscience": "Neuroscience",
    "Sociology": "Sociology",
    "Economics": "Economics",
    "Ecology": "Ecology",
    "Medicine": "Medicine",
}

RELATIONSHIP_LABELS = {
    "builds_upon": "Builds Upon",
    "related_to": "Related To",
    "specializes": "Specializes",
    "contradicts": "Contradicts",
}


def normalize_domain(domain):
    """Map raw domain to canonical 15-domain taxonomy."""
    if domain in CANONICAL_DOMAINS:
        return domain
    return DOMAIN_UPWARD_MAP.get(domain, domain)


def gather_public_concepts():
    """Load all concepts, return public-facing data with domain info."""
    all_cids = load_all_concept_cids()
    concepts = []
    domain_counts = Counter()
    subdomain_index = {}

    for cid in all_cids:
        concept = load_concept(cid)
        if 'error' in concept:
            continue

        hid = concept.get('human_id', '')
        title = concept.get('title', hid.replace('_', ' ').title())
        raw_domain = concept.get('domain', 'Unknown')
        canonical = normalize_domain(raw_domain)
        definition = concept.get('definition', '')
        rels = concept.get('relationships', {})
        extra = concept.get('extra_fields', {})

        domain_counts[canonical] += 1

        if canonical not in subdomain_index:
            subdomain_index[canonical] = set()
        subdomain_index[canonical].add(raw_domain)

        concepts.append({
            "human_id": hid,
            "title": title,
            "domain": raw_domain,
            "canonical_domain": canonical,
            "domain_display": DOMAIN_DISPLAY.get(canonical, canonical.replace('_', ' ')),
            "definition": definition,
            "poetic_version": extra.get("poetic_version", ""),
            "mantra": extra.get("mantra", ""),
            "insight": extra.get("insight", ""),
            "cid": cid,
            "relationships": {
                "builds_upon": [r for r in rels.get("builds_upon", []) if isinstance(r, str)],
                "related_to": [r for r in rels.get("related_to", []) if isinstance(r, str)],
                "specializes": [r for r in rels.get("specializes", []) if isinstance(r, str)],
                "contradicts": [r for r in rels.get("contradicts", []) if isinstance(r, str)],
            },
        })

    id_to_title = {c["human_id"]: c["title"] for c in concepts}

    for c in concepts:
        filtered_rels = {}
        for rel_type, targets in c["relationships"].items():
            filtered_rels[rel_type] = [
                {"id": t, "title": id_to_title.get(t, t)}
                for t in targets
                if t in id_to_title
            ]
        c["relationships"] = filtered_rels

    subdomain_index = {k: sorted(v) for k, v in subdomain_index.items()}

    return sorted(concepts, key=lambda c: c["title"]), domain_counts, subdomain_index


def escape_html(text):
    """Escape text for safe HTML embedding."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_card(concept):
    """Build a single concept card with expandable detail."""
    hid = concept["human_id"]
    title = escape_html(concept["title"])
    domain = concept["domain"]
    canonical_domain = concept["canonical_domain"]
    domain_display = escape_html(concept["domain_display"])
    definition = escape_html(concept["definition"])
    domain_class = canonical_domain.lower().replace(" ", "-").replace("_", "-")

    rel_html_parts = []
    for rel_type in ["builds_upon", "related_to", "specializes", "contradicts"]:
        targets = concept["relationships"].get(rel_type, [])
        if targets:
            label = RELATIONSHIP_LABELS.get(rel_type, rel_type)
            tags = "".join(f'<span class="rel-tag rel-{rel_type}">{escape_html(t["title"])}</span>' for t in targets)
            rel_html_parts.append(f'<div class="rel-group"><strong>{label}:</strong> {tags}</div>')
    rel_html = "".join(rel_html_parts) if rel_html_parts else '<p class="no-rels"><em>No relationships recorded yet.</em></p>'

    extras = []
    if concept.get("insight"):
        extras.append(f'<div class="extra-section"><strong>Core Insight:</strong> {escape_html(concept["insight"])}</div>')
    if concept.get("poetic_version"):
        poetic = escape_html(concept["poetic_version"]).replace("\n", "<br>")
        extras.append(f'<div class="extra-section poetic"><strong>Poetic Version:</strong><blockquote>{poetic}</blockquote></div>')
    if concept.get("mantra"):
        extras.append(f'<div class="extra-section mantra"><strong>Mantra:</strong> <em>"{escape_html(concept["mantra"])}"</em></div>')
    extras_html = "".join(extras)

    return f'''
    <article class="concept-card" data-domain="{escape_html(canonical_domain)}" data-raw-domain="{escape_html(domain)}" data-search="{title.lower()} {domain_display.lower()} {hid.lower()}">
        <div class="card-header" onclick="this.parentElement.classList.toggle('expanded')">
            <span class="domain-badge domain-{domain_class}">{domain_display}</span>
            <h2>{title}</h2>
            <p class="definition-preview">{definition[:250]}{'...' if len(definition) > 250 else ''}</p>
            <span class="expand-hint">Click to expand ↓</span>
        </div>
        <div class="card-detail">
            <div class="definition-full">
                <p>{definition}</p>
            </div>
            {extras_html}
            <div class="relationships">
                <h3>Relationships</h3>
                {rel_html}
            </div>
            <div class="cid-box">
                <strong>Permanent CID:</strong><br>
                <code>{concept["cid"]}</code>
            </div>
        </div>
    </article>'''


def build_index_page(concepts, domain_counts, subdomain_index):
    """Build the single-page public gateway."""
    cards = [build_card(c) for c in concepts]

    domain_filters = []
    for d in CANONICAL_DOMAINS:
        count = domain_counts.get(d, 0)
        if count > 0:
            display = DOMAIN_DISPLAY.get(d, d)
            domain_filters.append(f'<button class="filter-btn" data-filter="{d}">{display} ({count})</button>')

    total_edges = sum(
        sum(len(targets) for targets in c["relationships"].values())
        for c in concepts
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CADMIES Mycelium — Public Knowledge Graph</title>
    <meta name="description" content="A decentralized knowledge graph of {len(concepts)} interconnected scientific and philosophical concepts. Content-addressed, open-source, forever.">
    <meta name="robots" content="index, follow">
    <link rel="sitemap" type="application/xml" href="sitemap.xml">
    <link rel="alternate" type="application/json" href="concepts.json">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0d1117; color: #c9d1d9; line-height: 1.6; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #161b22 0%, #0d1117 100%); border-bottom: 1px solid #30363d; padding: 50px 20px 40px; text-align: center; }}
        .header-content {{ display: flex; align-items: center; justify-content: center; gap: 12px; flex-wrap: wrap; }}
        header h1 {{ font-size: 2.4em; color: #e6edf3; margin: 0; }}
        .header-sprout {{ font-size: 2.4em; line-height: 1; }}
        .header-subtitle {{ color: #8b949e; font-size: 1.05em; max-width: 600px; margin: 8px auto 20px; }}
        .translate-toggle {{ display: inline-flex; align-items: center; gap: 6px; background: transparent; border: 1px solid #30363d; border-radius: 6px; padding: 4px 12px; font-size: 0.9em; color: #8b949e; cursor: pointer; transition: all 0.2s ease; font-family: inherit; line-height: 1.5; margin-right: 4px; }}
        .translate-toggle:hover {{ color: #c9d1d9; border-color: #58a6ff; }}
        .translate-toggle.active {{ border-color: #58a6ff; color: #58a6ff; }}
        .translate-toggle .icon {{ font-size: 1em; }}
        #translate-select {{ background: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; border-radius: 6px !important; padding: 4px 8px !important; font-size: 0.85em !important; font-family: inherit !important; }}
        #translate-select option {{ background: #161b22; color: #c9d1d9; }}
        .map-link {{ display: inline-block; margin-top: 12px; padding: 10px 24px; background: #238636; color: #ffffff; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.95em; transition: background 0.2s; }}
        .map-link:hover {{ background: #2ea043; }}
        .stats {{ display: flex; gap: 20px; justify-content: center; margin: 24px 0 0; flex-wrap: wrap; }}
        .stat {{ background: #161b22; border: 1px solid #30363d; padding: 14px 24px; border-radius: 8px; }}
        .stat-number {{ font-size: 1.6em; font-weight: bold; color: #e6edf3; }}
        .stat-label {{ font-size: 0.8em; color: #8b949e; }}
        .stat-orcid .stat-number {{ font-size: 1.0em; font-weight: 600; color: #58a6ff; }}
        .stat-orcid .stat-label {{ display: flex; align-items: center; gap: 6px; justify-content: center; }}
        .stat-orcid .stat-label svg {{ width: 18px; height: 18px; fill: #58a6ff; }}
        .search-bar {{ margin: 24px 0; }}
        .search-bar input {{ width: 100%; padding: 12px 18px; background: #161b22; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; font-size: 1em; outline: none; }}
        .search-bar input:focus {{ border-color: #58a6ff; }}
        .search-bar input::placeholder {{ color: #484f58; }}
        .filters {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 8px; }}
        .filter-btn {{ background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 14px; border-radius: 20px; cursor: pointer; font-size: 0.85em; transition: all 0.2s; }}
        .filter-btn:hover {{ background: #30363d; }}
        .filter-btn.active {{ background: #58a6ff; color: #ffffff; border-color: #58a6ff; }}
        .subdomain-row {{ display: none; flex-wrap: wrap; gap: 6px; margin: 4px 0 12px; padding-left: 4px; }}
        .subdomain-row.visible {{ display: flex; }}
        .subdomain-btn {{ background: #1c2333; border: 1px solid #30363d; color: #8b949e; padding: 4px 12px; border-radius: 16px; cursor: pointer; font-size: 0.75em; transition: all 0.2s; }}
        .subdomain-btn:hover {{ background: #30363d; color: #c9d1d9; }}
        .subdomain-btn.active {{ background: #58a6ff; color: #ffffff; border-color: #58a6ff; }}
        .subdomain-label {{ color: #484f58; font-size: 0.75em; margin-right: 4px; align-self: center; }}
        .concept-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }}
        .concept-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px; overflow: hidden; transition: border-color 0.2s; }}
        .concept-card:hover {{ border-color: #58a6ff; }}
        .concept-card.hidden {{ display: none; }}
        .card-header {{ padding: 20px; cursor: pointer; user-select: none; }}
        .card-header h2 {{ font-size: 1.15em; color: #e6edf3; margin-bottom: 6px; }}
        .definition-preview {{ color: #8b949e; font-size: 0.9em; }}
        .expand-hint {{ display: block; font-size: 0.75em; color: #484f58; margin-top: 10px; }}
        .card-detail {{ display: none; padding: 0 20px 20px; border-top: 1px solid #30363d; }}
        .concept-card.expanded .card-detail {{ display: block; }}
        .concept-card.expanded .expand-hint {{ display: none; }}
        .definition-full {{ margin: 16px 0; padding: 16px; background: #0d1117; border-radius: 8px; border: 1px solid #21262d; }}
        .definition-full p {{ color: #c9d1d9; font-size: 0.95em; }}
        .relationships {{ margin: 16px 0; }}
        .relationships h3 {{ font-size: 0.9em; color: #8b949e; margin-bottom: 10px; }}
        .rel-group {{ margin: 8px 0; font-size: 0.85em; color: #8b949e; }}
        .rel-group strong {{ color: #c9d1d9; }}
        .rel-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; margin: 2px 4px 2px 0; }}
        .rel-builds_upon {{ background: #1b3a1b; color: #7ee787; }}
        .rel-related_to {{ background: #1b2d4a; color: #79c0ff; }}
        .rel-specializes {{ background: #2d1b3a; color: #d2a8ff; }}
        .rel-contradicts {{ background: #3a1b1b; color: #ff7b72; }}
        .no-rels {{ color: #484f58; font-style: italic; font-size: 0.85em; }}
        .extra-section {{ margin: 12px 0; font-size: 0.9em; color: #c9d1d9; }}
        .extra-section strong {{ color: #e6edf3; }}
        .poetic blockquote {{ border-left: 3px solid #58a6ff; padding-left: 14px; color: #8b949e; font-style: italic; margin: 8px 0; }}
        .mantra em {{ color: #d2a8ff; }}
        .cid-box {{ margin: 16px 0; padding: 12px; background: #0d1117; border-radius: 6px; font-size: 0.8em; color: #8b949e; }}
        .cid-box code {{ word-break: break-all; color: #484f58; }}
        .domain-badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.72em; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .domain-physics {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-philosophy {{ background: #2d1b3a; color: #d2a8ff; }}
        .domain-biology {{ background: #1b3a1b; color: #7ee787; }}
        .domain-mathematics {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-ethics {{ background: #3a1b2d; color: #ff9bce; }}
        .domain-psychology {{ background: #1b3a2d; color: #7ee787; }}
        .domain-chemistry {{ background: #3a361b; color: #e3b341; }}
        .domain-consciousness {{ background: #21262d; color: #c9d1d9; }}
        .domain-computer-science {{ background: #1b2d4a; color: #79c0ff; }}
        .domain-spirituality {{ background: #2d1b3a; color: #d2a8ff; }}
        .domain-neuroscience {{ background: #1b3a2d; color: #7ee787; }}
        .domain-sociology {{ background: #3a1b2d; color: #ff9bce; }}
        .domain-economics {{ background: #3a361b; color: #e3b341; }}
        .domain-ecology {{ background: #1b3a1b; color: #7ee787; }}
        .domain-medicine {{ background: #1b3a1b; color: #7ee787; }}
        footer {{ text-align: center; padding: 40px 20px; color: #484f58; font-size: 0.85em; border-top: 1px solid #30363d; margin-top: 40px; }}
        footer a {{ color: #58a6ff; text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}
        .footer-privacy {{ font-size: 0.85em; color: #484f58; margin-top: 8px; }}
        .results-count {{ color: #8b949e; font-size: 0.85em; margin: 4px 0 16px; }}
        @media (max-width: 640px) {{ .concept-grid {{ grid-template-columns: 1fr; }} header h1 {{ font-size: 1.6em; }} .stats {{ gap: 10px; }} .stat {{ padding: 10px 16px; }} .header-content {{ gap: 8px; }} .translate-toggle {{ font-size: 0.8em; padding: 3px 10px; }} }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <button class="translate-toggle" id="translateToggle" onclick="toggleTranslation()">
                    <span class="icon">🌐</span> <span id="toggleLabel">Translate</span>
                </button>
                <span class="header-sprout">🌱</span>
                <h1>CADMIES</h1>
            </div>
            <p class="header-subtitle">A decentralized knowledge graph of interconnected scientific and philosophical concepts.<br>Content-addressed. Open-source. Forever.</p>
            <a href="mycelium_map.html" class="map-link">Explore the Interactive Mycelium Map</a>
            <div class="stats">
                <div class="stat"><div class="stat-number">{len(concepts)}</div><div class="stat-label">Concepts</div></div>
                <div class="stat"><div class="stat-number">{len(domain_counts)}</div><div class="stat-label">Domains</div></div>
                <div class="stat"><div class="stat-number">{total_edges}</div><div class="stat-label">Relationships</div></div>
                <div class="stat"><div class="stat-number">CC BY-SA 4.0</div><div class="stat-label">License</div></div>
                <div class="stat stat-orcid">
                    <div class="stat-number">0009-0000-8877-2731</div>
                    <div class="stat-label">
                        <svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
                            <path d="M256 128c0 70.686-57.314 128-128 128C57.314 256 0 198.686 0 128 0 57.314 57.314 0 128 0c70.686 0 128 57.314 128 128z" fill="#A6CE39"/>
                            <path d="M86.4 106.4h25.6v43.2H86.4zM86.4 86.4h25.6v12.8H86.4z" fill="#fff"/>
                            <path d="M130.4 106.4h25.6v43.2h-25.6zM130.4 86.4h25.6v12.8h-25.6z" fill="#fff"/>
                            <path d="M174.4 106.4h12.8v43.2h-12.8zM174.4 86.4h12.8v12.8h-12.8z" fill="#fff"/>
                        </svg>
                        ORCID iD
                    </div>
                </div>
            </div>
        </div>
    </header>
    <main class="container">
        <div class="search-bar">
            <input type="text" id="search" placeholder="Search concepts..." oninput="filterConcepts()">
        </div>
        <div class="filters" id="filters">
            <button class="filter-btn active" data-filter="all">All ({len(concepts)})</button>
            {''.join(domain_filters)}
        </div>
        <div class="subdomain-row" id="subdomainRow">
            <span class="subdomain-label">Subdomains:</span>
        </div>
        <div class="results-count" id="resultsCount">Showing {len(concepts)} of {len(concepts)} concepts</div>
        <div class="concept-grid" id="conceptGrid">
            {''.join(cards)}
        </div>
    </main>
    <footer>
        <div class="container">
            <p>CADMIES — Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem</p>
            <p>All concepts licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. Each concept has a permanent CID (Content Identifier) — the hash proves nothing was altered.</p>
            <p><a href="sitemap.xml">Sitemap</a> · <a href="concepts.json">JSON Feed</a> · <a href="https://github.com/Project-Hierion/Hierion-CADMIES">GitHub</a></p>
            <p class="footer-privacy">🌐 Translation powered by <a href="https://translate.zvo.cn" target="_blank" rel="noopener noreferrer">translate.js</a> — all processing occurs client-side. No data is sent to CADMIES servers.</p>
        </div>
    </footer>
    <script>
        let currentFilter = 'all';
        const totalConcepts = {len(concepts)};
        let translationActive = false;

        function toggleTranslation() {{
            if (!translationActive) {{
                if (typeof translate === 'undefined') {{
                    const script = document.createElement('script');
                    script.src = 'https://cdn.staticfile.net/translate.js/3.15.6/translate.min.js';
                    script.onload = function() {{
                        translate.execute();
                        translationActive = true;
                        updateToggleUI(true);
                        try {{ localStorage.setItem('translateActive', 'true'); }} catch(e) {{}}
                    }};
                    document.head.appendChild(script);
                }} else {{
                    translate.execute();
                    translationActive = true;
                    updateToggleUI(true);
                    try {{ localStorage.setItem('translateActive', 'true'); }} catch(e) {{}}
                }}
            }} else {{
                if (typeof translate !== 'undefined' && translate.reset) {{
                    translate.reset();
                }} else {{
                    location.reload();
                }}
                translationActive = false;
                updateToggleUI(false);
                try {{ localStorage.setItem('translateActive', 'false'); }} catch(e) {{}}
            }}
        }}

        function updateToggleUI(active) {{
            const btn = document.getElementById('translateToggle');
            const label = document.getElementById('toggleLabel');
            if (active) {{
                btn.classList.add('active');
                label.textContent = 'English';
            }} else {{
                btn.classList.remove('active');
                label.textContent = 'Translate';
            }}
        }}

        (function() {{
            try {{
                const saved = localStorage.getItem('translateActive');
                if (saved === 'true') {{
                    setTimeout(function() {{
                        if (typeof translate !== 'undefined') {{
                            translate.execute();
                            translationActive = true;
                            updateToggleUI(true);
                        }} else {{
                            const script = document.createElement('script');
                            script.src = 'https://cdn.staticfile.net/translate.js/3.15.6/translate.min.js';
                            script.onload = function() {{
                                translate.execute();
                                translationActive = true;
                                updateToggleUI(true);
                            }};
                            document.head.appendChild(script);
                        }}
                    }}, 500);
                }}
            }} catch(e) {{ }}
        }})();

        document.addEventListener('translateLanguageChange', function(e) {{
            if (e.detail && e.detail.language) {{
                const label = document.getElementById('toggleLabel');
                label.textContent = e.detail.language;
                document.getElementById('translateToggle').classList.add('active');
            }}
        }});

        function setFilter(filter, btn) {{
            currentFilter = filter;
            document.querySelectorAll('#filters .filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('subdomainRow').classList.remove('visible');
            filterConcepts();
        }}

        function filterConcepts() {{
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const cards = document.querySelectorAll('.concept-card');
            let visible = 0;

            cards.forEach(card => {{
                const domain = card.dataset.domain;
                const searchData = card.dataset.search;
                const matchesFilter = currentFilter === 'all' || domain === currentFilter;
                const matchesSearch = searchData.includes(searchTerm);
                if (matchesFilter && matchesSearch) {{
                    card.classList.remove('hidden');
                    visible++;
                }} else {{
                    card.classList.add('hidden');
                }}
            }});

            document.getElementById('resultsCount').textContent = 'Showing ' + visible + ' of ' + totalConcepts + ' concepts';
        }}

        document.querySelectorAll('#filters .filter-btn').forEach(function(btn) {{
            btn.addEventListener('click', function() {{
                var filter = this.dataset.filter;
                setFilter(filter, this);
            }});
        }});

        document.getElementById('search').addEventListener('input', filterConcepts);
    </script>
</body>
</html>'''


def build_json_feed(concepts):
    """Build a JSON-LD structured data feed with domain info."""
    items = []
    for c in concepts:
        items.append({
            "@type": "DefinedTerm",
            "name": c["title"],
            "description": c["definition"],
            "termCode": c["cid"],
            "inDefinedTermSet": {
                "@type": "DefinedTermSet",
                "name": "CADMIES Mycelium",
            },
            "url": f"{SITE_URL}/index.html#{c['human_id']}",
            "domain": c["domain"],
            "canonical_domain": c["canonical_domain"],
        })
    return json.dumps({"@context": "https://schema.org", "@graph": items}, indent=2)


def build_sitemap(concepts):
    """Build XML sitemap for search engines."""
    urls = [f'<url><loc>{SITE_URL}/index.html</loc></url>']
    for c in concepts:
        urls.append(f'<url><loc>{SITE_URL}/index.html#{c["human_id"]}</loc></url>')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''


def main():
    print("=" * 60)
    print(f"CADMIES PUBLIC MYCELIUM GATEWAY GENERATOR v{VERSION}")
    print(f"Output: {OUTPUT_DIR}")
    print("translate.js integration: ENABLED (client-side, privacy-respecting)")
    print("=" * 60)

    concepts, domain_counts, subdomain_index = gather_public_concepts()
    total_edges = sum(
        sum(len(targets) for targets in c["relationships"].values())
        for c in concepts
    )
    print(f"\nLoaded {len(concepts)} concepts across {len(domain_counts)} canonical domains with {total_edges} edges")
    print(f"Subdomain index: {len(subdomain_index)} canonical domains with subdomains")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating index.html (single-page gateway with translate.js)...")
    index_html = build_index_page(concepts, domain_counts, subdomain_index)
    with open(OUTPUT_DIR / "index.html", "w") as f:
        f.write(index_html)

    print("Generating concepts.json (structured data with domain fields)...")
    json_feed = build_json_feed(concepts)
    with open(OUTPUT_DIR / "concepts.json", "w") as f:
        f.write(json_feed)

    print("Generating sitemap.xml...")
    sitemap = build_sitemap(concepts)
    with open(OUTPUT_DIR / "sitemap.xml", "w") as f:
        f.write(sitemap)

    nojekyll = OUTPUT_DIR / ".nojekyll"
    if not nojekyll.exists():
        nojekyll.touch()

    print(f"\nPublic gateway generated: {OUTPUT_DIR}")
    print(f"   index.html — single-page app with {len(concepts)} concept cards")
    print(f"   concepts.json — JSON-LD structured data with domain fields")
    print(f"   sitemap.xml — search engine sitemap")
    print(f"   .nojekyll — bypass Jekyll processing")
    print(f"\nDomain filter pills now functional. Click a domain to filter cards.")
    print(f"   Subdomain tier is designed but not yet implemented.")
    print(f"\ntranslate.js integration:")
    print(f"   Toggle left of CADMIES title — click to activate client-side translation")
    print(f"   Language preference stored in localStorage")
    print(f"   All processing occurs client-side — no data sent to CADMIES servers")
    print(f"\nDeploy: push to GitHub, Pages serves from /docs folder")


if __name__ == "__main__":
    main()
