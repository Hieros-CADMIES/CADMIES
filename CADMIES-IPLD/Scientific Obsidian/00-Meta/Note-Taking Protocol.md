---
type: protocol
version: 1.1.0
date: 2026-07-25
status: Living document — updated as conventions evolve
related: [[NASA-level standards reference]], [[CADMIES-Canon]], [[Architecture Overview]]
---

Purpose
This protocol governs how notes are created, formatted, linked, and promoted within the Scientific Obsidian vault. It ensures consistency across Raw CADMIES and Polished CADMIES, making the vault navigable for gardeners, collaborators, and PhDs alike. Standards are informed by NASA-level scientific documentation practices where applicable.

Vault Notes Structure
The vault notes hav two primary workspaces plus a meta layer:

Raw CADMIES/ — The primary workspace. The live lab notebook. This is where ideas land, sessions are drafted, and half-formed thoughts find their first expression. Gardeners work here by default. Mistakes are welcome. Typos are canon.

Polished CADMIES/ — The secondary workspace. Structured, reviewed, PhD-ready documentation. Notes are promoted here from Raw when they meet the promotion criteria below.

00-Meta/ — Governs both layers. Templates, conventions, this protocol.

File Naming Conventions
Use Sentence case for all note titles: Harvester pipeline overview.md not harvester_pipeline_overview.md

Phase documents: Phase-XX-Brief-Description.md (e.g., Phase-35-Difficulty-Levels.md)

Session summaries: Session-XXX.md (e.g., Session-005.md)

No special characters except hyphens and em-dashes. No emojis, no colons in filenames.

Spaces are fine — Obsidian handles them natively.

All markdown files must carry the .md extension. Files without extensions will not be recognized by automation tools.

Raw CADMIES Conventions
Every note in Raw CADMIES begins with a banner:

⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
unfiltered thoughts, and coded messages for fellow gardeners.
For polished documentation, check Polished CADMIES or promote this note.

Rules for Raw:

Write freely. Grammar optional. Structure optional. Vibes mandatory.

Date your entries. Even a quick 2026-05-14 at the top helps trace idea lineage.

Use [[double brackets]] to link to related concepts, phases, sessions, or people — even if the target note doesn't exist yet. Red links are future spores.

Tag generously but loosely. #idea, #question, #breakthrough, #bug, #wtf

No pressure to organize. The mycelium finds connections organically.

Session notes must include the standard session template sections (What We Did, What Worked, What Broke, Decisions Made, Nuggets Collected, Next Session). This ensures every session is searchable and comparable.

Polished CADMIES Conventions
Every note in Polished CADMIES includes a YAML frontmatter header:

text
---
phase: XX
date: YYYY-MM-DD
status: Complete | In Progress | Designed | Planned | Abandoned | Active
related: [[note-one]], [[note-two]]
---
Rules for Polished:

Structured, clear, PhD-readable.

Every claim links to evidence — a session summary, a commit, a test result.

No banners needed. The folder itself signals "this is the clean copy."

Follow the folder structure: System, Pipeline, Development, Concepts, Collaboration.

Version your notes if they undergo major revisions (append version to metadata, not filename).

No emojis in polished notes. These documents serve a scientific audience. Use words, not icons.

Required sections for phase notes: ## What Changed and ## Why are mandatory. Additional sections (## Changes Made, ## Testing, ## Results, ## Analysis, ## Conclusion) are recommended where applicable.

Status values are standardized. Use plain text: Complete, In Progress, Designed, Planned, Abandoned, Active. No emoji-prefixed statuses. If a phase is postponed, use Designed with clarification in the body.

A blank line must separate the YAML frontmatter closing --- from the content. This ensures compatibility with Obsidian's preview parser.

YAML Frontmatter Rule
Polished notes use YAML frontmatter (the --- block at the top). The only --- in any note is the YAML block. For section dividers in the body, use *** (three asterisks). This prevents Obsidian's YAML parser from breaking when it encounters --- mid-document.

All frontmatter fields use lowercase keys with spaces in values where needed. Required fields vary by document type — see the automation config.yaml for the authoritative list.

Promotion Criteria: Raw → Polished
A note is ready for promotion when:

It has a clear title that describes its content.

It is structured enough that a stranger (or a PhD) could understand it without context.

Key claims link to evidence (session notes, commits, test results).

The Raw banner is removed and replaced with a Polished metadata header.

It is placed in the appropriate Polished CADMIES subfolder.

All wikilinks resolve to actual files. Dead links must be fixed or removed before promotion.

Promotion is optional. Not every raw note needs to become polished. Some spores stay in the scrawl forever, and that's fine.

Linking Philosophy
The vault is a graph, not a hierarchy. Link aggressively:

[[Phase-35-Difficulty-Levels]] — links to phase documentation

[[Session-005]] — links to a session summary

[[Harvester Pipeline (Superceded by Workflows)]] — links to a pipeline tool note

[[Dr. Rebentisch — Twin Mycelium]] — links to a person/collaborator note

[[bayes_theorem]] — links to a concept (mirrors the mycelium)

Wikilinks must use the full filename of the target note (without the .md extension). Shorthand links like [[Session-014 — 2026-05-20 — Buttercup setup]] that rely on Obsidian's partial matching will be flagged as dead links by automation. Use the complete note title.

