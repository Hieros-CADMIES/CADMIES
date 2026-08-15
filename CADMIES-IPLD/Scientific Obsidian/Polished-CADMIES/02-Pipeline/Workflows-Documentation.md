---
pipeline: CADMIES Documentation Workflow
date: 2026-08-12
status: Living document
related: [[Session-049-2026-08-12-Script-Audit-and-Standardization]], [[Phase-37-Scientific-Obsidian]]
---

# CADMIES Documentation Workflow

## What This Covers

Every session produces documentation: raw notes, polished phase notes, roadmap updates, script audits, and changelog entries. This workflow ensures nothing is forgotten.

## Workflow: Session Documentation
Session ends
│
▼
Raw session note → Scientific Obsidian/Raw-CADMIES/Session-Notes/Session-XXX.md
│
▼
Polished phase notes (if any) → Scientific Obsidian/Polished-CADMIES/03-Development/Phase-XX-Name.md
│
▼
Roadmap update → growth_roadmap.md (milestone log, metrics)
│
▼
Script inventory update → SCRIPT_INVENTORY.md (new scripts, version bumps, status changes)
│
▼
Commit & push → git add -A && git commit && git push

text

## Note Types

### Raw Session Notes
- **Location:** `Scientific Obsidian/Raw-CADMIES/Session-Notes/Session-XXX.md`
- **Format:** Casual Friday tone. Soundtrack, vibes, half-formed ideas, coded messages.
- **Template:** Banner warning, session number, date, soundtrack, sections for what happened, final state, bugs, nuggets.
- **Created:** Every session.

### Polished Phase Notes
- **Location:** `Scientific Obsidian/Polished-CADMIES/03-Development/Phase-XX-Name.md`
- **Format:** Scientific rigor. Frontmatter (phase/date/status/related), then What Changed, Why, Changes Made, Testing, Results, Analysis, Conclusion, Next Steps.
- **Created:** When a phase is completed or a significant milestone is reached.

### Pipeline Documents
- **Location:** `Scientific Obsidian/Polished-CADMIES/02-Pipeline/`
- **Format:** Workflow diagrams, command references, quick reference cards.
- **Created:** When new workflows are established or existing ones change significantly.

### Script Inventory
- **Location:** `SCRIPT_INVENTORY.md` (repo root)
- **Format:** Table with file path, version, status, function, related scripts, inputs, outputs, notes.
- **Created:** After script audits or significant script changes.

### Pipeline Flow
- **Location:** `PIPELINE_FLOW.md` (repo root)
- **Format:** ASCII diagram showing the full pipeline from harvest to deployment.
- **Created:** After architectural changes or new pipeline stages.

## Quick Reference

| Document Type | Location | When to Create |
|--------------|----------|----------------|
| Raw session note | Raw-CADMIES/Session-Notes/ | Every session |
| Polished phase note | Polished-CADMIES/03-Development/ | Phase completion |
| Roadmap update | growth_roadmap.md | Every session |
| Script inventory update | SCRIPT_INVENTORY.md | Script changes |
| Pipeline flow update | PIPELINE_FLOW.md | Architectural changes |
| Pipeline document | Polished-CADMIES/02-Pipeline/ | New workflows |

## Script Documentation Standard

Every Python script follows the NASA-standard documentation format established in Session 049:

- YAML metadata block (System, Document_ID, Version, Classification, Author, Reviewers, Status, Created, Modified, Related_Docs)
- Version History section in docstring
- VERSION constant for dynamic version display
- Paths managed exclusively through paths.py
- Terminal emoji policy: user-facing tools retain emojis, scientific tools removed them

When updating a script, always:
1. Bump the VERSION constant
2. Add a Version History entry
3. Update SCRIPT_INVENTORY.md
4. Log the change in the session note
