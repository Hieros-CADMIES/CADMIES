---
type: protocol
version: 0.1.0
date: 2026-09-06
status: DRAFT
related: [[Note-Taking Protocol]], [[CADMIES-Canon]], [[NASA-level standards reference]]
---

# SOP Creation SOP

## Purpose

This document defines how Standard Operating Procedures (SOPs) are built as
local Obsidian vaults. One vault equals one SOP. The vault is the document.
Links are the navigation. The graph view is the map.

This SOP lives in the Scientific Obsidian repo because it governs how all
other SOPs are made. Operational SOPs built from this standard stay local
and private.

## Audience

The reader is anyone who picks up an SOP vault. The standard is simple:
if you can read, you can do it. No prior exposure to the system is assumed.
The SOP must carry a person from zero to operational without outside help.

## Core Principles

1. **One vault, one SOP.** No multi-topic vaults. Scope stays tight.
2. **Everything links.** Pages connect to pages, references connect to
   procedures, troubleshooting connects to causes. The link web is how a
   person navigates.
3. **The landing note is the front door.** It explains what the SOP is,
   how to use the vault, and links to every major section.
4. **Flat enough to grasp, deep enough to trust.** Keep the structure
   simple, but do not skip detail. A thousand-page light bulb manual
   compressed into notes that are actually useful.
5. **No assumed knowledge.** Every term is defined. Every command is
   explained. Every dependency is named.
6. **Local and private by default.** SOP vaults stay off the public repo.
   They may contain paths, internal names, and operational details.

## Vault Structure

Every SOP vault uses this base layout:
```text
Vault-Root/
├── SOP Landing.md # Front door — title, purpose, how to use, map
├── 01-Overview.md # Scope, terminology, system context
├── 02-Prerequisites.md # Everything needed before starting
├── 03-Procedures/ # Step-by-step work, split by task
│ ├── 03-01-Task-Name.md
│ ├── 03-02-Task-Name.md
│ └── 03-03-Task-Name.md
├── 04-References/ # Commands, configs, dependencies, schemas
│ ├── 04-01-Command-Reference.md
│ ├── 04-02-Configuration.md
│ └── 04-03-Dependencies.md
├── 05-Troubleshooting/ # Known failure modes and fixes
│ ├── 05-01-Symptom-Name.md
│ └── 05-02-Symptom-Name.md
└── 06-Appendices/ # Glossaries, checklists, deeper dives
├── 06-01-Glossary.md
└── 06-02-Checklist.md
```


Folders and files are numbered so order is obvious in the file tree.
Numbers also make wikilinks easier to scan.

## The Landing Note

The landing note is the most important file in the vault. It contains:

- The SOP title and one-sentence description
- What the system is and what it does
- How to use the vault (read order, graph view, search)
- A map of the vault's sections
- Status and version information

The landing note links to every section. Every section links back to it.
The landing note is the hub. The graph should look like a wheel with
spokes, plus cross-links between spokes where topics touch.

## Linking Rules

- Link aggressively. If a note mentions a dependency, link to the
  dependency note. If a procedure references a command, link to the
  command reference.
- Every note links back to the landing note.
- Every procedure links to its prerequisites and to related
  troubleshooting notes.
- Cross-link between sections when they share context. The graph view
  should reveal the shape of the system.
- Use full filenames in wikilinks, including the numeric prefix.
  Example: `[[03-01-Deploy-the-Service]]`

## Frontmatter

Every note in an SOP vault uses this lightweight frontmatter:

```text
---
sop: [SOP name]
section: [Landing | Overview | Prerequisites | Procedures | References | Troubleshooting | Appendices]
date: YYYY-MM-DD
status: [DRAFT | ACTIVE | DEPRECATED]
related: [[note-one]], [[note-two]]
---
```

The sop field ties every note back to its vault. The section field
keeps the graph organized. Local SOP vaults are not validated by the
repo automation, but the fields stay consistent anyway.

Writing Standard
Write like you are explaining the system to a smart person who has never
seen it. Casual tone, precise detail.

Every step is numbered.

Every command shows the full invocation and explains what it does.

Every dependency is named and linked.

Every assumption is stated.

Every term that is not common knowledge gets defined on first use.

Troubleshooting entries follow this shape: symptom, cause, fix.

No emojis. No fluff. Facts over decoration. If a step needs a diagram,
use ASCII art or a link to an image file in the vault.

Building an SOP Vault: Step by Step
Step 1: Define the scope
Before creating any files, write down:

What system or procedure this SOP covers

What the reader will be able to do after using it

What is explicitly out of scope

If the scope takes more than a paragraph, split it into multiple SOPs.

Step 2: Create the vault
Create a new Obsidian vault. Name it after the SOP.
Example: Ollama-Service-Operations

Step 3: Build the landing note
Create SOP Landing.md. Write the title, description, and how-to-use
section. List the six sections. Leave the map links for now — add them
as the sections are built.

Step 4: Build the skeleton
Create empty notes for every section, following the vault structure
above. Fill in frontmatter. Link every section note back to the
landing note.

Step 5: Fill in Overview and Prerequisites
Define the scope, terms, and context. List everything a person needs
before they can follow the procedures. Link dependencies to their
reference notes.

Step 6: Write the procedures
Write each procedure as its own note. Number the steps. Explain every
command. Link to references and troubleshooting as you go.

Step 7: Build references
Create command references, configuration notes, and dependency notes.
Link them from the procedures that use them.

Step 8: Write troubleshooting
Think through what can break. For each failure, write the symptom,
the cause, and the fix. Link from procedures and references.

Step 9: Add appendices
Glossary, checklists, diagrams, deeper explanations. Anything that
would slow down the main procedures gets pushed here and linked.

Step 10: Verify the graph
Open the graph view. Every note should be connected to the landing
note. There should be cross-links between related sections. No orphan
notes. Fix dead links. Then mark the SOP ACTIVE.

Quality Checklist
Before marking an SOP ACTIVE, verify:

Landing note links to every section

Every note links back to the landing note

Every command is explained

Every dependency is named and linked

Every troubleshooting entry has symptom, cause, fix

Glossary covers every non-obvious term

Graph view shows no orphan notes

A person with no system knowledge could follow it

Versioning
SOP vaults follow semantic versioning. The version lives in the landing
note frontmatter. Major changes restructure the vault. Minor changes
add sections or procedures. Patches fix errors.

Keep a version history note in the Appendices. Log what changed and why.

Relationship to Other Standards
This SOP builds on the [[Note-Taking Protocol]] for naming and linking
philosophy, [[CADMIES-Canon]] for ecosystem context, and the
[[NASA-level standards reference]] for rigor. Local SOP vaults are
exempt from repo validation, but the thinking carries over.
