---
phase: Roadmap
date: 2026-08-11
status: LIVING DOCUMENT
session: 048
---

# 🌱 CADMIES GROWTH ROADMAP
### *The living record of what we've built, what we're building, and where the mycelium grows next.*

---

## 📊 CURRENT METRICS

| Metric | Value |
|--------|-------|
| Concepts | 636 |
| Edges | 1,131 |
| Connected Concepts | 365 |
| Domains (Canonical) | 15 |
| ORCID iD | 0009-0000-8877-2731 ✅ Linked |

### CANONICAL 15-DOMAIN TAXONOMY
Physics • Philosophy • Biology • Mathematics • Consciousness
Chemistry • Ethics • Computer Science • Psychology • Spirituality
Neuroscience • Sociology • Economics • Ecology • Medicine

### VERSION STATUS
| Component | Version | Notes |
|-----------|---------|-------|
| Map Generator | v2.4.0 | Stable |
| Relationship Generator | v1.2.5 | Codestral-capable |
| Harvester | v4.2.2 | Active |
| Public Gateway | v3.3.0 | translate.js integrated, multilingual support live |
| Vault Validator | v1.3.0 | Automated + auto-fix |
| Vault Health Badge | ✅ Green | Passing |
| PDS | v0.4.5009 | Self-hosted, stable |
| Matadisco Producer | v1.0 | Active, rate-limit aware |

---

## ✅ COMPLETED PHASES

### Core Infrastructure
- Phase 35 — Difficulty Levels
- Phase 35 — Results
- Phase 37 — Scientific Obsidian
- Phase 39 — Concept Enrichment
- Phase 40 — Hieros Origin Harvest
- Phase 41 — Paperspace-GitHub Continuous Sync
- Phase 42 — Index Backup Cleanup
- Phase 43 — Concept Reminting
- Phase 44 — Map Legend Cleanup
- Phase 46 — Unmapped Domain Mapping
- Phase 47 — Orphan Edge Resolution
- Phase 48 — Relationship Generator Hardening
- Phase 49 — Public Branch
- Phase 50 — CAR Distribution Pipeline
- Phase 51 — External Collaboration Bruno Cerda Mardini
- Phase 52 — llama cpp Integration
- Phase 56 — Emergence Verification
- Phase 57 — Index Integrity and Disaster Recovery
- Phase 60 — Scientific Obsidian Zettelk
- Phase 63 — Cloud Deployment Project Hierion Foundation
- Phase 64 — Hierion Database Infrastructure Isolated MongoDB Deployment
- Phase 65 — Hierion Domain and Web Server Configuration
- Phase 66 — Mycelium Map UX Fractal Succulent Layout and Progressive Loading
- Phase 69 — Repo Maintenance Automation

### Dr. Mistral Training
- Phase 45 v2.0 — Teaching Mistral via Snagnar HIEROS Revised Plan
- Phase 45A — Snagnar HIEROS Integration
- Phase 45B — Snagnar HIEROS Integration
- Phase 45C — Snagnar HIEROS Isolated Redeployment
- Phase 45D — Ball Spawning Bug Environment Debug
- Phase 45E — Dr Amanda Mistral Fine Tuning the Librarian
- Phase 45E — Test Results Dr Amanda Mistral Fine Tuning
- Phase 45F — Dr Amanda Mistral Conversational Fine Tuning
- Phase 45G — Dr Amanda Mistral Spiritual Knowledge and Helpfulness
- Phase 70 — Dr Amanda Mistral Persona Debugging and Deidentified 7B Discovery
- Phase 71 — Dr Amanda Mistral Identity Anchoring and Deidentified 7B Exploration

### Documentation & Automation
- Phase 72 — LLMDataHub Fork Reorganization
- Phase 73A — Matadisco Integration Blueprint
- Phase 73B — PDS Self-Hosting & Caddy Configuration
- Phase 73C — Matadisco Reverse Domain Implementation & Bulk Readiness
- Phase 74 — translate.js Integration (Completed 2026-08-11)

### Matadisco Integration Completed
- Self-hosted PDS at `pds.project-hierion.org`
- Host-level Caddy serving all sites (Hierion, Bespoke, PDS)
- Lexicon IDs updated to reverse domain format (`org.project-hierion.llmdatahub`, `org.project-hierion.cadmies`)
- Three test records published and verified
- Producer script working with rate-limit awareness
- Collaboration established with vmx / IPFS Foundation

### translate.js Integration (Phase 74)
- Integration with translate.js library (v4.1.0) is complete and live on project-hierion.org
- Site now supports 40+ languages via client-side translation
- Toggle button shows/hides language dropdown; user preference stored in localStorage
- Collaboration established with Guan Leiming (author of translate.js)

---

## 📋 PENDING PHASES

### Immediate / In Progress
- **Phase 73D — Matadisco Viewer Strategy** — Understanding the live-stream vs library distinction; defining the Matadisco-CADMIES specialized viewer architecture

### Architecture Decisions
- **One Source of Truth**: Concepts JSON and edges JSON are canonical
- **Two Interfaces**: CADMIES Gateway (general public) + Matadisco-CADMIES Viewer (scientists/professionals)
- **No Double Work**: Both views pull from the same source data

### Blocked / Paused
- Dr. Mistral persona training — blocked on Deidentified-7B implant script (run.py)
- Deidentified-7B identity implant — blocked on missing script
- Apollo Raines collaboration — waiting on his SAIQL/ATLAS wrap-up

