---
type: pipeline-doc
pipeline: Core
date: 2026-08-12
status: Active
related: []
---

# CADMIES Script Inventory

This inventory documents every Python script in the CADMIES repository, its function, relationships, and status as of the script audit completed on 2026-08-12.

---

## Script Status Legend

- ✅ **ACTIVE** — Currently in use, required for pipeline
- ⚠️ **MAINTENANCE** — Used occasionally, not part of core pipeline
- 🗑️ **DEPRECATED** — Superseded or replaced, pending deletion
- 📋 **REFERENCE** — Kept for documentation purposes only

---

## CORE TOOLS (tools/core/)

### paths.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/core/paths.py`
- **Version:** 1.2.0
- **Status:** ✅ ACTIVE
- **Function:** Centralized path management for all CADMIES tools. Resolves project root dynamically.
- **Exports:** PROJECT_ROOT, STORE_DIR, BLOCKS_DIR, INDEX_DIR, LOGS_DIR, SOURCE_CONCEPTS_DIR, DOCS_DIR, INDEX_FILE, ensure_dirs()
- **Related Scripts:** Imported by nearly every other script
- **Input:** None
- **Output:** Path constants and directory creation
- **Notes:** The hub. Every script should import from here, not compute paths locally.

### cid_generator.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/core/cid_generator.py`
- **Version:** 1.2.0
- **Status:** ✅ ACTIVE
- **Function:** Generates CIDs from concept JSONs using IPLD/DAG-CBOR. Validates concepts, creates blocks, updates index, logs operations.
- **Related Scripts:** Uses paths.py, provenance_manager.py. Used by harvest_full_pipeline.py, enrich_concepts.py, generate_relationships.py
- **Input:** Concept dict (via --concept-file or sample)
- **Output:** CID, block in store/blocks/{cid}.cbor, index update, operations log
- **Notes:** The heart of the system. Every concept flows through here.

### cbor_reader.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/core/cbor_reader.py`
- **Version:** 1.1.0
- **Status:** ✅ ACTIVE
- **Function:** Reads concepts from blockstore by CID or human_id. Lists all blocks. Shows schema compliance and provenance.
- **Related Scripts:** Uses paths.py, provenance_manager.py, verification_manager.py
- **Input:** CID or human_id (CLI argument)
- **Output:** Formatted concept display, retrieval log
- **Notes:** The read side of the blockstore.

### provenance_manager.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/core/provenance_manager.py`
- **Version:** 1.1.0
- **Status:** ✅ ACTIVE
- **Function:** Creates and queries provenance records (timestamps, authorship, verification).
- **Related Scripts:** Uses paths.py. Used by cid_generator.py, cbor_reader.py, verification_manager.py, enrich_concepts.py, harvest_full_pipeline.py
- **Input:** concept_cid, author, record_type, kwargs
- **Output:** Provenance block in store/blocks/, query results
- **Notes:** The audit trail. Every concept has a history.

### verification_manager.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/core/verification_manager.py`
- **Version:** 1.1.0
- **Status:** ✅ ACTIVE
- **Function:** Four-tier verification system (Unverified, Self-verified, Verified, Highly Verified). Manages verification statements and CAR export.
- **Related Scripts:** Uses paths.py, provenance_manager.py. Used by orcid_stamper.py, orcid_device_flow.py, cbor_reader.py
- **Input:** concept_cid, verifier_key, statement_type, source
- **Output:** Verification provenance blocks, verification status
- **Notes:** The trust layer. ORCID badges live here.

### scientific_validator.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/core/scientific_validator.py`
- **Version:** 1.1.0
- **Status:** ✅ ACTIVE
- **Function:** Four-level validation (BASIC, STANDARD, RIGOROUS, STRICT). Enforces scientific rigor before CID generation.
- **Related Scripts:** Standalone. Used by harvest_full_pipeline.py, enrich_concepts.py
- **Input:** Concept dict
- **Output:** Validation result (is_valid, errors, report)
- **Notes:** The quality gatekeeper. No weak concepts enter the mycelium.

