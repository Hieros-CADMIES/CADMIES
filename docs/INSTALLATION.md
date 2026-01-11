# Detailed Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Python**: 3.8 or higher
- **Storage**: 50MB free space
- **Memory**: 512MB RAM

### Recommended Requirements
- **Python**: 3.10 or higher
- **Storage**: 500MB for extensive knowledge bases
- **Memory**: 2GB+ RAM for large operations

## Installation Methods

### Method 1: Basic Installation (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install dag-cbor multiformats

# 4. Verify installation
python -c "import dag_cbor, multiformats; print('✅ Dependencies installed successfully')"

Method 2: Development Installation
bash

# Clone with all branches
git clone --recursive https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES

# Install development dependencies
pip install dag-cbor multiformats pytest jupyter

# Run test suite to verify
python -m pytest tests/ -v

Method 3: Docker Installation (Advanced)
Dockerfile

# Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install dag-cbor multiformats
CMD ["python", "cid_generator_v1.1.0.py"]

Configuration
Directory Structure

After first run, the system creates:
text

./
├── blocks/          # CBOR-encoded knowledge blocks
├── index/           # Human ID to CID mapping
├── logs/            # Operation logs
└── schemas/         # Schema definitions

Environment Variables (Optional)
bash

# Custom storage paths
export IPLD_BLOCKS_DIR="/path/to/blocks"
export IPLD_INDEX_DIR="/path/to/index"
export IPLD_LOGS_DIR="/path/to/logs"

# Verbose logging
export IPLD_VERBOSE="true"

Verification
Test 1: Basic Functionality
bash

# Generate a sample concept
python cid_generator_v1.1.0.py

# Check directories were created
ls -la blocks/ index/ logs/

Test 2: Read/Write Cycle
bash

# Create a simple test concept
cat > test_concept.json << 'EOF'
{
  "schema_version": "1.0.0",
  "human_id": "test_installation",
  "title": "Installation Test",
  "definition": "Testing the installation",
  "type": "Test",
  "domain": "Testing",
  "metadata": {
    "created": "2026-01-07T12:00:00Z",
    "creator": "TestUser",
    "certainty_score": 0.9,
    "version": 1,
    "purpose": "testing"
  }
}
EOF

# Generate CID
python cid_generator_v1.1.0.py --concept-file test_concept.json

# Read it back
python cbor_reader.py test_installation

# Clean up
rm test_concept.json

Test 3: Schema Validation
bash

# Verify schema file exists
ls -la schemas/universal_scientific_concept_schema_v1.0.0.json

# Check schema is valid JSON
python -m json.tool schemas/universal_scientific_concept_schema_v1.0.0.json > /dev/null && echo "✅ Schema is valid JSON"

Platform-Specific Notes
Linux/Mac
bash

# Ensure Python is installed
python3 --version

# Install pip if missing
sudo apt-get install python3-pip  # Debian/Ubuntu
brew install python3              # macOS

Windows (WSL2 Recommended)
bash

# Enable WSL2
wsl --install

# Install Python in WSL
sudo apt update
sudo apt install python3 python3-pip

# Continue with Method 1 above

Windows Native (Not Recommended)
powershell

# Install Python from python.org
# Add Python to PATH during installation

# Install dependencies
pip install dag-cbor multiformats

# Note: Some features may require WSL2 for full compatibility

Troubleshooting Installation
Common Issues

Issue: "Command not found: python"
bash

# Try python3 instead
python3 --version
python3 cid_generator_v1.1.0.py

Issue: "Module not found: dag_cbor"
bash

# Reinstall with pip
pip uninstall dag-cbor multiformats -y
pip install dag-cbor multiformats --upgrade

Issue: Permission denied creating directories
bash

# Check current directory permissions
ls -la .

# Create directories manually if needed
mkdir -p blocks index logs

Issue: Python version too old
bash

# Check Python version
python --version

# Install Python 3.8+ if needed
# Ubuntu/Debian: sudo apt install python3.10
# macOS: brew install python@3.10
# Windows: Download from python.org

Next Steps

After successful installation:

    Run tests to verify everything works

    Explore examples to see usage patterns

    Read user manual for complete documentation

For additional help: hieroscadmies@proton.me