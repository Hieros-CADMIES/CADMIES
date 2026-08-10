> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 044C - 2026-08-10 - Matadisco Viewer Clarification and Architecture Strategy

## Soundtrack

Clashing weather streams. Satellite streams & Coconut dreams.

## What We Did

- Confirmed the Matadisco viewer is a live stream, not a library browser
- Published test record with PNG preview — didn't appear in viewer
- Observed viewer logs: only records with `eo` and `stac` fields render
- Realized our records are on the network but not "live" when viewer opened
- Defined architecture: One source of truth (concepts.json), two interfaces (CADMIES Gateway + Matadisco-CADMIES Viewer)
- Discussed future of data vs image rendering
- El Hierro and 31UCR officially canon

## What We Learned

- Matadisco viewer is satellite-specific live stream, not a generic library
- Viewer displays records as they're published, not retroactively
- Preview field is universal but viewer rendering logic is hardcoded for `eo`/`stac`
- No need for a new viewer — we already have the CADMIES gateway for the public
- But we should build a Matadisco-CADMIES viewer for scientists/academics, pulling from the same source data

## Decisions Made

- Architecture: One source of truth (concepts.json), two interfaces (CADMIES Gateway + Matadisco-CADMIES Viewer)
- No double work — both views pull from the same source
- Matadisco-CADMIES viewer will be a separate portal for specialized discovery

## Nuggets Collected

- "The image is optional. The data is permanent."
- "The mycelium doesn't care how you render it. It just grows."
- "Crazy fuckers with mustard seed faith, sitting in a garage, looking at satellite data and dreaming up virtual coconuts on El Hierro."
- El Hierro — origin of the CADMIES spore
- 31UCR — France, Dr. Mistral's homeland

## Next Steps

- Build Matadisco-CADMIES viewer
- Share architecture plan with vmx
- Continue license audit and bulk publishing

---
*Let the mycelium grow!* 🌱