### car_utils.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/core/car_utils.py`
- **Version:** 1.1.0
- **Status:** ✅ ACTIVE
- **Function:** Read/write CAR files without external dependencies. CID calculation, block integrity verification.
- **Related Scripts:** Used by export_to_car.py, import_from_car.py, verification_manager.py
- **Input:** Blocks dict, roots, file paths
- **Output:** CAR files, extracted blocks
- **Notes:** The transport layer. CAR files are how concepts travel.

### orcid_stamper.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/core/orcid_stamper.py`
- **Version:** 1.1.0
- **Status:** ⚠️ MAINTENANCE
- **Function:** Public API ORCID verification (claimed, not owner-verified).
- **Related Scripts:** Uses verification_manager.py
- **Input:** concept_cid, orcid_id
- **Output:** Verification block
- **Notes:** Use only when OAuth device flow not needed.

### orcid_device_flow.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/core/orcid_device_flow.py`
- **Version:** 1.1.0
- **Status:** ⚠️ MAINTENANCE
- **Function:** OAuth device flow for ORCID owner-verified stamping.
- **Related Scripts:** Uses paths.py, verification_manager.py
- **Input:** concept_cid
- **Output:** Verification block with authenticated ORCID
- **Notes:** Requires .env with ORCID_CLIENT_ID and ORCID_CLIENT_SECRET.

---

## TOOLS (tools/)

### generate_public_gateway.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/generate_public_gateway.py`
- **Version:** 3.2.1
- **Status:** ✅ ACTIVE
- **Function:** Generates the public website from blockstore. Filterable concept cards, search, translate.js, ORCID iD, JSON-LD, sitemap.
- **Related Scripts:** Uses paths.py, cadmies_concept_reader.py
- **Input:** Blockstore concepts
- **Output:** docs/index.html, docs/concepts.json, docs/sitemap.xml, docs/.nojekyll
- **Notes:** The front door. What the world sees.

### generate_mycelium_map.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/generate_mycelium_map.py`
- **Version:** 2.4.1
- **Status:** ✅ ACTIVE
- **Function:** Generates interactive Cytoscape.js map from blockstore. Zoom, search, tooltips, concept cards, legend, keyboard shortcuts, Easter egg.
- **Related Scripts:** Uses paths.py, cadmies_concept_reader.py
- **Input:** Blockstore concepts and relationships
- **Output:** mycelium_map.html
- **Notes:** The visualization. Where connections become visible.

### generate_relationships.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/generate_relationships.py`
- **Version:** 1.2.7
- **Status:** ✅ ACTIVE
- **Function:** Feeds concepts to Codestral/Mistral in batches to propose relationships. Two-phase: intra-batch and cross-batch bridges.
- **Related Scripts:** Uses paths.py, cid_generator.py, cadmies_concept_reader.py
- **Input:** Blockstore concepts
- **Output:** New edges written to blockstore (with --write)
- **Notes:** The edge builder. Connects what was separate.
- **Flag:** Write mode mutates blocks in place without new CID. Known tension with content-addressing.

### export_to_car.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/export_to_car.py`
- **Version:** 1.1.0
- **Status:** ✅ ACTIVE
- **Function:** Exports concepts (with provenance) to CAR files for sharing.
- **Related Scripts:** Uses paths.py, car_utils.py
- **Input:** human_ids or CIDs
- **Output:** CAR file
- **Notes:** How concepts leave the mycelium.

### import_from_car.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/import_from_car.py`
- **Version:** 1.3.0
- **Status:** ✅ ACTIVE
- **Function:** Imports concepts from CAR files. Integrity verification, reminting, index update, provenance preservation.
- **Related Scripts:** Uses paths.py, car_utils.py, verification_manager.py
- **Input:** CAR file
- **Output:** Blocks in store, index update
- **Notes:** How concepts enter the mycelium.

### import_from_github.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/import_from_github.py`
- **Version:** 1.1.0
- **Status:** ⚠️ MAINTENANCE
- **Function:** Downloads CAR files from URLs and imports them.
- **Related Scripts:** Uses paths.py, import_from_car.py
- **Input:** URL to CAR file
- **Output:** Imported concepts
- **Notes:** Convenience wrapper for remote CAR imports.

