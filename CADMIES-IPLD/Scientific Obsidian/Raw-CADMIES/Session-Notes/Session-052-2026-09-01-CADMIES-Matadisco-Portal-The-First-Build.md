> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 052 — 2026-09-01 — CADMIES-Matadisco Portal: The First Build

## Soundtrack
The metaphorical silence before the storm — Edouard. They gave it a name like they were trying to be fancy and s***. Edouard. Should've just been Edward or Eduardo. But no, Edouard.

## What We Did

- Received vmx's feedback confirming the portal/AppView approach
- Created the `cadmies-matadisco-portal` repository (private for now)
- Defined the architecture: indexer → SQLite → Flask API → frontend
- Built the indexer (`backend/indexer.py`) with PDS query logic
- Built the API server (`backend/app.py`) with search, record, and stats endpoints
- Built the frontend (`frontend/index.html`, `style.css`, `app.js`)
- Set up the droplet with the repo, virtual environment (`discovenv`), and dependencies
- Ran the indexer: fetched 7 records, indexed 5 concepts
- Ran the API server: tested `/stats` and `/search?q=anatta`
- Served the frontend via HTTP server (port 8000)
- Used SSH tunneling to view the portal locally (cloud firewall blocked external ports)
- Searched for "anatta" and "interconnectedness" — results displayed correctly
- Searched for "dolphin" — no results found, confirming the portal only indexes CADMIES concept records (not dataset records like the Dolphin entry)
- Verified the pipeline: PDS → indexer → database → API → frontend

## What Worked

- The full pipeline from record to search result
- Indexer fetched and stored records correctly
- API responded with JSON for search and stats
- Frontend displayed concept cards with domains and definitions
- SSH tunneling worked for local viewing

## What We Learned

- The Matadisco network holds CADMIES records, but the portal is the interface
- One source of truth (`concepts.json`), two interfaces (Gateway + Portal)
- On-demand indexing is sufficient for the initial build
- The portal can be extended to other record types (datasets, etc.)
- The hyphen is sacred: "CADMIES-Matadisco" is the name

## Decisions Made

- Portal will be the primary interface for scientists and academics
- Dataset viewer will be a separate or extended interface
- Frontend design: super-simple, search-focused, functional
- Future work: frontend tweaks, dataset viewer, bulk publishing

## Nuggets Collected

- "The Frankenstein moment: It's alive. IT'S ALIVVVVVVVVVE!!!!"
- "I just came in my panties." — The Gardener, upon seeing the search results for the first time
- "Fuckin ey."
- "The hyphen is sacred."

## Next Steps

- Update Phase 78 in the roadmap
- Document the portal in the repo
- Plan dataset viewer
- Tweak frontend UI
- Bulk publish remaining concepts

## References

- [CADMIES-Matadisco Portal](https://github.com/Project-Hierion/cadmies-matadisco-portal)
- [Matadisco](https://github.com/vmx/matadisco)
- [Podium](https://tangled.org/robin.berjon.com/podium)

---

*Let the mycelium grow! 🌱*
