> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 042 — 2026-07-28 — Filename Uniformity and Protocol Update

## Soundtrack
Film - Tentacle 8

## What We Did

**Standardized all filenames across the vault.** Every polished phase note and raw session note now uses hyphens only — no spaces, no em-dashes, no dots, no ampersands.

- Renamed 35+ polished phase notes to `Phase-XX-Description-With-Hyphens.md` format
- Renamed 38 raw session notes to `Session-XXX-YYYY-MM-DD-Description-With-Hyphens.md` format
- Removed all `Dr.` → `Dr`, all `&` → `and`, all `—` → `-`
- Updated 100+ wikilinks across the vault to match new filenames
- Built and tested a filename convention checker script, then deleted it (one-time use)
- Updated the Note-Taking Protocol to v1.2.0 with the new hyphen-only standard
- Fixed the validator's fuzzy matcher to handle shorthand session/phase links (v1.3.1)

## What Worked

- Bulk sed commands for renaming files and updating links
- The validator caught every dead link created by the renames
- Manual cleanup of the last stubborn links was quick once patterns were identified
- The new naming standard is simple: hyphens only, no exceptions

## What Broke

- Em-dashes in filenames caused `-—-` artifacts during sed replacements — had to clean those up
- The filename checker script was too strict, then too loose, then deleted
- Multiple push conflicts from editing on two machines simultaneously
- Apostrophes in filenames broke inline Python scripts during bulk link updates
- The `&` character kept getting encoded as `&amp;` by sed

## Decisions Made

- **Hyphens only in filenames.** No spaces, no em-dashes, no dots, no ampersands. Machine-readable, command-line safe, scientifically rigorous.
- **`Dr` not `Dr.`** — no dots in names
- **`and` not `&`** — no special characters
- **Date format in session notes:** `YYYY-MM-DD` separated by hyphens, not em-dashes
- **Note-Taking Protocol v1.2.0** codifies all of the above
- **Filename checker script deleted** — the validator already catches naming issues

## Nuggets Collected

- "Hyphens only. No exceptions. The machines demand it."
- "Every em-dash in a filename is a future dead link."
- "Rename files, run validator, fix links, repeat. The loop works."
- "The protocol is the law. The validator is the enforcer."
- "98 files, 0 issues. The mycelium is uniform."
