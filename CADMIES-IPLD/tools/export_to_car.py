#!/usr/bin/env python3
"""
File: export_to_car.py
Tool: CADMIES CAR Export
Version: 1.1.0
System: CADMIES / tools
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Export CADMIES concepts (with provenance) to CAR files for sharing.
         Content-addressed, verifiable, portable.

Usage:
    python tools/export_to_car.py <human_id_or_cid> --output <file.car>
    python tools/export_to_car.py --concepts id1,id2,id3 --output bundle.car
    python tools/export_to_car.py --all --output full_mycelium.car

Version History:
  v1.1.0 (2026-08-12): Added scientific documentation YAML metadata block.
      Switched to paths.py for BLOCKS_DIR and INDEX_FILE.
      Made version display dynamic via VERSION constant.
      Removed emojis from output for scientific rigor compliance.
  v1.0.0: Initial release. Multi-concept export with provenance collection.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Optional, Union, List, Set

# Add tools directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from core.car_utils import (
    write_car,
    load_block_from_store,
    calculate_cid
)
from core.paths import BLOCKS_DIR, INDEX_FILE

VERSION = "1.1.0"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_index() -> Dict[str, str]:
    """Load human_id to CID mapping from index."""
    if not INDEX_FILE.exists():
        return {}
    with open(INDEX_FILE, 'r') as f:
        return json.load(f)


def is_cid(value: str) -> bool:
    """Check if string looks like a CID (starts with bafy or Qm)."""
    return value.startswith('bafy') or value.startswith('Qm')


def ensure_bytes(value: Union[str, bytes]) -> bytes:
    """Convert string to bytes if needed."""
    if isinstance(value, str):
        return value.encode('utf-8')
    return value


def resolve_identifier(identifier: str, index: Dict[str, str]) -> Optional[str]:
    """
    Auto-detect if identifier is CID or human_id.
    Returns CID string or None if not found.
    """
    if is_cid(identifier):
        block_path = BLOCKS_DIR / f"{identifier}.cbor"
        if block_path.exists():
            return identifier
        else:
            print(f"ERROR: CID not found in blockstore: {identifier}")
            return None
    else:
        cid = index.get(identifier)
        if cid:
            return cid
        else:
            print(f"ERROR: Human ID not found in index: {identifier}")
            return None


def get_provenance_blocks(concept_cid: str) -> Dict[str, bytes]:
    """
    Find all provenance blocks that reference this concept.
    Returns dict of {cid: block_bytes}
    """
    provenance_blocks = {}
    
    for block_path in BLOCKS_DIR.glob("*.cbor"):
        cid = block_path.stem
        
        if cid == concept_cid:
            continue
        
        block_data = load_block_from_store(cid, BLOCKS_DIR)
        if not block_data:
            continue
        
        try:
            import dag_cbor
            decoded = dag_cbor.decode(block_data)
            
            if (decoded.get('record_type') in ['creation', 'verification', 'supersession', 'comment'] 
                and decoded.get('concept_cid') == concept_cid):
                provenance_blocks[cid] = block_data
        except:
            pass
    
    return provenance_blocks


def collect_concept_blocks(identifiers: List[str], index: Dict[str, str], include_provenance: bool = True) -> tuple:
    """
    Collect all blocks for given identifiers.
    Returns (blocks_dict, concept_cids_list, human_id_map)
    """
    blocks = {}
    concept_cids = []
    human_id_map = {}
    
    for identifier in identifiers:
        cid = resolve_identifier(identifier, index)
        if not cid:
            print(f"WARNING: Skipping invalid identifier: {identifier}")
            continue
        
        concept_cids.append(cid)
        
        concept_block = load_block_from_store(cid, BLOCKS_DIR)
        if not concept_block:
            print(f"WARNING: Concept block not found for {identifier} ({cid})")
            continue
        
        blocks[cid] = concept_block
        print(f"   Block: {identifier} -> {cid[:16]}... ({len(concept_block)} bytes)")
        
        human_id_map[identifier] = cid
        
        if include_provenance:
            provenance = get_provenance_blocks(cid)
            blocks.update(provenance)
            if provenance:
                print(f"      +{len(provenance)} provenance block(s)")
    
    return blocks, concept_cids, human_id_map


def export_concepts(identifiers: List[str], output_path: Path, include_provenance: bool = True) -> bool:
    """
    Export multiple concepts to a CAR file.
    """
    print("=" * 60)
    print(f"CADMIES Export to CAR v{VERSION}")
    print("=" * 60)
    
    index = load_index()
    
    print(f"\nCollecting {len(identifiers)} concept(s)...")
    blocks, concept_cids, human_id_map = collect_concept_blocks(identifiers, index, include_provenance)
    
    if not blocks:
        print("ERROR: No valid concepts found to export")
        return False
    
    print(f"\nCollected {len(blocks)} total block(s)")
    print(f"   Concept blocks: {len(concept_cids)}")
    print(f"   Total unique CIDs: {len(set(blocks.keys()))}")
    
    index_bytes = json.dumps(human_id_map, indent=2).encode('utf-8')
    index_cid = calculate_cid(index_bytes)
    blocks[index_cid] = index_bytes
    print(f"Added consolidated index block with {len(human_id_map)} mapping(s)")
    
    try:
        blocks_for_car = {}
        for cid_str, block_data in blocks.items():
            cid_bytes = ensure_bytes(cid_str)
            blocks_for_car[cid_bytes] = block_data
        
        roots = [ensure_bytes(cid) for cid in concept_cids]
        
        write_car(blocks_for_car, roots, output_path)
        
        print(f"\nSuccessfully exported to: {output_path}")
        print(f"   Total blocks: {len(blocks)}")
        print(f"   Root concepts: {len(concept_cids)}")
        print(f"   File size: {output_path.stat().st_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: Failed to write CAR file: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_all_concept_cids(index: Dict[str, str]) -> List[str]:
    """Get all unique concept CIDs from the index."""
    return list(set(index.values()))


def get_all_human_ids(index: Dict[str, str]) -> List[str]:
    """Get all human_ids from the index."""
    return list(index.keys())


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description=f"Export CADMIES concepts to CAR file v{VERSION}",
        epilog="""
