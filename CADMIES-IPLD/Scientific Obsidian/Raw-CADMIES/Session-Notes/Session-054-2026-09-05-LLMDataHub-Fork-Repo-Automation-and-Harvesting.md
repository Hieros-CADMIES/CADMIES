> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,  
> unfiltered thoughts, and coded messages for fellow gardeners.  
> For polished documentation, check Polished CADMIES or promote this note.

# Session 054 — 2026-09-05 — LLMDataHub Fork Repo Automation and Harvesting

## Soundtrack
Quiet reorganizing vibes. Mycelium reclaiming nutrients from fallen logs.

## What We Did

**Phase 1: Vault Automation**
- Adapted CADMIES `validate_vault.py` for LLMDataHub
- Created `config.yaml` with rules for DATASETS.md and REVISED-DESCRIPTIONS.md
- Set up GitHub Action workflow (`vault-check.yml`)
- Added "Repo Automation Status" badge to README
- Fixed YAML escape errors and config mismatches
- Validator now runs clean: 0 issues, 2 files checked

**Phase 2: Dataset Harvesting**
- Hunted and verified 58+ new datasets (all non-HF)
- Added Korean datasets (pretraining, QA, NLI, STS, speech, emotion, legal, medical, patent, culture)
- Added vision datasets (CIFAR-10, CelebA, LVIS, WIDER Face, Medical MNIST)
- Added finance datasets (Phrasebank, SEC EDGAR, Yahoo Finance, Walmart)
- Added time series datasets (M5, SMD, SMAP, MSL)
- Added audio datasets (VoxCeleb2, LibriSpeech)
- Created new "Time Series Datasets" section
- Reorganized file structure: heroes up top, HF graveyard at bottom

**Phase 3: ORCID Integration**
- Added ORCID iD to README footer

## What Worked

Validator came together cleanly once config was fixed. The CADMIES code adapted well to LLMDataHub needs.

GitHub Action deployed and badge is live.

Dataset hunting was productive — found everything from GitHub, ModelScope, and direct sources. Zero HF links.

## What Broke

- `config.yaml` initially empty (0 bytes) — had to recreate
- YAML escape error on `placeholder_marker_alt` — fixed by removing backslashes
- Section headers didn't match config — updated to match `<div id="...">` format
- Placeholder consistency flagged overlap table entries — fixed by skipping overlap section in validator
- Divergent branches during push — resolved with `--no-rebase` merge
- Workflow file missing from `.github/workflows/` — recreated and committed

## Decisions Made

- Skip the overlap table entirely (remnant from original repo, not maintaining)
- Use "Repo Automation Status" for badge label (not "Vault")
- All HF datasets go to graveyard, no links
- ORCID goes in README footer next to contact email
- Keep 🤑 emoji for HF-hosted datasets (tombstone later, maybe)

## Nuggets Collected

- "The vault is clean. The mycelium is healthy."
- "Repo Automation Status" — new badge for LLMDataHub
- "Our work is open, traceable, and part of the scientific record."

## Next Actions

- Branch off for harvester pipeline (`feature/harvester-pipeline`)
- Build GitHub scraper for dataset discovery
- Automate PR generation for new dataset additions
- Schedule weekly runs via GitHub Action
