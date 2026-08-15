> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 050 - 2026-08-14 - Gateway Generator Rewrite and Relationship Harvest

## Soundtrack
(Whatever was playing during the longest debugging session of the summer)

## What We Did

**Rewrote the public gateway generator.** `generate_public_gateway.py` v3.3.0 now outputs the new site's app shell instead of the old dark-mode pre-baked cards. The generator's job is the data layer: `index.html` shell, `concepts.json` with relationships, `sitemap.xml`. The hand-maintained design files (`app.js`, `style.css`, `splash.css`) are no longer overwritten.

**Harvested relationships.** Ran `generate_relationships.py` on Paperspace with Codestral 22B. 533 edges written across 361 concepts. Blockstore now holds 1507 edges total. The relationship generator needed a model name fix — `codestral` → `codestral:22b`.

**Updated concept cards.** `app.js` now renders expandable inline cards instead of the modal approach. Cards show domain badge, title, preview, "Click to expand" hint. Expanded state reveals full definition, relationships with colored pills (Builds Upon, Related To, Specializes, Contradicts), and CID box. All styled with the new Navy/Indigo theme.

**Regenerated the gateway.** The new generator produced `concepts.json` with relationships and extra fields (insight, poetic_version, mantra). 636 concepts, 108 canonical domains, 1507 edges.

## What Worked

- The relationship harvest produced coherent edges. Samples looked right.
- The blockstore kept edges through git pulls — blockstore files are gitignored and live on Paperspace's disk.
- The new generator v3.3.0 ran clean after pulling from main.
- Expandable card rendering in `app.js` works with `concepts.json` data.

## What Broke

- **Model name mismatch.** Relationship generator called `codestral` but Ollama had `codestral:22b`. Fixed with sed.
- **Generator version confusion.** Paperspace had v3.2.1 while the repo had v3.3.0. Multiple pulls and stash operations needed to sync.
- **raw_batch files kept returning.** Relationship generator creates `raw_batch*.txt` artifacts. They got committed, pushed, pulled, deleted, recreated. Need `.gitignore` entries.
- **Auth failures.** Paperspace git credentials expired mid-push. Required retry.
- **Git conflicts.** Codespaces and Paperspace both had local changes. Multiple checkout --theirs/--ours resolutions.

## Decisions Made

- **Generator architecture.** The generator produces the data layer and app shell. Design files are separate and hand-maintained. Generator never overwrites `app.js`, `style.css`, or `splash.css`.
- **Cards render client-side.** No pre-baked HTML cards. `app.js` builds cards from `concepts.json`.
- **All four relationship types displayed.** Builds Upon, Related To, Specializes, Contradicts.
- **No modal.** Inline expand/collapse on the card itself.

## Nuggets Collected

- "The generator fills the data. The cards render the data. The design files stay untouched."
- "1507 edges. The mycelium is getting dense."
- "Codestral needs the full model name. Always."
- "raw_batch files are like weeds. Pull them and they come back."
- "Three machines, one repo. Chaos is the default state."

## Next Session

- Add raw_batch*.txt and raw_bridge*.txt to .gitignore
- Clean up remaining raw_batch files from the repo
- Regenerate mycelium map with new edges
- Test the live site on the droplet
- Consider SSH keys for Paperspace git auth
