---
type: pipeline-doc
pipeline: Core
date: 2026-08-15
related: []
---

# PIPELINE FLOW
```text
CONVERSATION / TEXT
        │
        ▼
┌─────────────────┐
│  HARVEST        │
│  harvest_full_  │
│  pipeline.py    │
│                 │
│  chunks text    │
│  searches       │
│  mycelium       │
│  extracts via   │
│  Mistral        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SOURCE         │
│  CONCEPTS       │
│  *.json files   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  VALIDATE       │
│  scientific_    │
│  validator.py   │
│                 │
│  BASIC/STANDARD │
│  RIGOROUS/      │
│  STRICT         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MINT           │
│  cid_generator  │
│  .py            │
│                 │
│  generates CID  │
│  saves .cbor    │
│  updates index  │
│  logs operation │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PROVENANCE     │
│  provenance_    │
│  manager.py     │
│                 │
│  creation       │
│  records        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  BLOCKSTORE     │
│  store/blocks/  │
│  store/index/   │
│  store/logs/    │
└────────┬────────┘
         │
         ├──────────────────────┐
         │                      │
         ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│  RELATIONSHIPS  │    │  ENRICHMENT     │
│  generate_      │    │  enrich_        │
│  relationships  │    │  concepts.py    │
│  .py            │    │                 │
│                 │    │  fills gaps     │
│  Codestral      │    │  via LLM        │
│  proposes edges │    │  remints        │
└────────┬────────┘    └────────┬────────┘
         │                      │
         └──────────┬───────────┘
                    │
                    ▼
         ┌─────────────────┐
         │  REMINT         │
         │  remint_        │
         │  existing_      │
         │  concepts.py    │
         │                 │
         │  new CIDs for   │
         │  changed blocks │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  VERIFY         │
         │  scientific_    │
         │  audit.py       │
         │                 │
         │  4-part check   │
         └────────┬────────┘
                  │
                  ├──────────────────────┬──────────────────────┐
                  │                      │                      │
                  ▼                      ▼                      ▼
         ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
         │  GENERATE       │    │  GENERATE       │    │  EXPORT         │
         │  GATEWAY        │    │  MAP            │    │  export_to_     │
         │  generate_      │    │  generate_      │    │  car.py         │
         │  public_        │    │  mycelium_      │    │                 │
         │  gateway.py     │    │  map.py         │    │  CAR files for  │
         │                 │    │                 │    │  sharing        │
         │  index.html     │    │  mycelium_map   │    └────────┬────────┘
         │  concepts.json  │    │  .html          │             │
         │  sitemap.xml    │    │                 │             ▼
         └─────────────────┘    └─────────────────┘    ┌─────────────────┐
                                                        │  IMPORT        │
                                                        │  import_from_  │
                                                        │  car.py        │
                                                        │                │
                                                        │  restores      │
                                                        │  blocks        │
                                                        └─────────────────┘
```
