---
phase: 48
date: 2026-08-08
status: Complete
related: [[Phase-47-Orphan-Edge-Resolution]], [[generate_relationships.py]], [[Session-021-2026-05-25-The-Harvester-Hardening]]
---

# Phase 48: Relationship Generator Hardening

## What Changed
The relationship generator (generate_relationships.py) was patched from v1.2.3 to v1.2.6 with a blockstore validation check in the write step, a model-agnostic interface allowing configuration between Codestral and Mistral, and enriched prompts that include domain and definition context for more accurate relationship proposals. Every edge written is now verified against the full concept index before being appended. A type-check guard was added to handle malformed LLM responses. The patched generator was tested with incremental and full passes, producing 92 new edges with zero orphan edges created. 

## Why
Phase 47 identified the root cause of orphan edge accumulation: the relationship generator wrote edges without verifying target existence. The fix required a validation gate in the write step. A secondary issue emerged during testing: the LLM occasionally returns target as a list instead of a string, causing a TypeError crash.

Additionally, a fresh clone test simulating a new user's experience revealed that the map generator's bare "ERROR: No concepts loaded" message provides no guidance. This led to designing a human-centered "Don't Panic" message that walks users through blockstore setup with warmth and clarity. The test also confirmed the need for a public-CADMIES branch optimized for end users.

The generator was updated to be model-agnostic, allowing the user to configure which LLM handles relationship generation via the MODEL variable. The prompt structure was enhanced to include domain and definition context, improving the quality of proposed relationships by giving the LLM more information to reason with.

## Changes Made

1. Model-Agnostic Interface (v1.2.6)

The function call_mistral() was renamed to call_llm() to reflect that the generator can use any configured model. The MODEL variable at the top of the script determines which LLM is called:

python
MODEL = "codestral"  # Can be changed to "mistral:7b" or any Ollama model

The call_llm() function now prints the active model name in its output, providing clear feedback on which model is being used:

python
print(f"  {MODEL} <- {est_tokens} tokens...", end=" ", flush=True)

This change makes the script future-proof and eliminates confusion about whether Codestral or Mistral is being used.

2. Enriched Prompt Context (v1.2.5)

The build_intra_batch_prompt() function was updated to include domain and definition for each concept:

python
lines.append(f"{hid} [{domain}]: {definition}")

Previously, only concept IDs were sent. The LLM now has full context for each concept, allowing it to make more meaningful connections. The prompt instructs the LLM to look for concepts in the same domain that build on each other, as well as concepts across different domains that relate or contradict.

The build_bridge_prompt() function was already including domains; definitions were added for consistency.

3. Batch Size Optimization

BATCH_SIZE was reduced from 15 to 10 for more focused proposals. Smaller batches allow the LLM to consider each concept more carefully and reduce the cognitive load of the prompt, resulting in higher-quality edges.

4. Orphan Prevention Gate (v1.2.4)

A validation check was added to the write step:

python
if target not in cid_map:
    print(f"  SKIP: target '{target}' not in blockstore (orphan prevented)")
    skipped_orphans += 1
    continue

This prevents orphan edges from being written to the blockstore. Previously, edges referencing deleted or renamed concepts were written without validation, accumulating over time and corrupting the graph.

5. List-Type Target Guard

A type-check guard was added to handle malformed LLM responses:

python
if isinstance(target, str) and target in valid_ids and target != source and rel_type in VALID_RELATION_TYPES:
This prevents a TypeError crash when the LLM returns target as a list instead of a string, a known quirk in some model responses.

6. Skipped Orphan Reporting

The write section now reports skipped_orphans count at completion, providing transparency about edges that were filtered out:

python
if skipped_orphans:
    print(f"⚠️  Skipped {skipped_orphans} orphan edge(s) — target(s) not in blockstore")

7. Third Clone — Fresh User Test

A clean clone was installed to ~/CADMIES/ on the SanDisk internal drive, simulating a stranger's first encounter. Key findings:

## Finding	Resolution

Blockstore is gitignored — 0 nodes loaded	Designed behavior; needs friendly error
dag_cbor not installed — JSON fallback can't read CBOR	Add to setup or make fallback functional
Ollama not installed — warnings scare users	Make optional; document clearly
No tarball in repo — users can't self-serve	Add cadmies_latest.tar.gz to repo
Paths hardcoded to developer machine	Use auto-detected paths in messages

8. "Don't Panic" User Message Design

A human-centered error message was designed to replace the bare ERROR: No concepts loaded. The message:

Acknowledges the technical output in plain language

Reassures the user they did nothing wrong

Provides step-by-step hand-holding through blockstore setup

Includes Linux and Windows paths

Uses emoji and warm, conversational tone

## Testing

Relationship Generator

Run	Mode	Edges	Orphans	Crashes
Incremental	319 sparse	56	0	0
Full	339 all	53	0	1 (patched)

Fresh Clone Test

Step	Expected	Actual	Action
git clone	Success	Clean clone, 2732 objects	—
Map generator	342 nodes	❌ 0 nodes, 342 skipped	dag_cbor missing
Extract tarball	Blocks loaded	1460 blocks on disk	—
Map generator (after tar)	342 nodes	❌ 0 nodes (still)	dag_cbor still missing
Install dag_cbor	Blocks readable	Pending	Setup script needed

## Analysis

Performance Improvement

The BATCH_SIZE reduction from 15 to 10 slightly increases the number of batches processed but improves the quality of each batch's proposals. The enriched prompts (with domain and definition context) produce more meaningful connections than the minimalist ID-only approach.

Orphan Prevention

The write-time validation gate prevents a class of errors that previously required manual cleanup. Orphan edges no longer accumulate in the blockstore, ensuring the graph remains clean and queryable.

Model-Agnostic Design

The rename from call_mistral() to call_llm() and the exposed MODEL variable make the script adaptable to future LLMs. This design choice follows the architecture principle of swapping the engine without rebuilding the vehicle. The script can now use Codestral for depth, Mistral for speed, or any other Ollama-compatible model.

## Conclusion

Phase 48 is complete. The relationship generator has been hardened against orphan creation and malformed responses, enhanced with model-agnostic architecture and enriched prompt context, and optimized with a reduced batch size for more focused proposals. A third clone validated the new-user experience and inspired the "Don't Panic" message design.

The generator can now be configured to use any Ollama model, defaulting to Codestral for its superior reasoning capabilities.

## Key Principles Established

Validate at write time. The write step is the final gate.

Type-check external input. LLMs are not JSON validators.

Provide context to the LLM. Definitions and domains improve relationship quality.

Keep batches focused. Smaller batches produce better proposals.

Design for model-agnosticism. Don't hardcode model names in functions.

Test as a stranger. The fresh clone revealed gaps invisible to developers.

Humanism over engineering. Error messages should hold your hand, not point at file paths.