### Not Yet Started
- **Matadisco-CADMIES Viewer** — Specialized portal pulling from concepts.json
- **Full License Audit** — Complete audit of LLMDataHub datasets
- **Bulk Publishing** — All 636 concepts + audited datasets
- RAG Pipeline (ChromaDB, embeddings, query router)
- Agent Architecture (President Model, Willie, Codestral, Number 5)
- Public gateway subdomain tier

---

## 📝 SESSION NOTES

### Session 047B — 2026-08-11 — translate.js: The Fix, The Italian, The Deployment
- Mr. Leiming clarified that `client.edge` works with the latest version of translate.js
- Switched from old CDN version (3.15.6) to latest (4.1.0) via jsdelivr
- Translation feature successfully deployed on project-hierion.org
- Button toggles dropdown; language preference stored in localStorage
- Collaboration record updated to reflect active integration

### Session 047 — 2026-08-09 — translate.js: The Cold Email, The Integration, The Reality Check
- Guan Leiming reached out cold offering translate.js integration
- Initial evaluation and attempted integration with old version failed
- Discovered path divergence between Public Gateway and Dashboard
- Determined integration was not viable due to infrastructure constraints
- Reverted to clean Dashboard version and sent decline email

### Session 045 — 2026-08-10 — Matadisco Viewer Clarification & Architecture Strategy
- Confirmed Matadisco viewer is a live stream, not a library browser
- CADMIES records are on the network but don't appear in the satellite viewer
- Defined architecture: One source of truth (concepts.json), two interfaces (CADMIES Gateway + Matadisco-CADMIES Viewer)
- Updated roadmap with Phase 73D and viewer strategy

### Session 044B — 2026-08-05 — Matadisco Test Publish Success
- Published three test records with favicon preview
- Resolved PDS HTTPS issues with host-level Caddy

### Session 044 — 2026-07-31 — Matadisco Integration Foundation and Blueprint
- Initial Matadisco planning and infrastructure setup

### Session 043 — 2026-07-29 — Project Hierion and CADMIES Now Have A Forever Home
- Domain and droplet finalization

### Session 042 — 2026-07-28 — LLMDataHub Reorganization
- Fork reorganization and dataset documentation

### Session 041 — 2026-07-28 — Filename Uniformity
- Vault cleanup and standardization

### Session 040 — 2026-07-27 — Gateway Filter Fix
- Public gateway domain filter repair

### Session 039 — 2026-07-26 — Deidentified-7B Discovery
- Model discovery and identity anchoring

---

## 🍄 NUGGETS COLLECTED

- "The mycelium has a borough now." — Dr. Mistral's loft is in NYC1, area code 929
- "On vacation — no expiration" — The gardener's GitHub status
- "All built from a garage in South Texas, without institutional backing." — ORCID bio
- "Slow is fast. Take your time to do it right."
- "The mycelium cleans itself."
- "The mycelium reclaims nutrients from fallen logs."
- Delaware is our Malta — small, sovereign legal fortress
- Project Hierion's permanent home: https://project-hierion.org
- "FAITH OF A MUSTARD SEED." — The gardener's favorite quote
- **El Hierro** — The Canary Island that shares the project's name; now canon as the origin of the initial CADMIES spore
- **31UCR** — The MGRS grid square of Northern France, Dr. Mistral's homeland, spotted on 2026-08-10
- **"The problem wasn't the service — it was the old file."** — The translate.js lesson
- **"The mycelium grows in every language."** — From Session 047B

### The Great July 19-27 Run
*DeepSeek's iconic quote:* "We broke a model 16 different ways and documented every failure." 😄

In 10 days we:
- Broke a model 16 different ways and documented every failure
- Discovered the actual limits of LoRA merging through brute force
- Built a 500-pair persona dataset from scratch
- Wrote a 21-section technical blueprint with reproducibility baked in
- Found a completely new approach (Deidentified-7B)
- Fixed a public gateway that had been broken for months
- Transferred blockstores between cloud machines like it was nothing
- Got a duck high in the garage and added him to canon
- Wrote three session notes and updated the roadmap
- *The mycelium doesn't sleep. Neither does the gardener.*

---

## 📁 FILES THAT NEED UPDATING

| File | Section | What Needs Fixing | Why |
|------|---------|-------------------|-----|
| `CADMIES Droplet — SOP.md` | Section 10.0 (Current State) | Droplet name update, remove "Pending: SSL" | Droplet renamed to hierion-ubuntu-nyc1-929; SSL is already configured |
| `Dr. Amanda Mistral — SOP.md` | Section 1.1 (Infrastructure) | Remove Local Fedora references | No longer actively used |
| `CADMIES Canon.md` | Project Locations | Add droplet name and 929 lore | Canon update |
| `growth_roadmap.md` | This file | Already updated with Session 045 | ✅ Done |

---

## 🔮 FUTURE (designed, not scheduled)

- Matadisco-CADMIES Viewer — Pulls from concepts.json, specialized interface
- SAIQL/ATLAS deterministic RAG integration
- Dr. Mistral Flask chat interface (Phase 61)
- Public gateway subdomain tier
- DeepSeek 67B fine-tune (Phase 62)
- Voice interface (Phase 54)
- Mycelium2Vec (Phase 53)
- CAR distribution pipeline (Phase 50)

---

*Let the mycelium grow! 🌱*