### normalize_concept_schema.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/normalize_concept_schema.py`
- **Version:** 1.1.0
- **Status:** ⚠️ MAINTENANCE
- **Function:** Normalizes all source_concept JSONs to unified superset schema.
- **Related Scripts:** Uses paths.py
- **Input:** source_concepts/*.json
- **Output:** Normalized JSONs (in place)
- **Notes:** Run after schema changes. Modifies files in place.

### strip_all_orphans.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/strip_all_orphans.py`
- **Version:** 1.1.0
- **Status:** ⚠️ MAINTENANCE
- **Function:** Strips edges pointing to non-existent targets. Creates backup first.
- **Related Scripts:** Uses paths.py, cadmies_concept_reader.py
- **Input:** Blockstore concepts
- **Output:** Cleaned blockstore, backup tarball
- **Notes:** Run after relationship generation to clean orphans.

### remint_existing_concepts.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/remint_existing_concepts.py`
- **Version:** 2.0.1
- **Status:** ⚠️ MAINTENANCE
- **Function:** Remints concepts whose block content changed since original minting.
- **Related Scripts:** Uses paths.py, cid_generator.py, provenance_manager.py, cadmies_concept_reader.py
- **Input:** Blockstore concepts
- **Output:** New CIDs, updated index, provenance records
- **Notes:** Run after relationship additions to maintain content-addressing integrity.

### enrich_concepts.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/enrich_concepts.py`
- **Version:** 1.1.0
- **Status:** ⚠️ MAINTENANCE
- **Function:** Enriches existing concepts with missing fields via LLM. Validates and remints.
- **Related Scripts:** Uses paths.py, cid_generator.py, scientific_validator.py, provenance_manager.py
- **Input:** Existing concepts
- **Output:** Enriched concepts with new CIDs
- **Notes:** For filling gaps in older concepts.

### phase1_extract.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/phase1_extract.py`
- **Version:** 1.1.0
- **Status:** ⚠️ MAINTENANCE (superseded by harvest_full_pipeline.py)
- **Function:** Legacy Phase 1 — send batches to Mistral, save raw responses.
- **Related Scripts:** Uses paths.py, cadmies_concept_reader.py
- **Input:** Blockstore concepts
- **Output:** raw_extractions/batch_XX.txt
- **Notes:** Kept for reference. Use harvest_full_pipeline.py for new work.

### phase2_parse.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/phase2_parse.py`
- **Version:** 1.1.0
- **Status:** ⚠️ MAINTENANCE (superseded by harvest_full_pipeline.py)
- **Function:** Legacy Phase 2 — parse raw responses, deduplicate, output new_edges.json.
- **Related Scripts:** Uses paths.py, cadmies_concept_reader.py
- **Input:** raw_extractions/batch_XX.txt
- **Output:** new_edges.json
- **Notes:** Kept for reference. Broken import fixed in v1.1.0.

### phase3_write.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/phase3_write.py`
- **Version:** 1.1.0
- **Status:** ⚠️ MAINTENANCE (superseded by harvest_full_pipeline.py)
- **Function:** Legacy Phase 3 — write new edges to blockstore.
- **Related Scripts:** Uses paths.py, cadmies_concept_reader.py
- **Input:** new_edges.json
- **Output:** Updated blockstore
- **Notes:** Kept for reference.

---

## HARVEST PIPELINE (tools/harvest/)

### harvest_full_pipeline.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/harvest/harvest_full_pipeline.py`
- **Version:** 4.2.1
- **Status:** ✅ ACTIVE
- **Function:** End-to-end harvester. Chunks conversation, searches mycelium, extracts concepts via Mistral, saves to source_concepts/, reviews, validates, mints.
- **Related Scripts:** Uses paths.py, cid_generator.py, scientific_validator.py, provenance_manager.py, cadmies_concept_reader.py
- **Input:** conversation.json (or batch mode)
- **Output:** source_concepts/*.json, harvested_concepts.json, minted blocks
- **Notes:** The primary harvester. Replaces the three-phase scripts.

### extract_concepts.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/tools/harvest/extract_concepts.py`
- **Status:** 🗑️ DEPRECATED
- **Function:** Old version of harvester with hardcoded conversation_01.json.
- **Notes:** DELETE. Superseded by harvest_full_pipeline.py.

---

## AGENTS (agents/code/)

### cadmies_concept_reader.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/agents/code/cadmies_concept_reader.py`
- **Version:** 1.3.0
- **Status:** ✅ ACTIVE
- **Function:** Willie the Research Assistant. Hybrid search (keyword + semantic), feeds concepts to LLM, returns answers with CID references and accuracy tags.
- **Related Scripts:** Uses paths.py. Used by gateway generator, map generator, relationship generator, harvester.
- **Input:** User query, optional CIDs
- **Output:** Answers with concept references
- **Notes:** The bridge between natural language and CADMIES.

### philosophical_analyzer.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/agents/code/philosophical_analyzer.py`
- **Version:** 1.1.0
- **Status:** ✅ ACTIVE
- **Function:** Analyzes concepts for patterns, connections, insights. Three depth levels.
- **Related Scripts:** Uses paths.py
- **Input:** Concept CIDs
- **Output:** Analysis results (connections, insights, recommendations)
- **Notes:** The pattern finder. Air-gapped, stdlib only.

---

## AUDITS (audits/)

### scientific_audit.py
- **Path:** `/notebooks/CADMIES/CADMIES-IPLD/audits/scientific_audit.py`
- **Version:** 1.1.0
- **Status:** ⚠️ MAINTENANCE
- **Function:** Four-part audit: structure, metadata, functionality, standards. Generates report.
- **Related Scripts:** Uses paths.py, cid_generator.py
- **Input:** Project root
- **Output:** scientific_audit_report.json, terminal report
- **Notes:** Run periodically to verify system health.

---

## DATA FILES (not scripts)

| File | Path | Purpose |
|------|------|---------|
| conversation.json | tools/harvest/ | Input for harvester |
| harvested_concepts.json | tools/harvest/ | Output from harvester |
| new_edges.json | tools/ | Phase 2 output |
| legacy_edges.json | tools/ | Legacy relationship edges |
| human_id_to_cid.json | store/index/ | The index — concept mapping |
| operations.jsonl | store/logs/ | CID generation log |
| knowledge_retrieval.jsonl | store/logs/ | Concept retrieval log |

---

## DELETIONS PENDING

| File | Reason |
|------|--------|
| tools/harvest/extract_concepts.py | Superseded by harvest_full_pipeline.py |
| tools/generate_precomputed_map.py | Not a CADMIES script |

---

## SCRIPT RELATIONSHIPS
```
paths.py (hub)
│
├── cid_generator.py ──── provenance_manager.py
│ │ │
│ ├── harvest_full_pipeline.py
│ ├── enrich_concepts.py
│ └── generate_relationships.py
│
├── cbor_reader.py ──── provenance_manager.py + verification_manager.py
│
├── cadmies_concept_reader.py
│ │
│ ├── generate_public_gateway.py
│ ├── generate_mycelium_map.py
│ └── generate_relationships.py
│
├── car_utils.py
│ │
│ ├── export_to_car.py
│ └── import_from_car.py
│
└── scientific_validator.py
│
├── harvest_full_pipeline.py
└── enrich_concepts.py
```


---

## AUDIT NOTES (2026-08-12)

All scripts reviewed and standardized:
- Added YAML metadata blocks to all files
- Added VERSION constants
- Switched to paths.py for all path management
- Fixed broken imports (phase2_parse.py llm_mycelium_reader → cadmies_concept_reader)
- Fixed hardcoded paths (orcid_device_flow.py)
- Standardized .cbor extension usage
- Removed dead code
- Removed non-essential emojis from scientific tools
- Retained terminal emojis in user-facing tools per gardener preference
- Retained ORCID verification badges per gardener preference
- Flagged generate_relationships.py write-mode mutation issue (not fixed — architectural decision needed)
