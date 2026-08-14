#!/usr/bin/env python3
"""
File: provenance_manager.py
Tool: CADMIES Provenance Manager
Version: 1.1.0
System: CADMIES / tools/core
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Create and query provenance records (timestamps, authorship, verification).
         Air-gapped compatible. No network required.

Usage:
    from provenance_manager import ProvenanceManager

Dependencies: dag_cbor, multiformats

Version History:
    v1.1.0 (2026-08-12): Added scientific documentation YAML metadata block.
        Removed store_path parameter for path consistency with paths.py.
        Standardized block file naming to .cbor extension.
        Removed unused imports.
    v1.0.0: Initial release. Creation and query of provenance records.
"""

import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

import dag_cbor
from multiformats import multihash, CID

from paths import BLOCKS_DIR, ensure_dirs

class ProvenanceManager:
    def __init__(self):
        ensure_dirs()
        self.blocks_path = BLOCKS_DIR
        
    def create_provenance_record(self, concept_cid: str, author: str, record_type: str, **kwargs) -> Dict[str, Any]:
        """Create a provenance record and store it as an IPLD block"""
        
        record = {
            "concept_cid": concept_cid,
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "author": author,
            "record_type": record_type,
            **kwargs
        }
        
        cbor_bytes = dag_cbor.encode(record)
        digest = hashlib.sha256(cbor_bytes).digest()
        mh = multihash.wrap(digest, 'sha2-256')
        cid = CID('base32', 1, 'dag-cbor', mh)
        
        block_path = self.blocks_path / f"{cid}.cbor"
        with open(block_path, 'wb') as f:
            f.write(cbor_bytes)
        
        return {
            "provenance_cid": str(cid),
            "record": record,
            "stored": True
        }
    
    def query_provenance(self, concept_cid: str) -> List[Dict[str, Any]]:
        """Find all provenance records referencing a concept CID"""
        results = []
        
        for block_file in self.blocks_path.glob("bafy*.cbor"):
            with open(block_file, 'rb') as f:
                cbor_bytes = f.read()
            
            try:
                record = dag_cbor.decode(cbor_bytes)
                if isinstance(record, dict) and record.get("concept_cid") == concept_cid:
                    results.append(record)
            except (ValueError, KeyError, TypeError):
                continue
        
        results.sort(key=lambda x: x.get("timestamp", ""))
        return results
    
    def get_origin(self, concept_cid: str) -> Optional[Dict[str, Any]]:
        """Get the creation record (oldest provenance) for a concept"""
        records = self.query_provenance(concept_cid)
        for record in records:
            if record.get("record_type") == "creation":
                return record
        return None

if __name__ == "__main__":
    pm = ProvenanceManager()
    print("Provenance Manager initialized")
    print(f"Store path: {pm.blocks_path}")
    print(f"Blocks: {len(list(pm.blocks_path.glob('bafy*.cbor')))}")
