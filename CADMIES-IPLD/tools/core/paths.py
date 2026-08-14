#!/usr/bin/env python3
"""
File: paths.py
Tool: CADMIES Path Manager
Version: 1.1.0
System: CADMIES / tools/core
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Centralized path management for all CADMIES tools.
         Resolves project root and standard directories dynamically.

Usage:
    from paths import BLOCKS_DIR, INDEX_DIR, LOGS_DIR, SOURCE_CONCEPTS_DIR, ensure_dirs

Version History:
    v1.0.0: Initial release. Dynamic root resolution, store paths, ensure_dirs().
    v1.1.0: Added SOURCE_CONCEPTS_DIR for concept storage.
            Added error handling and confirmation output to ensure_dirs().
            Added scientific documentation YAML metadata block.
"""

from pathlib import Path

# Get project root (CADMIES-IPLD/) - this file is in tools/core/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Standard paths
STORE_DIR = PROJECT_ROOT / "store"
BLOCKS_DIR = STORE_DIR / "blocks"
INDEX_DIR = STORE_DIR / "index"
LOGS_DIR = STORE_DIR / "logs"
SOURCE_CONCEPTS_DIR = PROJECT_ROOT / "source_concepts"

# Index file path
INDEX_FILE = INDEX_DIR / "human_id_to_cid.json"

# Docs output directory (public gateway)
DOCS_DIR = PROJECT_ROOT.parent / "docs"

# Ensure directories exist
def ensure_dirs():
    """Create all required directories if they don't exist.
    
    Returns:
        bool: True if all directories exist or were created successfully.
    
    Raises:
        OSError: If any directory cannot be created or accessed.
    """
    required_dirs = [BLOCKS_DIR, INDEX_DIR, LOGS_DIR, SOURCE_CONCEPTS_DIR]
    
    for dir_path in required_dirs:
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Error: Could not create directory {dir_path}: {e}")
            raise
    
    print(f"All required directories ready: {len(required_dirs)} confirmed")
    return True
