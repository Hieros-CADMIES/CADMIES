# Matadisco Integration: Initial Blueprint - Phase 73
Created: July 31, 2026

🎯 Objective
Publish two test records to Matadisco:

One LLMDataHub dataset (license-audited, fully attributed)

One CADMIES concept (from our 636-concept knowledge graph)

Then scale based on learnings, with community collaboration.

🏗️ Infrastructure Decisions (Locked In)
Area	Decision
PDS	Self-hosted (open-source, privacy-focused, community-proven)
Handle	@project-hierion.org
Authentication	App password stored as GitHub secret
Producer	Python, dedicated repo: project-hierion/matadisco-producer
Deployment	Manual R&D first → GitHub Action later
Rate Limits	Follow gdi-de-csw-to-atproto pattern for spreading
📋 Schema Design (To Be Finalized)
Core Schema (cx.vmx.matadisco)
json
{
  "resource": "URI",
  "publishedAt": "ISO timestamp",
  "preview": { "mimeType": "string", "url": "URI" },  // optional
  "tags": ["array", "of", "strings"]                   // max 20, 1-200 chars
}
Custom Top-Level Keys (Our Namespace)
LLMDataHub datasets: project-hierion key

CADMIES concepts: cadmies key

Tag Strategy
LLMDataHub: project-hierion + author tags (if any)

CADMIES: cadmies + domain tags

Additional tags as needed per record

🔬 Data Preparation
LLMDataHub Dataset
Action: Audit for explicit open license

Criteria: MIT, Apache, CC-BY, etc. → publish; no license/iffy → skip

Attribution: Full credit to original authors, link sources, cite license

Test Record: TBD (one clean dataset)

CADMIES Concept
Action: Select one concept for test record

Resource URI: Public gateway card URL (e.g., https://project-hierion.org/cards/consciousness.html)

Test Record: TBD

📝 Documentation Structure — What We Need to Build
Matadisco Project Docs (within the producer repo)
/docs/ structure:

```text
docs/
├── README.md                    # Overview of the Matadisco integration project
├── schema/
│   ├── llmdatahub-schema.md    # Our custom schema for dataset records
│   └── cadmies-schema.md       # Our custom schema for concept records
├── audit/
│   ├── license-audit.md        # Full audit results (pass/skip per dataset)
│   └── methodology.md          # How we audited (criteria, process)
├── operations/
│   ├── producer-setup.md       # How to set up the producer environment
│   ├── manual-run.md           # How to run the producer manually
│   └── github-actions.md       # How to set up the automated pipeline (future)
├── records/
│   ├── test-dataset-record.json    # The actual test record (dataset)
│   ├── test-concept-record.json   # The actual test record (concept)
│   └── examples/                   # Additional example records
├── research/
│   ├── gdi-de-csw-to-atproto-analysis.md  # What we learned from their repo
│   └── rate-limits-analysis.md           # Rate limit strategy documentation
└── experiments/
    └── YYYY-MM-DD-experiment-description.md  # Each R&D session documented
```

Scientific Obsidian Integration
Raw notes: Session-XXX — YYYY-MM-DD — Matadisco [topic].md

Polished notes: Phase-73-Matadisco-Integration.md (when we're ready to formalize)

Cross-link to the producer repo's docs

🔬 Experiment Documentation Template
For each R&D session (test runs, schema experiments, etc.):

# Experiment: [Brief Description]
**Date:** YYYY-MM-DD
**Phase:** 73
**Status:** [Planned / Running / Complete / Failed]

## Objective
[What we're testing]

## Setup
- Environment: [local / Codespaces / droplet]
- Dependencies: [list versions]
- Command(s) run: [exact commands]

## Procedure
[Step-by-step what we did]

## Results
[What happened — output, logs, errors]

## Analysis
[What it means — successes, failures, surprises]

## Next Steps
[What we're doing based on this]

## References
- [Links to docs, issues, PRs]

🤝 Community Collaboration Workflow
Design schema → share with vmx for review

Get feedback → incorporate suggestions

Build test records → manual producer run

Share records with vmx → request final review

Get go-ahead → publish officially

Scale → apply learnings to bulk publishing

Principle: We consult as necessary. vmx is building the foundation with us — collaboration is the point.

✅ Immediate Next Actions
□ Pick first dataset from LLMDataHub fork (license-audited, clean)
□ Pick first concept from CADMIES (636 available)
□ Design schema structure for both record types
□ Share schema with vmx for early review
📦 Deliverables
project-hierion/matadisco-producer repo

Producer script (Python)

Two test records (one dataset, one concept)

License audit results for LLMDataHub datasets

Documentation for future scaling

🚧 Known Constraints
No license = skip (strict policy)

Full attribution always

No personal info in public records

Rate-limit-aware publishing