Examples:
  export_to_car.py natural_selection --output single.car
  export_to_car.py --concepts natural_selection,entropy,occams_razor --output bundle.car
  export_to_car.py --concepts-file my_list.txt --output bundle.car
  export_to_car.py --all --output full_mycelium.car
  export_to_car.py --cids bafy...,bafy... --output bundle.car
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        'identifier',
        nargs='?',
        help='Single CID or human_id'
    )
    input_group.add_argument(
        '--concepts', '-c',
        help='Comma-separated list of human_ids'
    )
    input_group.add_argument(
        '--concepts-file', '-f',
        help='File containing one human_id per line'
    )
    input_group.add_argument(
        '--cids',
        help='Comma-separated list of CIDs'
    )
    input_group.add_argument(
        '--all', '-a',
        action='store_true',
        help='Export all concepts in the mycelium'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output CAR file path'
    )
    
    parser.add_argument(
        '--no-provenance',
        action='store_true',
        help='Exclude provenance blocks'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    
    args = parser.parse_args()
    
    identifiers = []
    
    if args.identifier:
        identifiers = [args.identifier]
    elif args.concepts:
        identifiers = [h.strip() for h in args.concepts.split(',') if h.strip()]
    elif args.concepts_file:
        path = Path(args.concepts_file)
        if not path.exists():
            print(f"ERROR: File not found: {path}")
            sys.exit(1)
        with open(path, 'r') as f:
            identifiers = [line.strip() for line in f if line.strip()]
    elif args.cids:
        identifiers = [c.strip() for c in args.cids.split(',') if c.strip()]
    elif args.all:
        index = load_index()
        identifiers = get_all_human_ids(index)
        print(f"Exporting all {len(identifiers)} concepts from mycelium")
    
    if not identifiers:
        print("ERROR: No identifiers provided")
        sys.exit(1)
    
    print(f"Exporting {len(identifiers)} concept(s)")
    if args.verbose:
        for i, id in enumerate(identifiers[:10]):
            print(f"   {i+1}. {id}")
        if len(identifiers) > 10:
            print(f"   ... and {len(identifiers) - 10} more")
    
    success = export_concepts(
        identifiers=identifiers,
        output_path=Path(args.output),
        include_provenance=not args.no_provenance
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
