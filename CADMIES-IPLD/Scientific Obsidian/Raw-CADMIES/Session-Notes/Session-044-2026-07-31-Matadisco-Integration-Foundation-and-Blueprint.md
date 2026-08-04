> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 044 — 2026-07-31 — Matadisco Integration: Foundation & Blueprint

## Soundtrack
- Nature
- The hum of the pc fan

## What We Did

### Phase 73 Launch
- Officially kicked off Phase 73: Matadisco Integration
- Established two workstreams:
  1. **LLMDataHub → Matadisco** — publish license-audited dataset metadata
  2. **CADMIES Concepts → Matadisco** — publish 636 concepts as discoverable records

### Community Outreach
- Our issue (#18) on the Matadisco repo was responded to by vmx (lead dev)
- Green light received with guidance:
  - Use custom tags + top-level keys for namespace
  - Rate limits documented, report back per request
  - Self-hosting PDS has relay limit considerations
  - Offered to review example records/schema

### Key Decisions Made
- **PDS:** Self-hosted (open-source, privacy-focused, community-proven)
- **Handle:** `@project-hierion.org`
- **Authentication:** App password stored as GitHub secret
- **Producer:** Python, dedicated repo `project-hierion/hierion-matadisco`
- **Deployment:** Manual R&D first → GitHub Action later
- **Tag Strategy:** `project-hierion` for datasets, `cadmies` for concepts, author/domain tags as needed
- **License Policy:** Only explicit open licenses (MIT, Apache, CC-BY, BSD, GPL) — no license = skip
- **Attribution:** Full credit to original authors, link sources, cite licenses
- **Review Process:** Schema → vmx review → feedback → test records → vmx review → final go-ahead

### Repository Foundation
- Created `project-hierion/hierion-matadisco` on GitHub
- MIT license set
- README written with full project overview, structure, and usage
- Directory structure created:
  - `docs/` with subdirs: schema/, audit/, operations/, records/examples/, research/, experiments/
  - `scripts/`
  - `data/` with subdirs: llmdatahub/, cadmies/
  - `tests/`
- `.env.example` template created
- All directories tracked with `.gitkeep` files
- Initial commit pushed to main

### Blueprint Finalized
- Documented infrastructure decisions, schema approach, data preparation plan, community workflow
- Documentation structure designed for scientific rigor and reproducibility
- Experiment template established

## What Worked
- Clean repo setup with minimal friction
- Directory structure went in without issues
- `.env.example` created via cat command, clean and simple
- Sync to GitHub smooth

## What Broke
- Git doesn't track empty directories — caught and fixed with `.gitkeep` files
- Nothing else broke. Clean session.

## Decisions Made
1. Self-host PDS (open-source, privacy-focused)
2. Dedicated repo for producer (separate from LLMDataHub fork and CADMIES)
3. License audit is first priority before schema design
4. Community collaboration workflow: consult with vmx, review before publishing
5. All docs in `/docs/` with subdirectories for each major area
6. Raw session note uses full date and description format per protocol

## Nuggets Collected
- "We're early adopters contributing non-geospatial content to perform trial runs of the network."
- "They built it, we're testing it with real use cases."
- "No license = skip. Full attribution always."
- "We consult as necessary. Collaboration is the point."
- "Slow is fast. Lay the foundation before building the house."

## Next Steps
1. License audit of LLMDataHub fork → determine publishable datasets
2. Design schema for both record types
3. Pick first CADMIES concept for test record
4. Draft schema and share with vmx for review
5. Build test records once schema approved

## Related
- [[Phase-73-Matadisco-Integration]] (to be polished)
- [[Session-041-2026-07-28-LLMDataHub-Fork-Reorganization]]
- [hierion-matadisco](https://github.com/Project-Hierion/hierion-matadisco)
- [Matadisco #18](https://github.com/vmx/matadisco/issues/18)

---
*The mycelium redistributes.* 🍄