Red links (notes that don't exist yet) are planted spores. They mark where future notes should grow. Don't delete them — let them fruit.

Script files, concept IDs, and other non-note references should use backtick code formatting (backtick generate_mycelium_map.py backtick), not wikilinks.

Automation & Validation
The vault is monitored by an automated validation system at repo-maintenance-automation/. Key facts:

validate_vault.py scans all notes for frontmatter consistency, dead wikilinks, missing sections, duplicate files, roadmap drift, and missing file extensions.

Run it locally: python repo-maintenance-automation/validate_vault.py

Auto-fix mode: python repo-maintenance-automation/validate_vault.py --fix (shows before/after, asks for confirmation)

Batch mode: python repo-maintenance-automation/validate_vault.py --fix --yes (auto-applies all safe fixes)

GitHub Action: A workflow at .github/workflows/vault-check.yml runs the validator on every push to main. A status badge in the README shows current vault health.

Pre-commit hook: A local hook blocks commits if the vault has issues. Bypass with git commit --no-verify if necessary.

Backups: Every automated fix creates a timestamped backup in logs/backups/.

Configuration: config.yaml defines required fields and sections for each document type. Update it when standards evolve.

Tags
Use flat, lowercase tags. No hierarchy needed to start:

Tag	Usage
#idea	A new concept, approach, or possibility
#question	Something that needs answering
#breakthrough	A significant insight or discovery
#bug	Something broken that needs fixing
#decision	An architectural or design choice
#phase-XX	Relates to a specific roadmap phase
#harvester, #map, #gateway	Tool-specific notes
#collaboration	Cross-mycelium or external partnership
Tags will evolve. That's fine. Add new ones as needed.

Session Summary Template
Create one note per development session in Raw CADMIES/Session-Notes/. Use this template:

text
# Session XXX — YYYY-MM-DD — Brief Description

## Soundtrack
(Optional — what was playing)

## What We Did

## What Worked

## What Broke

## Decisions Made

## Nuggets Collected

## Next Session
Promote completed session summaries to Polished CADMIES/03-Development/ when they are coherent enough for external readers.

Collaboration Notes
All external collaboration documentation lives in Polished CADMIES/05-Collaboration/. Each collaborator gets a note:

Who they are

What they built / are building

How their work intersects with CADMIES

Links to their repositories, papers, or correspondence

Status of the collaboration (active, dormant, completed)

Classification & Privacy
Polished notes are safe for public viewing. No personal information beyond first initial. No internal tooling references that would confuse external readers.

Raw notes may contain local paths, unfiltered thoughts, and personal references. They stay in the vault but are not intended for public distribution.

Sensitive files (credentials, private keys, local configs) are excluded from GitHub via .gitignore and must never appear in the vault.

Credit & Attribution
All influences are documented. If a methodology, tool, or idea came from somewhere else, link to it.

Dr. Rupert Rebentisch (tools4zettelkasten) and the Luhmann/Ahrens/Forte zettelkasten tradition are the primary methodological influences on this vault.

NASA-level scientific documentation standards inform the structure and rigor of polished phase notes.

The Naming Protocol uses hyphens to denote partnership: CADMIES-Mistral, CADMIES-IPLD, CADMIES-Codestral. The hyphen is an acknowledgment of collaboration, not a claim of ownership. Attribution is architecture.

CADMIES is CC BY-SA 4.0. All vault content inherits this license.

Evolution
This protocol is version 1.1.0. It will change as we learn what works. The Casual Friday approach applies: start lenient, increase rigor organically. The mycelium teaches us how to document it.


What Changed (v1.0.0 → v1.1.0)
Added:

Session template now includes "Soundtrack" as an optional field — already in use across most session notes, now codified.

Session template title format now includes a brief description: Session XXX — YYYY-MM-DD — Brief Description matching existing convention.

File naming rule: All markdown files must carry the .md extension. Explicitly stated to prevent automation failures.

File naming rule: No colons in filenames (discovered during Phase 69 cleanup).

Emoji prohibition for polished notes: No emojis in phase notes. Scientific audience standard.

Required sections for phase notes: ## What Changed and ## Why are mandatory. This was implicit before; now explicit.

Standardized status values: Complete, In Progress, Designed, Planned, Abandoned, Active. No emoji-prefixed statuses. Postponed phases use Designed with clarification.

Blank line rule: A blank line must separate YAML frontmatter closing --- from content. Ensures Obsidian preview compatibility.

Wikilink rule: Must use full filename, not shorthand. Automation flags shorthand as dead links.

Non-note reference rule: Script files and concept IDs use backtick formatting, not wikilinks.

Promotion criterion #6: All wikilinks must resolve before promotion.

Automation & Validation section: Documents the validator, GitHub Action, pre-commit hook, and config system.

Classification & Privacy section: Distinguishes public-safe polished notes from raw notes and sensitive files.

NASA standards acknowledgment: Added to Purpose and Credit sections as a methodological influence.

Removed:

Duplicate "Naming Protocol" paragraph in Credit & Attribution section.

"Next Steps" from session template — removed per Phase 69 decision. Future steps are too fluid and create confusion.

Why:

The v1.0.0 protocol described ideals. v1.1.0 describes what we actually enforce — based on 135 issues discovered and resolved during Phase 69. Every change reflects a real problem found by the automation system or a convention already in practice across existing notes. The NASA-level documentation standards provide the rigor framework; the protocol provides the practical implementation.
"The fortress holds the library. The library holds the records. The mycelium holds the knowledge. Scientific Obsidian is the glass that remembers."
