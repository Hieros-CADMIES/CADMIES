---
phase: 73E
date: 2026-09-01
status: Complete
related: [[Phase-73D-Matadisco-Viewer-Clarification-and-Architecture-Strategy]], [[Session-052-2026-09-01-CADMIES-Matadisco-Portal-The-First-Build]], [[Phase-73C-Matadisco-Reverse-Domain-Implementation-and-Bulk-Readiness]]
---

# Phase 73E — CADMIES-Matadisco Portal: Build and Deployment

## What Changed

We built and deployed a dedicated viewer for CADMIES concept records on the Matadisco network. The portal provides a specialized search and discovery interface for scientists and academics, pulling from the same source of truth (`concepts.json`) as the CADMIES gateway.

**One source of truth. Two interfaces.**

## Why

Phase 73D confirmed that the Matadisco viewer is a live stream (satellite-specific) and not a library browser. Our CADMIES records, while published to the network, were not appearing in the Matadisco viewer. vmx validated our approach: build a dedicated portal for our own community's data.

> "Your approach is exactly what I'd expect. It fits into the vision of Matadisco, that people create their own 'portals' where the data of their specific community can easily be viewed/accessed." — vmx

## Changes Made

### Infrastructure
- Created `cadmies-matadisco-portal` repository (private)
- Set up directory structure on the droplet (`/home/Project/cadmies-matadisco-portal/`)
- Established virtual environment (`discovenv`) in the backend
- Installed dependencies: `atproto`, `requests`, `Flask`, `Flask-CORS`

### Architecture
```
PDS (AT Protocol)
│
▼
┌─────────────────────────────────────────────────────────────┐
│ CADMIES-Matadisco Portal │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐ │
│ │ Indexer │───▶│ SQLite │───▶│ Flask API │ │
│ │ (Python) │ │ Database │ │ (REST) │ │
│ └─────────────┘ └─────────────┘ └─────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────┐│
│ │ Frontend ││
│ │ (HTML/CSS/JS) ││
│ └─────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```


### Components

| Component | File | Technology | Purpose |
|-----------|------|------------|---------|
| Indexer | `backend/indexer.py` | Python | Queries PDS for CADMIES records, stores in SQLite |
| Database | `data/portal.db` | SQLite | Local cache of indexed records |
| API | `backend/app.py` | Flask | Serves search, record, and stats endpoints |
| Frontend | `frontend/` | HTML/CSS/JS | User interface for searching and displaying concepts |

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service metadata |
| `/search?q=...` | GET | Full-text search across concept names and definitions |
| `/record/<uri>` | GET | Retrieve a complete record by AT-URI |
| `/stats` | GET | Total number of indexed concepts |

### Naming Convention

The hyphen is sacred. The project is named **CADMIES-Matadisco Portal**, not "Matadisco CADMIES" or "CADMIES Matadisco." The repo is `cadmies-matadisco-portal`.

## Testing

### Indexer Test
- Authenticated with PDS using `gardener.pds.project-hierion.org`
- Fetched 7 records from the PDS
- Indexed 5 new records into SQLite
- Database initialized successfully at `/data/portal.db`

### API Test
- `/stats` endpoint returned `{"total_concepts": 5}`
- `/search?q=anatta` returned three matching concept records
- API running on port 5000 (Flask development server)

### Frontend Test
- Served via Python HTTP server on port 8000
- Viewed locally via SSH tunnel (cloud firewall blocked external ports)
- Search for "anatta" returned concept cards with:
  - Concept name
  - Domains
  - Definition
  - Publication date
- Search for "interconnectedness" returned two concept records
- Search for "dolphin" returned no results (dataset record, not a concept record)

### Pipeline Verification

| Step | Status |
|------|--------|
| PDS authentication | ✅ |
| Record fetch | ✅ (7 records) |
| Record indexing | ✅ (5 concepts) |
| API response | ✅ |
| Frontend display | ✅ |

## Results

### Portal Functionality

| Feature | Status |
|---------|--------|
| Search by concept name | ✅ |
| Search by definition | ✅ |
| Display concept cards | ✅ |
| Show domains | ✅ |
| Show definitions | ✅ |
| Show publication dates | ✅ |
| Stats display | ✅ |

### Live Sites Confirmed

| Site | Status |
|------|--------|
| CADMIES Gateway (`project-hierion.org`) | 200 ✅ |
| PDS (`pds.project-hierion.org`) | 200 ✅ |

### Indexed Records

| Concept | Records Found |
|---------|---------------|
| Anatta Not Self | 3 |
| Interconnectedness | 2 |
| Dolphin (dataset) | 0 |

## Analysis

### What Worked
- The indexer successfully authenticated with the PDS
- Records were fetched, indexed, and stored correctly
- The API responded with JSON for search and stats
- The frontend displayed concept cards with all relevant metadata
- The full pipeline from PDS to search result was verified

### What We Learned
- Matadisco records are immutable; the portal indexes them on-demand
- On-demand indexing is sufficient for the initial build
- The portal can be extended to other record types (datasets, etc.)
- The hyphen is sacred in naming: "CADMIES-Matadisco"
- SSH tunneling bypasses cloud firewall restrictions for local viewing

### Challenges
- Cloud firewall blocked external access to ports 5000 and 8000
- Resolved: used SSH tunneling for local viewing
- Payment due on DigitalOcean account prevented firewall changes
- Resolved: worked around it

## Conclusion

Phase 73E is complete. The CADMIES-Matadisco Portal is built, deployed, and functional. The pipeline from PDS to search result is verified. The portal provides a dedicated interface for scientists and academics to discover CADMIES concepts on the Matadisco network.

## Next Steps

1. **Dataset viewer** — Extend or create a separate viewer for LLMDataHub records
2. **Frontend tweaks** — Improve search experience, add filters, enhance UI
3. **Live indexing** — Add WebSocket or event-driven updates
4. **Bulk publishing** — Publish the remaining 636 concepts
5. **Documentation** — Update roadmap, session notes, and README

## References

- [CADMIES-Matadisco Portal](https://github.com/Project-Hierion/cadmies-matadisco-portal)
- [Matadisco](https://github.com/vmx/matadisco)
- [Podium](https://tangled.org/robin.berjon.com/podium)
- [hierion-matadisco](https://github.com/Project-Hierion/hierion-matadisco)

---

*Let the mycelium grow!* 🌱
