---
type: protocol
version: 1.2.0
date: 2026-07-29
status: Living document — updated as conventions evolve
related: [[NASA-level standards reference]], [[CADMIES-Canon]], [[Architecture Overview]]
---

# CADMIES Note-Taking Protocol

## Purpose

This protocol governs how notes are created, formatted, linked, and promoted within the Scientific Obsidian vault. It ensures consistency across Raw CADMIES and Polished CADMIES, making the vault navigable for gardeners, collaborators, and PhDs alike. Standards are informed by NASA-level scientific documentation practices where applicable.

---

## Vault Structure

The vault has two primary workspaces plus a meta layer:

- **Raw-CADMIES/** — The primary workspace. The live lab notebook. This is where ideas land, sessions are drafted, and half-formed thoughts find their first expression. Gardeners work here by default. Mistakes are welcome. Typos are canon.
- **Polished-CADMIES/** — The secondary workspace. Structured, reviewed, PhD-ready documentation. Notes are promoted here from Raw when they meet the promotion criteria below.
- **00-Meta/** — Governs both layers. Templates, conventions, this protocol.

---

## File Naming Conventions

**All filenames use hyphens only. No spaces, no em-dashes, no special characters except hyphens.** This ensures machine-readability, command-line safety, and scientific rigor.

### Polished Phase Notes

Format: `Phase-XX-Description-With-Hyphens.md`

Examples:
- `Phase-35-Difficulty-Levels.md`
- `Phase-69-Repo-Maintenance-Automation.md`
- `Phase-45E-Dr-Amanda-Mistral-Fine-Tuning-the-Librarian.md`

Rules:
- Starts with `Phase-` followed by the phase number (digits, optional letter for sub-phases)
- Description uses hyphens between all words
- No dots, no ampersands, no em-dashes
- Use `and` not `&`
- Use `Dr` not `Dr.`

### Raw Session Notes

Format: `Session-XXX-YYYY-MM-DD-Description-With-Hyphens.md`

Examples:
- `Session-037-2026-07-16-The-Mycelium-Cleans-Itself.md`
- `Session-041-2026-07-28-LLMDataHub-Fork-Reorganization.md`

Rules:
- Starts with `Session-` followed by the session number
- Date in YYYY-MM-DD format, separated by hyphens
- Description uses hyphens between all words
- No dots, no ampersands, no em-dashes

### General Rules

- All markdown files must carry the `.md` extension
- No colons, no emojis in filenames
- No special characters except hyphens
- Sentence case for descriptions (not lowercase, not UPPERCASE)

---

## Raw CADMIES Conventions

Every note in Raw CADMIES begins with a banner:

> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

**Rules for Raw:**

- Write freely. Grammar optional. Structure optional. Vibes mandatory.
- Date your entries. Even a quick `2026-05-14` at the top helps trace idea lineage.
- Use `[[double brackets]]` to link to related concepts, phases, sessions, or people — even if the target note doesn't exist yet. Red links are future spores.
- Tag generously but loosely. `#idea`, `#question`, `#breakthrough`, `#bug`, `#wtf`
- No pressure to organize. The mycelium finds connections organically.
- Session notes must include the standard session template sections.

---

## Polished CADMIES Conventions

Every note in Polished CADMIES includes a YAML frontmatter header:

```text
---
phase: XX
date: YYYY-MM-DD
status: Complete | In Progress | Designed | Planned | Abandoned | Active
related: [[note-one]], [[note-two]]
---
```

Rules for Polished:

Structured, clear, PhD-readable.

Every claim links to evidence — a session summary, a commit, a test result.

No banners needed. The folder itself signals "this is the clean copy."

Follow the folder structure: System, Pipeline, Development, Concepts, Collaboration.

No emojis in polished notes. These documents serve a scientific audience. Use words, not icons.

Required sections: ## What Changed and ## Why are mandatory. Additional sections (## Changes Made, ## Testing, ## Results, ## Analysis, ## Conclusion) are recommended where applicable.

Status values are standardized. Use plain text: Complete, In Progress, Designed, Planned, Abandoned, Active. If a phase is postponed, use Designed with clarification in the body.

A blank line must separate the YAML frontmatter closing --- from the content.

YAML Frontmatter Rule
Polished notes use YAML frontmatter (the --- block at the top). The only --- in any note is the YAML block. For section dividers in the body, use *** (three asterisks). All frontmatter fields use lowercase keys. Required fields vary by document type — see repo-maintenance-automation/config.yaml for the authoritative list.

Promotion Criteria: Raw → Polished
A note is ready for promotion when:

It has a clear title that describes its content.

It is structured enough that a stranger (or a PhD) could understand it without context.

Key claims link to evidence (session notes, commits, test results).

The Raw banner is removed and replaced with a Polished metadata header.

It is placed in the appropriate Polished CADMIES subfolder.

All wikilinks resolve to actual files. Dead links must be fixed or removed before promotion.

Promotion is optional. Not every raw note needs to become polished. Some spores stay in the scrawl forever.

Linking Philosophy
The vault is a graph, not a hierarchy. Link aggressively:

[[Phase-35-Difficulty-Levels]] — links to phase documentation

[[Session-041-2026-07-28-LLMDataHub-Fork-Reorganization]] — links to a session summary

[[Harvester Pipeline (Superceded by Workflows)]] — links to a pipeline tool note

Wikilinks must use the full filename of the target note (without the .md extension). Shorthand links will be flagged as dead links by automation.

Red links (notes that don't exist yet) are planted spores. They mark where future notes should grow. Don't delete them — let them fruit.

Script files, concept IDs, and other non-note references should use backtick code formatting, not wikilinks.

Automation & Validation
The vault is monitored by an automated validation system at repo-maintenance-automation/.

validate_vault.py — scans all notes for frontmatter consistency, dead wikilinks, missing sections, duplicate files, roadmap drift, and missing file extensions.

Run it: python repo-maintenance-automation/validate_vault.py

Auto-fix: python repo-maintenance-automation/validate_vault.py --fix (shows before/after, asks for confirmation)

Batch mode: python repo-maintenance-automation/validate_vault.py --fix --yes

GitHub Action: Runs on every push to main. Status badge in README.

Pre-commit hook: Blocks commits if vault has issues.

Backups: Every automated fix creates a timestamped backup.

Configuration: config.yaml defines required fields and sections. Update it when standards evolve.

Session Summary Template
Create one note per development session in Raw-CADMIES/Session-Notes/.

# Session XXX — YYYY-MM-DD — Brief Description

## Soundtrack
(If the gardener says they're playing music or a video or movie)

## What We Did

## What Worked

## What Broke

## Decisions Made

## Nuggets Collected

Tags
Tag	Usage
#idea	A new concept, approach, or possibility
#question	Something that needs answering
#breakthrough	A significant insight or discovery
#bug	Something broken that needs fixing
#decision	An architectural or design choice
#phase-XX	Relates to a specific roadmap phase
#harvester, #map, #gateway	Tool-specific notes
#collaboration	Cross-mycelium or external partnership
Collaboration Notes
All external collaboration documentation lives in Polished-CADMIES/05-Collaboration/. Each collaborator gets a note with: who they are, what they built, how their work intersects with CADMIES, links to their work, and collaboration status.

Classification & Privacy
Polished notes are safe for public viewing. No personal information beyond first initial.

Raw notes may contain local paths, unfiltered thoughts, and personal references. Not for public distribution.

Sensitive files are excluded from GitHub via .gitignore.

Credit & Attribution
All influences are documented. Link to sources.

NASA-level scientific documentation standards inform the structure and rigor of polished phase notes.

The Naming Protocol uses hyphens to denote partnership: CADMIES-Mistral, CADMIES-IPLD, CADMIES-Codestral. The hyphen is a handshake.

CADMIES is CC BY-SA 4.0. All vault content inherits this license.

Evolution
This protocol is version 1.2.0. It will change as we learn what works. The Casual Friday approach applies: start lenient, increase rigor organically. The mycelium teaches us how to document it.

What Changed (v1.1.0 → v1.2.0)
Changed:

File naming: hyphens only. Spaces, em-dashes, dots, and ampersands are no longer permitted in filenames. All filenames use hyphens between all words. This enforces machine-readability and scientific rigor. (Session 041 cleanup)

Phase note format: Phase-XX-Description-With-Hyphens.md — no Dr., no &, no —

Session note format: Session-XXX-YYYY-MM-DD-Description-With-Hyphens.md — date now separated by hyphens, not em-dashes

Updated examples throughout to reflect current filenames

Removed "Next Steps" from session template (was already removed in v1.1.0 but still appeared)

Clarified that Dr is used without a dot, and replaces &

Why:
During the Session 041 filename uniformity work, we discovered that em-dashes, dots, and ampersands in filenames cause cascading link breakage across the vault. Hyphens-only filenames are machine-parseable, command-line safe, and eliminate entire categories of dead links. The standard is now simple and enforceable: hyphens only.

"The fortress holds the library. The library holds the records. The mycelium holds the knowledge. Scientific Obsidian is the glass that remembers."
