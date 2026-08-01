⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, unfiltered thoughts, and coded messages for fellow gardeners. For polished documentation, check Polished CADMIES or promote this note.

# Session-045-2026-07-31-ORCID-Integration-and-Site-Sync

# Soundtrack
nature

# What We Did

Added ORCID iD (0009-0000-8877-2731) to the public gateway stats bar

Made the ORCID iD a clickable link to https://orcid.org/0009-0000-8877-2731

Regenerated public gateway with ORCID changes

Verified ORCID link is live on project-hierion.org

Renamed DigitalOcean droplet

Connected ORCID to personal GitHub profile

Updated ORCID profile with biography and project links

Pulled latest to Paperspace after ORCID link change

# What Worked

ORCID link works on the live site

Droplet rename was quick and painless

GitHub ORCID connection went through smoothly

# What Broke

Paperspace was out of sync with GitHub (174 commits behind, 2 local commits ahead)

Rebase conflict in harvest_full_pipeline.py

Generator couldn't find concepts until dag-cbor was installed

Droplet had local changes blocking the pull (stash fixed it)

# Decisions Made

ORCID goes in the stats bar next to the license

ORCID bio is complete and ready

Site design ideas parked for future session

# Nuggets Collected

"On vacation — no expiration" is the gardener's permament GitHub status

ORCID profile is now a proper scientific record

The bio: "all built from a garage in South Texas, without institutional backing"

Next Steps
Site design: CSS/SVG fluid background test, then canvas particle network

Update SOP documents (droplet name, ORCID info)
