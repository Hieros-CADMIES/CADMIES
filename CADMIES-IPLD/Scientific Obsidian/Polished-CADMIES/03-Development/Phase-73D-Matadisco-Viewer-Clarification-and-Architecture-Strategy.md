---
phase: 73D
date: 2026-08-10
status: Active
related: [[Phase-73C-Matadisco-Reverse-Domain-Implementation-and-Bulk-Readiness]], [[Session-044C-2026-08-10-Matadisco-Viewer-Clarification-and-Architecture-Strategy]]
---

# Phase 73D - Matadisco Viewer Clarification and Architecture Strategy

## What Changed

We confirmed that the Matadisco viewer is a **live stream** rather than a library browser. Our test records, while successfully published to the network, do not appear in the viewer because:

1. The viewer only renders records published while the page is open
2. The viewer's rendering logic is hardcoded for satellite data (records with `eo` and `stac` fields)
3. Our records have `preview` images but lack `eo` and `stac` fields

This clarified the distinction between the Matadisco network (which stores records permanently) and the Matadisco viewer (which displays live streaming data).

## Why

Understanding the viewer's behavior was essential for planning the next phase of Matadisco integration. We needed to determine whether to extend the existing viewer or build a separate one for CADMIES records.

## Changes Made

### Viewer Testing

- Published a test record with a PNG preview (`https://project-hierion.org/favicon.png`)
- Observed the viewer's console logs to understand rendering behavior
- Confirmed that only records with `eo` and `stac` fields appear on the page
- Verified that the viewer is a live stream, not a library browser

### Key Observations

| Observation | Implication |
|-------------|-------------|
| Viewer displays records as they're published, not retroactively | Our records are on the network but won't appear unless published while viewer is open |
| Only records with `eo` and `stac` fields render | Viewer is hardcoded for satellite data |
| Preview field is universal but viewer rendering logic is selective | Extending the viewer would require modifying `web.js` |

### Architecture Decision

We defined a two-interface architecture:

1. **CADMIES Gateway** (`project-hierion.org`) — General public interface. Pulls from `concepts.json`. Renders the library with definitions, domains, relationships, and the mycelium map.

2. **Matadisco-CADMIES Viewer** (to be built) — Specialized interface for scientists and academics. Pulls from the same `concepts.json`. Designed for decentralized discovery and querying.

**One source of truth. Two interfaces. No double work.**

## Testing

### Viewer Stream Observation

Leaving the viewer browser open confirmed that new satellite records continue to appear as they're published — proving it's a live stream, not a loading delay.

### Record Visibility

Our CADMIES records are visible in the network (verified via direct PDS query) but not in the viewer, confirming the viewer's satellite-specific filtering.

## Results

| Finding | Status |
|---------|--------|
| CADMIES records are on the network | ✅ Confirmed |
| Records have valid `preview` images | ✅ Confirmed |
| Viewer displays satellite records | ✅ Confirmed |
| Viewer displays CADMIES records | ❌ Not currently |
| Architecture defined | ✅ Completed |

## Analysis

### What Worked
- The preview test confirmed the record structure is valid
- The network accepted and stored the records
- The viewer's behavior is now clearly understood

### What We Learned
1. **The Matadisco viewer is a live stream, not a library.** It shows records as they're published, not retroactively.
2. **Rendering is hardcoded for satellite data.** The viewer ignores records without `eo` and `stac` fields.
3. **The `preview` field is universal but the viewer's rendering logic is not.** Extending the viewer would require a PR.
4. **We already have the library we need.** The CADMIES gateway is the public interface. A specialized Matadisco-CADMIES viewer would serve scientists and academics.

### Broader Implications
- **Data vs. Images:** The satellite images are rendered from data, not stored as images. This confirms Matadisco's role as a data network, not an image repository.
- **Future-Proofing:** The same data can be rendered in increasingly sophisticated ways over time (3D, holographic, etc.).
- **CADMIES Parallel:** Our concepts are the data. The gateway is the renderer. The future will render them in ways we can't yet imagine.

## Conclusion

Phase 73D clarified the distinction between the Matadisco network and the Matadisco viewer. We confirmed our records are on the network, defined the architecture for a specialized CADMIES viewer, and established that the data is the source of truth — images are just renderings.

## Next Steps

1. Build the Matadisco-CADMIES viewer, pulling from `concepts.json`
2. Share the architecture plan with vmx
3. Continue the full license audit of LLMDataHub datasets
4. Scale up to publish all 636 CADMIES concepts

## References

- [Matadisco Viewer](https://vmx.github.io/matadisco-viewer/)
- [AT Protocol Firehose Documentation](https://atproto.com/guides/streaming)
- [Project Hierion Matadisco Repo](https://github.com/Project-Hierion/hierion-matadisco)

---

*Let the mycelium grow!* 🌱
