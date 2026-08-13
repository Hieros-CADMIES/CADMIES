> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 049 - 2026-08-12 - Script Audit and Standardization

## Soundtrack
Nature. High-pressure heat, ugh.

## What We Did

**Conducted a comprehensive audit of every CADMIES Python script.** Reviewed 24 scripts across tools/, tools/core/, tools/harvest/, agents/code/, and audits/. Applied scientific documentation standards uniformly. Fixed broken imports, hardcoded paths, and inconsistent versioning.

### The Standardization Work

Every script now has:
- YAML metadata block with Document_ID, Version, Classification, Author, Reviewers, Status, Created, Modified, Related_Docs
- Version History section documenting all changes
- VERSION constant for dynamic version display
- paths.py import for all path management (no more local PROJECT_ROOT computation)
- Consistent .cbor extension handling with legacy fallback

### Scripts Fixed (24 total)

**Core tools (9):**
- paths.py — Added SOURCE_CONCEPTS_DIR, DOCS_DIR, error handling, version 1.2.0
- cid_generator.py — YAML block, INDEX_FILE usage, ensure_dirs call, emoji removal
- cbor_reader.py — YAML block, dynamic version, UTC timestamps, emoji removal
- provenance_manager.py — YAML block, removed store_path param, .cbor standardization
- verification_manager.py — YAML block, kept ORCID badges, removed other emojis
- scientific_validator.py — YAML block, dynamic version, UTC timestamps
- car_utils.py — YAML block, dynamic version, emoji removal
- orcid_stamper.py — YAML block, UTC timestamps
- orcid_device_flow.py — YAML block, fixed hardcoded .env path to use PROJECT_ROOT

**Tools (10):**
- generate_public_gateway.py — YAML block, VERSION constant, paths.py DOCS_DIR
- generate_mycelium_map.py — YAML block, VERSION constant
- generate_relationships.py — YAML block, VERSION constant, kept terminal emojis, flagged write-mode mutation
- export_to_car.py — YAML block, paths.py integration
- import_from_car.py — YAML block, paths.py integration
- import_from_github.py — YAML block, paths.py integration, kept terminal emojis
- normalize_concept_schema.py — YAML block, paths.py import
- strip_all_orphans.py — YAML block, VERSION constant
- remint_existing_concepts.py — YAML block, removed dead code, UTC backup timestamps
- enrich_concepts.py — YAML block, paths.py integration

**Harvester:**
- harvest_full_pipeline.py — YAML block, paths.py for SOURCE_CONCEPTS_DIR and INDEX_FILE, VERSION constant

**Agents (2):**
- cadmies_concept_reader.py — YAML block, paths.py import, removed duplicate path logic
- philosophical_analyzer.py — YAML block, paths.py import, dynamic test CIDs

**Audits:**
- scientific_audit.py — YAML block, fixed CID Generator import (tools.core not tools)

### Broken Imports Fixed
- phase2_parse.py — was importing from `llm_mycelium_reader` (nonexistent). Fixed to `cadmies_concept_reader`.
- scientific_audit.py — was importing from `tools.cid_generator`. Fixed to `tools.core.cid_generator`.
- orcid_device_flow.py — was hardcoded to `/workspaces/CADMIES/.env`. Now resolves via paths.py.

### The Inventory Document

Created SCRIPT_INVENTORY.md — comprehensive documentation of all 24 scripts:
- File paths, versions, status
- Functions and purposes
- Related scripts (upstream/downstream)
- Inputs and outputs
- Notes and flags
- Script relationship diagram
- Deletions pending list

### Files Flagged for Deletion
- tools/harvest/extract_concepts.py — superseded by harvest_full_pipeline.py
- tools/generate_precomputed_map.py — not a CADMIES script

### Architectural Issue Flagged (Not Fixed)
generate_relationships.py write-mode mutates blocks in place without generating new CIDs. The content changes but the filename stays the same. This breaks content-addressing. Requires architectural decision — either relationships move outside the immutable concept block, or the write mode must call remint_existing_concepts.py after every update.

### ORCID Discussion

Walked through how ORCID verification works in CADMIES:
- orcid_stamper.py — public API, claimed not owner-verified
- orcid_device_flow.py — OAuth device flow, real proof of ownership
- Need ORCID API credentials (.env with CLIENT_ID and CLIENT_SECRET)
- Need to retroactively stamp all current concepts once credentials exist
- Discussed batch stamping script as next step

## What Worked
- Systematic approach to script review — one file at a time, full analysis, fixes
- paths.py as the hub — every script now imports from it
- YAML metadata standard — consistent across all files
- Terminal emoji policy — kept in user-facing tools, removed from scientific tools
- The inventory document — everything documented, relationships mapped

## What Broke
- Nothing broke during the audit. But we found:
  - Two broken imports that would have crashed if run
  - One hardcoded path that only worked on Codespaces
  - Multiple dead code blocks
  - Inconsistent .cbor naming
  - Duplicate path computation everywhere

## Decisions Made
- GitHub is source of truth. Working in Codespaces.
- All scripts use paths.py. No local PROJECT_ROOT computation.
- YAML metadata on all files. No exceptions.
- Terminal emojis: kept in user-facing tools, removed from scientific tools
- ORCID badges stay. They're the verification system's identity.
- generate_relationships.py write-mode flagged but not changed — needs bigger architectural decision
- extract_concepts.py and generate_precomputed_map.py pending deletion

## Nuggets Collected
- "The hub. Every script should import from here, not compute paths locally."
- "The quality gatekeeper. No weak concepts enter the mycelium."
- "The transport layer. CAR files are how concepts travel."
- "The front door. What the world sees."
- "The edge builder. Connects what was separate."
- "The pattern finder. Air-gapped, stdlib only."
- "The audit trail. Every concept has a history."
- "The trust layer. ORCID badges live here."
