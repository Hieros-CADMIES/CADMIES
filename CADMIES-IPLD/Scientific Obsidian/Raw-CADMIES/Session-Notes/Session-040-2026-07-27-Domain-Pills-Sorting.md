<!-- TEMPLATE: wikilinks in this file are teaching examples -->
> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 040 — 2026-07-27 — Domain Pills Sorting

## Soundtrack
Nature. Crickets. The distant rumble of a summer storm rolling in.

## What We Did

**Fixed the public gateway domain filter pills.** The 15 domain filter buttons at the top of the CADMIES public gateway (project-hierion.duckdns.org) have been decorative for who knows how long. Clicking them did nothing. The filter logic existed in the generator script — `setFilter()` was a real function — but the `onclick` attributes in the HTML were being treated as strings by the browser, not executable code. The buttons were dead.

**The fix:** Replaced inline `onclick` attributes with `addEventListener` bindings in the JavaScript section of the generator script. Now when you click "Physics" or "Philosophy" or "Spirituality," the concept cards actually filter. The results counter updates to show "Showing X of Y concepts."

**Transferred the blockstore to the droplet.** The droplet had the repository but the actual concept blocks were missing — 0 concepts loaded. The blockstore lived on Paperspace. Tarred it up (586K for 2065 CBOR files), set up SSH keys, SCP'd it over. Now the droplet has the full blockstore.

**Regenerated the site.** Installed dag-cbor on the droplet (had to use `--break-system-packages` because Ubuntu 24.04 blocks system-wide pip). Ran the generator script. 636 concepts across 107 canonical domains with 1,131 edges. Site is live.

**Recovered from a file corruption.** During troubleshooting, accidentally overwrote the generator script with a shell heredoc instead of Python code. Syntax error on line 1. Used `git reset --hard origin/main` to restore from GitHub. Pulled commit b245ede — the corrected version. Lesson learned: double-check the cat redirect before hitting enter.

**Tried to set up a DuckDNS domain for Paperspace.** Failed — reCaptcha issue during domain creation. Not critical. The droplet's domain works fine.

## What Worked
- addEventListener approach — filter pills now functional
- Blockstore transfer via tar + scp — 586K, quick and clean
- SSH key setup from Paperspace to droplet — persistent access now
- dag-cbor installation with `--break-system-packages` — bypassed Ubuntu's protection
- git reset --hard to recover corrupted file — thank god for version control
- Site regeneration — 636 concepts, search still works, filter counter updates

## What Broke
- Inline onclick attributes — treated as strings, not functions. Useless in dynamically generated HTML.
- Generator script accidentally overwritten — shell heredoc instead of Python. Recovered via git.
- DuckDNS domain creation for Paperspace — reCaptcha blocked it. Not a real loss.
- git checkout with wrong path — used `CADMIES-IPLD/tools/` instead of `tools/`. Git paths are relative to repo root.

## Decisions Made
- Use addEventListener for all future dynamic HTML generation — inline onclick is dead to us
- The droplet's blockstore is separate from the repository — must be transferred independently after harvests
- DuckDNS for Paperspace is nice-to-have, not essential — deprioritized

## Nuggets Collected
- "Inline onclick attributes are treated as strings. addEventListener or die."
- "The blockstore travels via tarball. Always has. Always will."
- "Ubuntu 24.04 protects you from yourself. --break-system-packages says 'I know what I'm doing.'"
- "git reset --hard is the emergency brake. Don't be afraid to pull it."
- "The filter pills were decorative for months. Nobody noticed. Now they work. The mycelium awakens."

## Current State (Post-Session)
- Public gateway: ✅ Domain filter functional, search functional, 636 concepts live
- Blockstore: ✅ On both Paperspace and droplet
