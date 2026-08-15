---
pipeline: CADMIES End-to-End Workflows
date: 2026-08-12
status: Living document
related: [[Phase-66-Mycelium-Map-UX-Fractal-Succulent-Layout-and-Progressive-Loading]], [[Phase-63-Cloud-Deployment-Project-Hierion-Foundation]], [[Session-049-2026-08-12-Script-Audit-and-Standardization]]
---

# CADMIES Pipeline Workflows

### Ground Zero: Capture the Conversation
Before anything else, save your conversation to **`tools/harvest/conversation.json`**.
This is the template. This is a spore. Everything downstream flows from this file.

```json
{
  "metadata": {
    "_citation_guidance": "For scientific provenance and proper attribution, complete the fields below. They are optional but we highly advise they be filled in — omitted fields default to internal CADMIES system standards. All entries may be amended later as new source information becomes available.",
    "source_description": "YOUR TEXT HERE",
    "source_url": "YOUR TEXT HERE",
    "author": "YOUR TEXT HERE",
    "license": "YOUR TEXT HERE"
  },
  "content": "YOUR TEXT HERE"
}
``

---

Workflow 1: Full Harvest Pipeline
The complete journey from source conversation to public mycelium map deployment.

text
conversation.json → Harvester → source_concepts/ → Validate → Mint → Blockstore → Relationships → Map → Gateway
Commands
Prepare source material:
Edit tools/harvest/conversation.json with your text. Optional: fill in metadata.source_* fields.

Run the full pipeline (on Paperspace GPU):

text
python tools/harvest/harvest_full_pipeline.py --auto --with-relationships
Regenerate map (v2.4.1 — Cytoscape.js interactive):

text
python tools/generate_mycelium_map.py
Regenerate public gateway (v3.2.1 — translate.js enabled):

text
python tools/generate_public_gateway.py
Export backup CAR:

text
python tools/export_to_car.py --all --output cadmies_latest.car
Commit and push to GitHub (droplet auto-pulls and deploys):

text
git add -A && git commit -m "Harvest: description of changes" && git push origin main
Sync to local:

text
cd /run/media/fedora/PNY/CADMIES/CADMIES-IPLD && source venv/bin/activate && git pull origin main
Workflow 2: External Source Harvest
For published work (blogs, papers, articles) requiring citation.

text
conversation.json with metadata → Harvester reads metadata → Injects into proofs → Concepts minted with full attribution
Example: Rebentisch Harvest
json
{
  "metadata": {
    "_citation_guidance": "For scientific provenance and proper attribution, complete the fields below. Optional — defaults to internal CADMIES standards. May be amended later.",
    "source_description": "Dr. Rupert Rebentisch's blog 'Mycelium of Knowledge' — article: 'When AI Becomes Your Zettelkasten's Co-Pilot'",
    "source_url": "https://www.mycelium-of-knowledge.org/when-ai-becomes-your-zettelkastens-co-pilot/",
    "author": "Dr. Rupert Rebentisch",
    "license": "MIT"
  },
  "content": "[Full article text here]"
}
The harvester automatically injects this metadata into the proofs array:

```json
"proofs": [{
  "type": "conversation_extraction",
  "description": "Extracted from conversation via mistral:7b",
  "reference": "https://...",
  "author": "...",
  "license": "..."
}]
```

Workflow 3: CAR Import & Sync
Bringing the mycelium from Paperspace to the droplet or local machines.

text
Paperspace → export_to_car.py → cadmies_latest.car → import_from_car.py → Blockstore updated
Commands
On Paperspace — export:

text
python tools/export_to_car.py --all --output cadmies_latest.car
Download cadmies_latest.car to target machine's incoming_cars/

On droplet or local — import:

text
python tools/import_from_car.py incoming_cars/cadmies_latest.car
python tools/generate_mycelium_map.py
python tools/generate_public_gateway.py
Workflow 4: Quality Control & Maintenance
text
Remint stale → Regenerate map → Check unmapped domains → Audit concepts → Export CAR backup
Commands
Remint any stale CIDs:

text
python tools/remint_existing_concepts.py --apply
Regenerate map and check domains:

text
python tools/generate_mycelium_map.py
Look for "NOTE: Unmapped domain" in output. Add missing mappings to DOMAIN_UPWARD_MAP if needed.

Audit source concepts:

text
python3 -c "
import json
from pathlib import Path
source_dir = Path('source_concepts')
for jf in source_dir.glob('*.json'):
    with open(jf) as f:
        c = json.load(f)
    dl = c.get('difficulty_levels', {})
    for level in ['beginner', 'intermediate', 'expert']:
        if level not in dl or not dl[level]:
            print(f'{c[\"human_id\"]}: EMPTY {level}')
"
Run scientific audit:

text
python audits/scientific_audit.py
Strip orphan edges (if relationship generator left any):

text
python tools/strip_all_orphans.py --apply
Export backup:

text
python tools/export_to_car.py --all --output cadmies_latest.car
Workflow 5: Concept Enrichment
Fill gaps in existing concepts via LLM.

text
Detect gaps → Enrich via LLM → Validate → Remint with new CID
Commands
Enrich all concepts with gaps:

text
python tools/enrich_concepts.py
Enrich single concept:

text
python tools/enrich_concepts.py --concept=entropy
Dry run (preview only):

text
python tools/enrich_concepts.py --dry-run
Workflow 6: ORCID Verification
Stamp concepts with researcher identity.

text
Device Flow (owner-verified) → Fetch profile → Create verification block → Badge updates
Commands
Owner-verified stamp (requires .env with ORCID credentials):

text
python tools/core/orcid_device_flow.py <concept_cid>
Claimed stamp (public API, no auth):

text
python tools/core/orcid_stamper.py <concept_cid> <orcid_id>
Check verification status:

text
python tools/core/verification_manager.py --status <concept_cid>
Workflow 7: Session Sync
End-of-session synchronization across all nodes.

text
Paperspace → git push → GitHub → droplet auto-pull → public gateway updates
                                  └──→ local git pull

Commands
On Paperspace:

text
cd /notebooks/CADMIES/CADMIES-IPLD
git add -A
git commit -m "Session XXX: description of changes"
git push origin main
On local (PNY):

text
cd /run/media/fedora/PNY/CADMIES/CADMIES-IPLD && source venv/bin/activate
git pull origin main
Droplet — no manual step needed. Auto-pulls from GitHub via cron. Public gateway updates automatically at https://project-hierion.org

Node Responsibilities
Node	Role	Primary Scripts
Paperspace (GPU)	Harvest, extraction, relationship generation	harvest_full_pipeline.py, generate_relationships.py
Droplet (AMD)	Public gateway, blockstore, Matadisco producer	generate_public_gateway.py, generate_mycelium_map.py
Local (PNY)	Backup, local access, development	import_from_car.py, cbor_reader.py
GitHub	Source of truth, version control	All scripts
Script Reference
Full script documentation: SCRIPT_INVENTORY.md
Pipeline visual: PIPELINE_FLOW.md

Changes (2026-08-12 Update)
Map version corrected to v2.4.1 (Cytoscape.js, not v3.0.0 fractal)

Domain updated to project-hierion.org

Added Workflow 5: Concept Enrichment

Added Workflow 6: ORCID Verification

Added Node Responsibilities table

Added SCRIPT_INVENTORY.md and PIPELINE_FLOW.md references

Removed v3.0.0 fractal references (not yet implemented)

Added strip_all_orphans.py to maintenance workflow

Added scientific_audit.py to maintenance workflow
