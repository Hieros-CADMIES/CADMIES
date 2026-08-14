#!/usr/bin/env python3
"""
File: generate_public_gateway.py
Tool: CADMIES Public Mycelium Gateway Generator
Version: 3.3.0
System: CADMIES / tools
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Generates the public-facing CADMIES mycelium website.

         Reads concept data from the blockstore and writes:
           - index.html  (new single-page app: splash, dashboard, browse)
           - concepts.json (Schema.org JSON-LD, includes relationships)
           - sitemap.xml (SEO sitemap)

         Concept cards are rendered client-side from concepts.json
         by docs/app.js. Styling lives in docs/style.css and
         docs/splash.css. This generator owns the data layer and
         the HTML shell. The hand-maintained design files are not
         overwritten.

         No personal information. No internal tooling references.
         Just the knowledge the mycelium wants to share with the world.

Usage:
    python tools/generate_public_gateway.py

Output:
    ../docs/ — static site served by web server

Version History:
  v3.3.0 (2026-08-14): Rewrote generator for new site design.
      index.html now uses the new app shell (splash, dashboard, browse).
      Concept cards render client-side from concepts.json via app.js.
      Added relationships and extra fields to concepts.json JSON-LD.
      Sitemap now references the root page and section anchors.
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

VERSION = "3.3.0"
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
    "Quantum Physics and Philosophy": "Physics",
    "Physics and Philosophy": "Physics",
    "Physics & Philosophy": "Physics",
    "Physics, Philosophy": "Physics",
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


def build_index_page(concepts, domain_counts, subdomain_index):
    """Build the new single-page app shell.

    The app shell contains the splash screen, dashboard, navigation,
    and empty browse grid. Concept cards are rendered client-side by
    app.js from concepts.json. This function does NOT pre-bake cards.
    """
    total_edges = sum(
        sum(len(targets) for targets in c["relationships"].values())
        for c in concepts
    )

    domain_filter_buttons = []
    for d in CANONICAL_DOMAINS:
        count = domain_counts.get(d, 0)
        if count > 0:
            display = DOMAIN_DISPLAY.get(d, d)
            domain_filter_buttons.append(
                f'<button class="filter-btn" data-filter="{d}">{display} ({count})</button>'
            )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CADMIES — Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem</title>
    <meta name="description" content="A decentralized knowledge graph of {len(concepts)} interconnected scientific and philosophical concepts. Content-addressed. Open-source. Forever." />
    <link rel="icon" type="image/png" href="favicon.png" />

    <link rel="stylesheet" href="splash.css" />
    <link rel="stylesheet" href="style.css" />

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet" />

    <style>
        .translate-controls {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-top: 8px;
            flex-wrap: wrap;
        }}
        .translate-toggle {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 6px;
            padding: 6px 16px;
            font-size: 0.9em;
            color: #94A3B8;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
            line-height: 1.5;
        }}
        .translate-toggle:hover {{
            color: #FFFFFF;
            border-color: #4F46E5;
        }}
        .translate-toggle.active {{
            border-color: #4F46E5;
            color: #4F46E5;
        }}
        #translate-select {{
            background: rgba(255, 255, 255, 0.06) !important;
            color: #E2E8F0 !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 6px !important;
            padding: 6px 12px !important;
            font-size: 0.9em !important;
            font-family: 'Inter', sans-serif !important;
            cursor: pointer;
            outline: none;
            display: none;
        }}
        #translate-select:hover {{
            border-color: #4F46E5 !important;
        }}
        #translate-select option {{
            background: #1E1B4B;
            color: #E2E8F0;
        }}
        #translate-select.visible {{
            display: inline-block;
        }}
        .footer-privacy {{
            font-size: 0.85em;
            color: #484f58;
            margin-top: 8px;
        }}
    </style>
</head>
<body>

    <!-- SPLASH SCREEN -->
    <div id="splash-overlay">
        <div id="splash-content">
            <div class="splash-emoji">🌱</div>
            <h1 class="splash-title">CADMIES</h1>
            <p class="splash-subtitle">Cosmium Angelo Digital Mycorrhizal<br />Intelligence EcoSystem</p>
            <div class="splash-divider"></div>
            <p class="splash-message">The mycelium awaits you.</p>
        </div>
    </div>

    <!-- MAIN APP -->
    <div id="app" class="hidden">

        <!-- DASHBOARD -->
        <section id="page-dashboard" class="page active">
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <div class="header-center">
                        <div class="header-title">
                            <span class="header-emoji">🌱</span>
                            <h1>CADMIES</h1>
                        </div>
                        <div class="header-tagline">Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem</div>
                        <div class="translate-controls">
                            <button class="translate-toggle" id="translateToggle" onclick="toggleTranslate()">
                                <span class="icon">🌐</span> <span>Translate</span>
                            </button>
                            <select id="translate-select" onchange="handleLanguageChange(this.value)">
                                <option value="">Select Language</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="stats-grid" id="stats-grid">
                    <div class="stat-card" data-stat="concepts">
                        <div class="stat-number" id="stat-concepts">{len(concepts)}</div>
                        <div class="stat-label">Concepts</div>
                    </div>
                    <div class="stat-card" data-stat="domains">
                        <div class="stat-number" id="stat-domains">{len(domain_counts)}</div>
                        <div class="stat-label">Domains</div>
                    </div>
                    <div class="stat-card" data-stat="relationships">
                        <div class="stat-number" id="stat-relationships">{total_edges}</div>
                        <div class="stat-label">Relationships</div>
                    </div>
                    <div class="stat-card" data-stat="license">
                        <div class="stat-number">AGPLv3</div>
                        <div class="stat-label">License</div>
                    </div>
                    <div class="stat-card stat-orcid" data-stat="orcid">
                        <a href="https://orcid.org/0009-0000-8877-2731" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit;">
                            <div class="stat-number">0009-0000-8877-2731</div>
                            <div class="stat-label">ORCID iD</div>
                        </a>
                    </div>
                </div>

                <div class="nav-grid">
                    <div class="nav-card" data-page="mistral">
                        <div class="nav-card-icon">👩‍🏫</div>
                        <h3>Dr. Mistral</h3>
                        <p>Chat with Dr. Mistral</p>
                    </div>
                    <div class="nav-card" data-page="browse">
                        <div class="nav-card-icon">📚</div>
                        <h3>Browse The Mycelium Library</h3>
                        <p>Explore concepts in the library</p>
                    </div>
                    <div class="nav-card" data-page="add">
                        <div class="nav-card-icon">➕</div>
                        <h3>Add Concept</h3>
                        <p>Nourish the network.</p>
                    </div>
                    <div class="nav-card" data-page="map">
                        <div class="nav-card-icon">🕸️</div>
                        <h3>Mycelium Map</h3>
                        <p>See the connections!</p>
                    </div>
                </div>

                <div class="dashboard-footer">
                    <span>Let the mycelium grow! 🌱</span>
                </div>

                <div class="referral-footer">
                    <a href="https://www.digitalocean.com/?refcode=fd70c6e2650a&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge" target="_blank" rel="noopener noreferrer">
                        <img src="https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg" alt="DigitalOcean Referral Badge" />
                    </a>
                    <a href="https://cape.co/get-cape?referral=ZCWW60AA" target="_blank" rel="noopener noreferrer">Cape Wireless</a>
                    <a href="https://app.spheron.ai/signup?ref=ENXyV3608" target="_blank" rel="noopener noreferrer">Spheron AI</a>
                </div>

                <div class="footer-privacy" style="text-align:center;padding:12px 20px;max-width:900px;margin:0 auto;border-top:1px solid rgba(255,255,255,0.06);">
                    🌐 Translation powered by <a href="https://translate.zvo.cn" target="_blank" rel="noopener noreferrer" style="color:#58a6ff;text-decoration:none;">translate.js</a> — all processing occurs client-side. No data is sent to CADMIES servers.
                </div>
            </div>
        </section>

        <!-- DR MISTRAL -->
        <section id="page-mistral" class="page">
            <div class="full-page-container">
                <div class="full-page-header">
                    <button class="back-btn" data-page="dashboard">← Back to Dashboard</button>
                    <h2>👩‍🏫 Dr. Mistral</h2>
                    <p class="page-subtitle">Madame La Professeure de CADMIES</p>
                </div>
                <div class="chat-container">
                    <div class="chat-display" id="chat-display">
                        <div class="chat-message system">
                            <span class="msg-label">Dr. Mistral:</span>
                            <span class="msg-text">Bonjour, mon ami. I am Dr. Amanda Mistral. Ask me anything about the mycelium, and I shall consult the library.</span>
                        </div>
                    </div>
                    <div class="chat-controls">
                        <div class="control-group">
                            <label>Model</label>
                            <select id="chat-model">
                                <option value="tinyllama:1.1b">TinyLlama (Fast)</option>
                                <option value="mistral:7b" selected>Mistral (Deep)</option>
                            </select>
                        </div>
                        <div class="control-group">
                            <label>Tone</label>
                            <select id="chat-tone">
                                <option value="helpful">Helpful</option>
                                <option value="scholarly">Scholarly</option>
                                <option value="casual">Casual</option>
                                <option value="french" selected>French</option>
                            </select>
                        </div>
                        <div class="control-group">
                            <label>Max Concepts</label>
                            <select id="chat-max">
                                <option value="3">3</option>
                                <option value="5" selected>5</option>
                                <option value="10">10</option>
                                <option value="20">20</option>
                                <option value="all">All</option>
                            </select>
                        </div>
                    </div>
                    <div class="chat-input-area">
                        <input type="text" id="chat-input" placeholder="Ask Dr. Mistral about the mycelium..." />
                        <button id="chat-send">Send</button>
                    </div>
                    <div class="chat-status" id="chat-status">🟢 Connected to Dr. Mistral</div>
                </div>
            </div>
        </section>

        <!-- BROWSE -->
        <section id="page-browse" class="page">
            <div class="full-page-container">
                <div class="full-page-header">
                    <button class="back-btn" data-page="dashboard">← Back to Dashboard</button>
                    <h2>📚 Browse The Library</h2>
                    <p class="page-subtitle" id="browse-count">Loading concepts...</p>
                </div>
                <div class="browse-controls">
                    <input type="text" id="browse-search" placeholder="Search concepts..." />
                    <div class="domain-filters" id="browse-filters">
                        <button class="filter-btn active" data-filter="all">All ({len(concepts)})</button>
                        {''.join(domain_filter_buttons)}
                    </div>
                </div>
                <div class="concept-grid" id="browse-grid">
                    <p class="loading-text">Loading concepts...</p>
                </div>
            </div>
        </section>

        <!-- ADD CONCEPT -->
        <section id="page-add" class="page">
            <div class="full-page-container">
                <div class="full-page-header">
                    <button class="back-btn" data-page="dashboard">← Back to Dashboard</button>
                    <h2>➕ Add A Concept</h2>
                    <p class="page-subtitle">Submit a new concept to the mycelium.</p>
                </div>
                <form id="add-form" class="add-form">
                    <div class="form-section">
                        <h4>Required</h4>
                        <label>Human ID <span class="required">*</span>
                            <input type="text" id="add-human-id" placeholder="snake_case_identifier" required />
                        </label>
                        <label>Title <span class="required">*</span>
                            <input type="text" id="add-title" placeholder="Concept Title" required />
                        </label>
                        <label>Definition <span class="required">*</span>
                            <textarea id="add-definition" rows="3" placeholder="Clear 1–3 sentence definition"></textarea>
                        </label>
                        <label>Domain <span class="required">*</span>
                            <select id="add-domain">
                                <option value="Philosophy">Philosophy</option>
                                <option value="Physics">Physics</option>
                                <option value="Biology">Biology</option>
                                <option value="Mathematics">Mathematics</option>
                                <option value="Consciousness">Consciousness</option>
                                <option value="Chemistry">Chemistry</option>
                                <option value="Ethics">Ethics</option>
                                <option value="Computer Science">Computer Science</option>
                                <option value="Psychology">Psychology</option>
                                <option value="Spirituality">Spirituality</option>
                                <option value="Neuroscience">Neuroscience</option>
                                <option value="Sociology">Sociology</option>
                                <option value="Economics">Economics</option>
                                <option value="Ecology">Ecology</option>
                                <option value="Medicine">Medicine</option>
                                <option value="Other">Other</option>
                            </select>
                        </label>
                        <label>Type <span class="required">*</span>
                            <select id="add-type">
                                <option value="PhilosophicalPrinciple">Philosophical Principle</option>
                                <option value="ScientificTheory">Scientific Theory</option>
                                <option value="ScientificLaw">Scientific Law</option>
                                <option value="ScientificHypothesis">Scientific Hypothesis</option>
                                <option value="MetaphysicalConcept">Metaphysical Concept</option>
                                <option value="Other">Other</option>
                            </select>
                        </label>
                    </div>
                    <div class="form-section">
                        <h4>Optional — Enrichment</h4>
                        <label>Mantra <input type="text" id="add-mantra" placeholder="Short memorable phrase" /></label>
                        <label>Poetic Version <input type="text" id="add-poetic" placeholder="One beautiful sentence" /></label>
                        <label>Axioms (one per line)
                            <textarea id="add-axioms" rows="3" placeholder="Core truths of the concept"></textarea>
                        </label>
                        <label>Genesis (origin story)
                            <textarea id="add-genesis" rows="2" placeholder="How this concept came to be"></textarea>
                        </label>
                    </div>
                    <div class="form-section">
                        <h4>Optional — Relationships</h4>
                        <label>Builds Upon <input type="text" id="add-builds" placeholder="human_id, human_id" /></label>
                        <label>Related To <input type="text" id="add-related" placeholder="human_id, human_id" /></label>
                        <label>Contradicts <input type="text" id="add-contradicts" placeholder="human_id, human_id" /></label>
                    </div>
                    <div class="form-section">
                        <h4>Optional — Difficulty Levels</h4>
                        <label>Beginner <textarea id="add-beginner" rows="2" placeholder="Simple explanation"></textarea></label>
                        <label>Intermediate <textarea id="add-intermediate" rows="2" placeholder="Domain-fluent explanation"></textarea></label>
                        <label>Expert <textarea id="add-expert" rows="2" placeholder="Full depth explanation"></textarea></label>
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn-primary">Submit to Mycelium</button>
                        <button type="reset" class="btn-secondary">Reset</button>
                    </div>
                </form>
                <div id="add-result" class="hidden"></div>
            </div>
        </section>

        <!-- MAP -->
        <section id="page-map" class="page">
            <div class="full-page-container">
                <div class="full-page-header">
                    <button class="back-btn" data-page="dashboard">← Back to Dashboard</button>
                    <h2>🕸️ The Mycelium Map</h2>
                    <p class="page-subtitle">Interactive visualization of the CADMIES knowledge network</p>
                </div>
                <div class="map-content">
                    <div class="map-info">
                        <p>The mycelium map is a force-directed graph showing all concepts in the CADMIES knowledge network. Each node is a concept. Each connection is a relationship — builds_upon, related_to, or contradicts.</p>
                        <ul>
                            <li>🔄 Drag nodes to rearrange</li>
                            <li>🔍 Scroll to zoom</li>
                            <li>👆 Hover for concept name</li>
                            <li>🖱️ Click to highlight connections</li>
                        </ul>
                        <div class="map-status" id="map-status">
                            <span class="status-dot">●</span> Checking map file...
                        </div>
                        <button id="map-launch" class="btn-primary">🕸️ Launch The Mycelium Map</button>
                        <p class="map-note">Opens in a new tab. Requires a modern browser with JavaScript enabled.</p>
                    </div>
                </div>
            </div>
        </section>

    </div>

    <script src="app.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/xnx3/translate/translate.js/translate.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            translate.language.setLocal('english');
            translate.execute();
        }});

        let translationActive = false;
        let currentLanguage = '';
        const dropdown = document.getElementById('translate-select');

        function toggleTranslate() {{
            if (typeof translate === 'undefined') {{
                console.warn('translate.js not loaded yet');
                return;
            }}
            if (dropdown.classList.contains('visible')) {{
                dropdown.classList.remove('visible');
            }} else {{
                dropdown.classList.add('visible');
                if (dropdown.options.length <= 1) {{
                    populateLanguages();
                }}
                if (!currentLanguage) {{
                    dropdown.value = '';
                }}
            }}
        }}

        function populateLanguages() {{
            const languages = [
                {{ code: 'en', name: 'English' }},
                {{ code: 'es', name: 'Español' }},
                {{ code: 'fr', name: 'Français' }},
                {{ code: 'de', name: 'Deutsch' }},
                {{ code: 'it', name: 'Italiano' }},
                {{ code: 'pt', name: 'Português' }},
                {{ code: 'ru', name: 'Русский' }},
                {{ code: 'ja', name: '日本語' }},
                {{ code: 'ko', name: '한국어' }},
                {{ code: 'zh-cn', name: '简体中文' }},
                {{ code: 'zh-tw', name: '繁體中文' }},
                {{ code: 'ar', name: 'العربية' }},
                {{ code: 'hi', name: 'हिन्दी' }},
                {{ code: 'bn', name: 'বাংলা' }},
                {{ code: 'pa', name: 'ਪੰਜਾਬੀ' }},
                {{ code: 'ta', name: 'தமிழ்' }},
                {{ code: 'te', name: 'తెలుగు' }},
                {{ code: 'ml', name: 'മലയാളം' }},
                {{ code: 'kn', name: 'ಕನ್ನಡ' }},
                {{ code: 'mr', name: 'मराठी' }},
                {{ code: 'gu', name: 'ગુજરાતી' }},
                {{ code: 'or', name: 'ଓଡ଼ିଆ' }},
                {{ code: 'as', name: 'অসমীয়া' }},
                {{ code: 'mai', name: 'मैथिली' }},
                {{ code: 'sat', name: 'ᱥᱟᱱᱛᱟᱲᱤ' }},
                {{ code: 'th', name: 'ไทย' }},
                {{ code: 'lo', name: 'ລາວ' }},
                {{ code: 'my', name: 'မြန်မာ' }},
                {{ code: 'km', name: 'ខ្មែរ' }},
                {{ code: 'vi', name: 'Tiếng Việt' }},
                {{ code: 'id', name: 'Bahasa Indonesia' }},
                {{ code: 'ms', name: 'Bahasa Melayu' }},
                {{ code: 'tl', name: 'Tagalog' }},
                {{ code: 'pl', name: 'Polski' }},
                {{ code: 'uk', name: 'Українська' }},
                {{ code: 'ro', name: 'Română' }},
                {{ code: 'nl', name: 'Nederlands' }},
                {{ code: 'sv', name: 'Svenska' }},
                {{ code: 'no', name: 'Norsk' }},
                {{ code: 'da', name: 'Dansk' }},
                {{ code: 'fi', name: 'Suomi' }},
                {{ code: 'el', name: 'Ελληνικά' }},
                {{ code: 'tr', name: 'Türkçe' }},
                {{ code: 'he', name: 'עברית' }},
                {{ code: 'fa', name: 'فارسی' }},
                {{ code: 'ur', name: 'اردو' }}
            ];
            dropdown.innerHTML = '<option value="">Select Language</option>';
            languages.forEach(function(lang) {{
                const option = document.createElement('option');
                option.value = lang.code;
                option.textContent = lang.name;
                dropdown.appendChild(option);
            }});
        }}

        function getTranslateLangName(code) {{
            const map = {{
                'en': 'english', 'es': 'spanish', 'fr': 'french', 'de': 'deutsch',
                'it': 'italian', 'pt': 'portuguese', 'ru': 'russian', 'ja': 'japanese',
                'ko': 'korean', 'zh-cn': 'chinese_simplified', 'zh-tw': 'chinese_traditional',
                'ar': 'arabic', 'hi': 'hindi', 'bn': 'bengali', 'pa': 'punjabi',
                'ta': 'tamil', 'te': 'telugu', 'ml': 'malayalam', 'kn': 'kannada',
                'mr': 'marathi', 'gu': 'gujarati', 'or': 'oriya', 'as': 'assamese',
                'mai': 'maithili', 'sat': 'santali', 'th': 'thai', 'lo': 'lao',
                'my': 'burmese', 'km': 'khmer', 'vi': 'vietnamese', 'id': 'indonesian',
                'ms': 'malay', 'tl': 'tagalog', 'pl': 'polish', 'uk': 'ukrainian',
                'ro': 'romanian', 'nl': 'dutch', 'sv': 'swedish', 'no': 'norwegian',
                'da': 'danish', 'fi': 'finnish', 'el': 'greek', 'tr': 'turkish',
                'he': 'hebrew', 'fa': 'persian', 'ur': 'urdu'
            }};
            return map[code] || code;
        }}

        function handleLanguageChange(langCode) {{
            if (!langCode) return;
            currentLanguage = langCode;
            translationActive = true;
            const langName = getTranslateLangName(langCode);
            if (typeof translate !== 'undefined') {{
                translate.changeLanguage(langName);
            }}
            dropdown.classList.remove('visible');
            try {{
                localStorage.setItem('translateLanguage', langCode);
                localStorage.setItem('translateActive', 'true');
            }} catch(e) {{}}
            document.dispatchEvent(new CustomEvent('translateLanguageChange', {{
                detail: {{ language: langCode }}
            }}));
        }}

        function checkSavedLanguage() {{
            try {{
                const savedLang = localStorage.getItem('translateLanguage');
                const savedActive = localStorage.getItem('translateActive');
                if (savedLang && savedActive === 'true') {{
                    currentLanguage = savedLang;
                    translationActive = true;
                    setTimeout(function() {{
                        if (typeof translate !== 'undefined') {{
                            const langName = getTranslateLangName(savedLang);
                            translate.changeLanguage(langName);
                        }}
                    }}, 500);
                }}
            }} catch(e) {{}}
        }}

        function resetTranslation() {{
            if (typeof translate !== 'undefined' && translate.reset) {{
                translate.reset();
            }} else {{
                location.reload();
            }}
            translationActive = false;
            currentLanguage = '';
            dropdown.value = '';
            try {{
                localStorage.setItem('translateActive', 'false');
                localStorage.removeItem('translateLanguage');
            }} catch(e) {{}}
        }}

        setTimeout(checkSavedLanguage, 1000);

        document.addEventListener('translateLanguageChange', function(e) {{
            if (e.detail && e.detail.language) {{
                currentLanguage = e.detail.language;
                translationActive = true;
                try {{
                    localStorage.setItem('translateLanguage', e.detail.language);
                    localStorage.setItem('translateActive', 'true');
                }} catch(e) {{}}
            }}
        }});

        document.addEventListener('click', function(e) {{
            const controls = document.querySelector('.translate-controls');
            if (controls && !controls.contains(e.target)) {{
                dropdown.classList.remove('visible');
            }}
        }});
    </script>
</body>
</html>'''


def build_json_feed(concepts):
    """Build a JSON-LD structured data feed with domain info and relationships."""
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
            "relationships": {
                "builds_upon": [{"id": r["id"], "title": r["title"]} for r in c["relationships"].get("builds_upon", [])],
                "related_to": [{"id": r["id"], "title": r["title"]} for r in c["relationships"].get("related_to", [])],
                "specializes": [{"id": r["id"], "title": r["title"]} for r in c["relationships"].get("specializes", [])],
                "contradicts": [{"id": r["id"], "title": r["title"]} for r in c["relationships"].get("contradicts", [])],
            },
            "extra": {
                "insight": c.get("insight", ""),
                "poetic_version": c.get("poetic_version", ""),
                "mantra": c.get("mantra", ""),
            },
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
    print("App shell + data layer (cards render client-side from concepts.json)")
    print("=" * 60)

    concepts, domain_counts, subdomain_index = gather_public_concepts()
    total_edges = sum(
        sum(len(targets) for targets in c["relationships"].values())
        for c in concepts
    )
    print(f"\nLoaded {len(concepts)} concepts across {len(domain_counts)} canonical domains with {total_edges} edges")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating index.html (app shell)...")
    index_html = build_index_page(concepts, domain_counts, subdomain_index)
    with open(OUTPUT_DIR / "index.html", "w") as f:
        f.write(index_html)

    print("Generating concepts.json (structured data + relationships)...")
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
    print(f"   index.html — app shell with dashboard, browse, translate")
    print(f"   concepts.json — JSON-LD with relationships")
    print(f"   sitemap.xml — search engine sitemap")
    print(f"\nDesign files (style.css, splash.css, app.js) are maintained separately.")
    print(f"Deploy: push to GitHub, Pages serves from /docs folder")


if __name__ == "__main__":
    main()
