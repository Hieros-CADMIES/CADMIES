# IPLD Knowledge Tools

**Content-Addressed Systems for Educational Knowledge Management**

## 🎯 Purpose

This project provides tools for creating, storing, and retrieving knowledge concepts using IPLD (InterPlanetary Linked Data) and content addressing. It demonstrates how deterministic content identifiers (CIDs) can create reliable knowledge systems where the same understanding always leads to the same address.

## 🛠️ Available Tools

### 1. CID Generator (`cid_generator_v1.1.0.py`)
Generates Content Identifiers (CIDs) from structured knowledge concepts using DAG-CBOR encoding.

**Features:**
- Creates deterministic CIDs from JSON knowledge concepts
- Maintains human-readable indexes
- Includes audit logging for educational use
- Compatible with universal scientific concept schema

### 2. CBOR Reader (`cbor_reader.py`)
Retrieves and displays knowledge concepts stored in IPLD/CBOR format.

**Features:**
- Reads concepts by CID or human-readable ID
- Validates schema compliance
- Formats knowledge for educational display
- Configurable storage paths

### 3. Universal Scientific Concept Schema (`schemas/universal_scientific_concept_schema_v1.0.0.json`)
Standardized JSON Schema for representing educational and scientific concepts.

**Features:**
- JSON Schema draft-07 compliant
- Supports multi-level explanations (beginner to expert)
- Includes metadata for provenance and licensing
- Designed for research and educational applications

## 🧪 Hands-On Testing

**New to content addressing? Want to verify the system works on your computer?**

We've created a complete beginner's guide that walks you through every step:

👉 **[Testing the IPLD Knowledge System: A Complete Beginner's Guide](./docs/TESTING_GUIDE.md)**

**Perfect for:**
- First-time users with no programming experience
- Educators wanting to demonstrate content addressing  
- Researchers verifying system behavior
- Anyone who learns best by doing

**You'll learn how to:**
1. ✅ Set up Python and required tools (we guide you through it)
2. ✅ Generate your first Content Identifier (CID)
3. ✅ Retrieve knowledge using that CID
4. ✅ Verify the system is deterministic (critical test!)
5. ✅ Understand what "content addressing" means in practice

**No prior knowledge needed** - starts from "how to open your terminal"

## 📚 How It Works
Content Addressing Principle
text

Same Knowledge → Same CID → Same Understanding

The system ensures that:

    Identical content always produces the same CID

    CIDs can be shared and verified independently

    Knowledge remains permanently addressable

Complete Workflow

    Create knowledge concepts with standardized schema

    Generate CIDs using DAG-CBOR encoding

    Store in local blockstore with index

    Retrieve by CID or human-readable ID

    Verify content integrity through hashing

🏗️ Architecture
Schema-Based Knowledge

All concepts follow the universal_scientific_concept_schema_v1.0.0.json which defines:

    Required fields (title, definition, domain, metadata)

    Multi-level explanations for different audiences

    Cross-references and relationships

    Provenance and licensing information

Local-First Storage

    All data stored locally in ./blocks/ directory

    Human-readable index maintained in ./index/

    Operation logs in ./logs/ for auditing

    No external dependencies or cloud services

## ⚖️ License & Ethical Use
License

AGPLv3 with Commons Clause - See LICENSE
Permitted Uses

    ✅ Individual learning and research

    ✅ Academic institutions and non-profits

    ✅ Open source projects

    ✅ Personal knowledge management

Restricted Uses (Commons Clause)

    ❌ Commercial SaaS offerings without contributing back

    ❌ Proprietary AI training without reciprocity

    ❌ Commercial products that don't share improvements

For commercial licensing: Contact hieroscadmies@proton.me

📁 Repository Structure

```text
philosophical-ipld-tools/
├── cid_generator_v1.1.0.py    # CID generation tool
├── cbor_reader.py             # Knowledge retrieval tool
├── schemas/                   # Knowledge schemas
│   └── universal_scientific_concept_schema_v1.0.0.json
├── LICENSE                    # AGPLv3 + Commons Clause
└── README.md                  # This file
```

## 🔗 Related Resources

* IPLD Documentation: https://ipld.io/
* DAG-CBOR Specification: https://ipld.io/specs/codecs/dag-cbor/
* CID Explanation: https://docs.ipfs.tech/concepts/content-addressing/

🤝 Contributing

This project welcomes educational and research-focused contributions. Please ensure all contributions align with the project's ethical framework and licensing terms.
📞 Contact

For questions about ethical use, commercial licensing, or research collaboration: hieroscadmies@proton.me

"Knowledge should be free to access, but its commercial use should benefit the commons."
