# IPLD Knowledge Tools - Complete User Manual

## 🎯 What This System Does
A local-first, content-addressed knowledge system that lets you:
- **Store knowledge** with permanent, verifiable addresses (CIDs)
- **Retrieve knowledge** using those addresses or human-readable IDs
- **Structure information** using a standardized schema
- **Create trustworthy** knowledge systems where content can't be silently altered

## 📋 Quick Navigation

### For New Users
1. **[Quick Start](QUICK_START.md)** - 5-minute setup
2. **[Installation Guide](INSTALLATION.md)** - Detailed setup
3. **[Testing Guide](TESTING_GUIDE.md)** - Verify everything works

### For Practical Use
4. **[Use Cases](USE_CASES.md)** - Real-world applications
5. **[Examples Directory](../examples/)** - Ready-to-use examples

### For Advanced Users
6. **[Advanced Usage](ADVANCED_USAGE.md)** - Custom schemas, extensions
7. **[API Reference](../src/API_REFERENCE.md)** - Technical details

### When Things Go Wrong
8. **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues & solutions

## 🏗️ System Architecture Overview

Your Knowledge → CID Generator → CID (Content ID) → Blockstore
↑ ↓
Human ID ←─── CBOR Reader ←─── .cbor file
text


### Core Components:
1. **`cid_generator.py`** - Creates CIDs from knowledge concepts
2. **`cbor_reader.py`** - Reads knowledge by CID or human ID
3. **`schemas/universal_scientific_concept_schema_v1.0.0.json`** - Standard format

## 🚀 The 3-Step Workflow

### Step 1: Create Knowledge
```bash
python cid_generator.py --concept-file my_knowledge.json
# Output: CID, saved to ./blocks/

Step 2: Retrieve Knowledge
bash

# By CID
python cbor_reader.py bafyrei...

# By human ID
python cbor_reader.py my_concept_id

Step 3: Verify & Share

    Same content always produces same CID

    Share CIDs for verifiable knowledge sharing

    Build knowledge graphs using relationships

📚 Learning Pathways
Path A: Casual User (30 minutes)

    Quick Start guide

    Try one example concept

    Generate and read back a CID

Path B: Educator/Researcher (2 hours)

    Complete installation

    Explore use cases

    Adapt templates for your needs

    Run verification tests

Path C: Developer (4+ hours)

    Full installation with testing

    Examine schema and extensions

    Review advanced usage

    Contribute improvements

🔒 Ethical & Licensing

This system is licensed under AGPLv3 with Commons Clause:

    ✅ Free for: Education, research, personal use, open source projects

    ✅ Requires permission for: Commercial SaaS, proprietary AI training

    📧 Contact: hieroscadmies@proton.me for commercial inquiries

🤝 Getting Help

    Check Troubleshooting first

    Review examples in /examples/ directory

    Examine test files to see expected behavior

    Email questions to: hieroscadmies@proton.me

📈 Next Steps

    ✅ Install - Get the system running

    ✅ Test - Verify everything works

    ✅ Learn - Understand the workflow

    ✅ Apply - Use for your projects

    ✅ Extend - Customize for your needs

    ✅ Share - Contribute improvements

"Knowledge should be as trustworthy as mathematics."