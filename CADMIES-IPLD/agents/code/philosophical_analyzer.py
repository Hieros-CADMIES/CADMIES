#!/usr/bin/env python3
---
System: CADMIES / agents/code
Document_ID: CA-2026-035-AGENT
Version: 1.1.0
Classification: INTERNAL
Author: The Gardener
Reviewers: [The Gardener, DeepSeek]
Status: ACTIVE
Created: 2026-08-12
Modified: 2026-08-12
Related_Docs: [paths.py, cadmies_concept_reader.py]
---
"""
File: philosophical_analyzer.py
Agent: Philosophical Analyzer
Author: CADMIES Research Group
Created: 2025-12-29
Version: 1.1.0
System: CADMIES / agents/code
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Analyze philosophical concepts for patterns and connections.
         Air-gapped. No external dependencies beyond dag_cbor.

Usage:
    python philosophical_analyzer.py --test
    python philosophical_analyzer.py --cids CID1 CID2 CID3 --depth detailed

Signature: analyze_philosophical_patterns(concept_cids: list, context: dict) -> dict

Version History:
    v1.1.0 (2026-08-12): Added scientific documentation YAML metadata block.
        Switched to paths.py for PROJECT_ROOT and BLOCKSTORE_PATH.
        Made version display dynamic via VERSION constant.
    v1.0.0: Initial release. Pattern analysis with three depth levels.
"""

import json
import re
import time
import sys
import base64
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add tools/core to path for paths.py import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools" / "core"))

from paths import PROJECT_ROOT, BLOCKS_DIR

VERSION = "1.1.0"

BLOCKSTORE_PATH = BLOCKS_DIR

# Try importing dag_cbor for block reading
try:
    import dag_cbor
    DAG_CBOR_AVAILABLE = True
except ImportError:
    DAG_CBOR_AVAILABLE = False
    print("WARNING: dag_cbor not available - using JSON fallback")


def load_concept(cid: str, blockstore_path: Path = None) -> Dict[str, Any]:
    """
    Load a concept by CID from blockstore.
    
    Args:
        cid: Content Identifier of the concept
        blockstore_path: Optional path to blockstore (default: auto-detected)
        
    Returns:
        Dict containing concept data
        
    Raises:
        FileNotFoundError: If concept block doesn't exist
        ValueError: If CID format is invalid
    """
    if not cid.startswith('bafy'):
        raise ValueError(f"Invalid CID format: {cid}")
    
    if blockstore_path is None:
        blockstore_path = BLOCKSTORE_PATH
    
    cbor_file = blockstore_path / f"{cid}.cbor"
    if not cbor_file.exists():
        cbor_file = blockstore_path / cid
    
    if not cbor_file.exists():
        raise FileNotFoundError(f"Concept block not found: {cid} at {cbor_file}")
    
    with open(cbor_file, 'rb') as f:
        raw_data = f.read()
    
    if DAG_CBOR_AVAILABLE:
        try:
            return dag_cbor.decode(raw_data)
        except Exception as e:
            print(f"WARNING: DAG-CBOR decode failed for {cid}: {e}")
    
    try:
        return json.loads(raw_data.decode('utf-8'))
    except Exception as e:
        print(f"ERROR: Failed to decode {cid}: {e}")
        return {
            'error': str(e), 
            'cid': cid, 
            '_raw': base64.b64encode(raw_data[:100]).decode('utf-8')
        }


def extract_key_terms(text: str, min_length: int = 4) -> List[str]:
    """
    Extract meaningful terms from text.
    """
    if not text:
        return []
    
    text_lower = text.lower()
    
    stop_words = {'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'has', 
                  'was', 'were', 'are', 'is', 'be', 'been', 'being', 'does', 'do'}
    
    words = re.findall(r'\b[a-z][a-z-]{2,}\b', text_lower)
    
    filtered_words = []
    for word in words:
        clean_word = word.replace('-', '')
        if clean_word not in stop_words and len(clean_word) >= min_length:
            filtered_words.append(word)
    
    return filtered_words


def find_semantic_connections(concept1: Dict, concept2: Dict) -> List[Dict]:
    """
    Find semantic connections between two concepts.
    """
    connections = []
    
    domain1 = concept1.get('domain')
    domain2 = concept2.get('domain')
    if domain1 and domain1 == domain2:
        connections.append({
            'type': 'shared_domain',
            'description': f"Both concepts belong to domain: {domain1}",
            'confidence': 0.8,
            'evidence': [domain1]
        })
    
    type1 = concept1.get('type')
    type2 = concept2.get('type')
    if type1 and type1 == type2:
        connections.append({
            'type': 'shared_type',
            'description': f"Both are {type1} concepts",
            'confidence': 0.7,
            'evidence': [type1]
        })
    
    subdomain1 = concept1.get('subdomain')
    subdomain2 = concept2.get('subdomain')
    if subdomain1 and subdomain1 == subdomain2:
        connections.append({
            'type': 'shared_subdomain',
            'description': f"Both focus on subdomain: {subdomain1}",
            'confidence': 0.9,
            'evidence': [subdomain1]
        })
    
    text1 = f"{concept1.get('title', '')} {concept1.get('definition', '')}"
    text2 = f"{concept2.get('title', '')} {concept2.get('definition', '')}"
    
    terms1 = set(extract_key_terms(text1))
    terms2 = set(extract_key_terms(text2))
    
    shared_terms = terms1.intersection(terms2)
    if shared_terms:
        connections.append({
            'type': 'shared_terminology',
            'description': f"Share {len(shared_terms)} key terms",
            'confidence': min(0.3 + (len(shared_terms) * 0.1), 0.9),
            'evidence': list(sorted(shared_terms))[:5]
        })
    
    return connections


def analyze_philosophical_patterns(concept_cids: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Analyze philosophical concepts for patterns and connections.
    
    Args:
        concept_cids: List of CIDs for philosophical concepts to analyze
        context: Optional execution context with metadata
        
    Returns:
        Dict with analysis results
    """
    start_time = time.time()
    
    if context is None:
        context = {}
    
    focus_area = context.get('focus_area', 'general')
    analysis_depth = context.get('analysis_depth', 'basic')
    
    print("PHILOSOPHICAL ANALYSIS STARTED")
    print(f"   Concepts: {len(concept_cids)}")
    print(f"   Focus: {focus_area}")
    print(f"   Depth: {analysis_depth}")
    
    concepts = []
    load_errors = []
    
    for cid in concept_cids:
        try:
            concept_data = load_concept(cid, BLOCKSTORE_PATH)
            concepts.append({
                'cid': cid,
                'data': concept_data,
                'title': concept_data.get('title', 'Unknown'),
                'type': concept_data.get('type', 'Unknown'),
                'domain': concept_data.get('domain', 'Unknown'),
                'subdomain': concept_data.get('subdomain', ''),
                'definition': concept_data.get('definition', ''),
                'human_id': concept_data.get('human_id', '')
            })
            title = concept_data.get('title', cid[:16])
            print(f"   LOADED: {title}...")
        except Exception as e:
            error_msg = f"Failed to load {cid}: {e}"
            print(f"   ERROR: {error_msg}")
            load_errors.append(error_msg)
    
    if not concepts:
        return {
            'success': False,
            'error': 'No concepts could be loaded',
            'load_errors': load_errors,
            'metadata': {
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'concepts_requested': len(concept_cids),
                'concepts_loaded': 0
            }
        }
    
    print(f"SUCCESS: Loaded {len(concepts)}/{len(concept_cids)} concepts")
    
    results = {
        'success': True,
        'concepts_analyzed': len(concepts),
        'patterns_found': [],
        'connections': [],
        'insights': [],
        'recommendations': [],
        'metadata': {
            'analyzer_version': VERSION,
            'analysis_timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'execution_time_seconds': 0,
            'focus_area': focus_area,
            'analysis_depth': analysis_depth,
            'load_errors': load_errors if load_errors else None
        }
    }
    
    # BASIC ANALYSIS (always performed)
    
    domains = Counter([c['domain'] for c in concepts if c['domain']])
    if domains:
        results['domain_distribution'] = dict(domains)
        if len(domains) == 1:
            results['insights'].append({
                'type': 'domain_focus',
                'description': f"All concepts focus on {list(domains.keys())[0]}",
                'confidence': 0.9
            })
    
    types = Counter([c['type'] for c in concepts if c['type']])
    if types:
        results['type_distribution'] = dict(types)
    
    all_text = ' '.join([f"{c.get('title', '')} {c.get('definition', '')}" for c in concepts])
    key_terms = extract_key_terms(all_text)
    term_freq = Counter(key_terms)
    
    if term_freq:
        top_terms = dict(term_freq.most_common(10))
        results['common_terminology'] = top_terms
        
        philosophical_terms = {'reality', 'consciousness', 'existence', 'knowledge', 
                              'truth', 'being', 'mind', 'nature', 'universe', 'theory'}
        found_terms = philosophical_terms.intersection(set(top_terms.keys()))
        if found_terms:
            results['insights'].append({
                'type': 'core_philosophical_terms',
                'description': f"Found core philosophical terms: {', '.join(sorted(found_terms))}",
                'confidence': 0.8
            })
    
    # DETAILED ANALYSIS (if requested)
    if analysis_depth in ['detailed', 'comprehensive']:
        all_connections = []
        
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                conns = find_semantic_connections(concepts[i], concepts[j])
                for conn in conns:
                    connection_record = {
                        'source_cid': concepts[i]['cid'],
                        'source_title': concepts[i]['title'],
                        'target_cid': concepts[j]['cid'],
                        'target_title': concepts[j]['title'],
                        'connection_type': conn['type'],
                        'description': conn['description'],
                        'confidence': conn['confidence'],
                        'evidence': conn.get('evidence', [])
                    }
                    all_connections.append(connection_record)
        
        results['connections'] = all_connections
        
        if all_connections:
            connection_types = Counter([c['connection_type'] for c in all_connections])
            results['connection_analysis'] = {
                'total_connections': len(all_connections),
                'by_type': dict(connection_types),
                'strongest_connections': sorted(all_connections, 
                                               key=lambda x: x['confidence'], 
                                               reverse=True)[:5]
            }
    
    # COMPREHENSIVE ANALYSIS (additional insights)
    if analysis_depth == 'comprehensive' and len(concepts) >= 3:
        domain_groups = defaultdict(list)
        for concept in concepts:
            if concept['domain']:
                domain_groups[concept['domain']].append(concept['title'])
        
        if len(domain_groups) > 1:
            results['insights'].append({
                'type': 'multi_domain_analysis',
                'description': f"Concepts span {len(domain_groups)} different domains",
                'confidence': 0.7,
                'details': {domain: len(titles) for domain, titles in domain_groups.items()}
            })
    
    # Generate recommendations
    if len(concepts) >= 2:
        results['recommendations'].append({
            'type': 'further_exploration',
            'description': f"Explore relationships between '{concepts[0]['title']}' and '{concepts[1]['title']}'",
            'reason': 'These are primary concepts with potential deep connections',
            'priority': 'high'
        })
    
    if len(concepts) > 2:
        results['recommendations'].append({
            'type': 'synthesis_opportunity',
            'description': f"Create synthetic concept combining insights from {len(concepts)} concepts",
            'reason': 'Multiple related concepts suggest synthesis potential',
            'priority': 'medium'
        })
    
    execution_time = time.time() - start_time
    results['metadata']['execution_time_seconds'] = execution_time
    
    print("ANALYSIS COMPLETE")
    print(f"   Patterns found: {len(results.get('patterns_found', []))}")
    print(f"   Connections: {len(results.get('connections', []))}")
    print(f"   Insights: {len(results.get('insights', []))}")
    print(f"   Time: {execution_time:.2f}s")
    
    return results


def test_agent() -> Dict[str, Any]:
    """
    Self-test for the philosophical analyzer.
    Uses any available concepts from the index rather than hardcoded CIDs.
    """
    print("TESTING PHILOSOPHICAL ANALYZER AGENT")
    print("=" * 50)
    
    # Load available CIDs from index dynamically
    from paths import INDEX_FILE
    test_cids = []
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r') as f:
            index = json.load(f)
        test_cids = list(index.values())[:5]
    
    if not test_cids:
        print("No concepts available for testing. Import concepts first.")
        return {'success': False, 'error': 'No concepts in index'}
    
    print(f"Using {len(test_cids)} concepts from index for test")
    
    test_context = {
        "focus_area": "metaphysics",
        "analysis_depth": "detailed",
        "test_mode": True,
        "description": "Testing philosophical analyzer with available concepts"
    }
    
    try:
        results = analyze_philosophical_patterns(test_cids, test_context)
        
        print("\nTEST RESULTS SUMMARY:")
        print(f"   Success: {results.get('success', False)}")
        print(f"   Concepts analyzed: {results.get('concepts_analyzed', 0)}")
        print(f"   Connections found: {len(results.get('connections', []))}")
        print(f"   Insights generated: {len(results.get('insights', []))}")
        
        if results.get('success'):
            print("TEST PASSED - Agent is operational")
        else:
            print("TEST FAILED - Check errors above")
        
        return results
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'metadata': {
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'test_cids': len(test_cids)
            }
        }
        print(f"TEST FAILED WITH EXCEPTION: {e}")
        return error_result


# Command-line interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description=f'Philosophical Analyzer Agent v{VERSION} - Analyze concepts for patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--test', action='store_true', help='Run self-test with available concepts')
    parser.add_argument('--cids', nargs='+', help='List of CIDs to analyze')
    parser.add_argument('--context', type=str, help='JSON context string')
    parser.add_argument('--depth', choices=['basic', 'detailed', 'comprehensive'], 
                       default='basic', help='Analysis depth')
    
    args = parser.parse_args()
    
    if args.test:
        results = test_agent()
        print("\n" + "=" * 50)
        print("TEST COMPLETE")
        
    elif args.cids:
        context = {}
        if args.context:
            try:
                context = json.loads(args.context)
            except json.JSONDecodeError as e:
                print(f"ERROR: Invalid context JSON: {e}")
                exit(1)
        
        context['analysis_depth'] = args.depth
        
        print(f"EXECUTING AGENT WITH {len(args.cids)} CIDs")
        results = analyze_philosophical_patterns(args.cids, context)
        
        print("\n" + "=" * 50)
        print("ANALYSIS SUMMARY")
        print(f"Success: {results.get('success')}")
        print(f"Concepts: {results.get('concepts_analyzed')}")
        if results.get('connections'):
            print(f"Connections found: {len(results['connections'])}")
        if results.get('insights'):
            print(f"Insights: {len(results['insights'])}")
        
        results_dir = PROJECT_ROOT / "analysis_results"
        results_dir.mkdir(exist_ok=True)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        output_file = results_dir / f"analysis_results_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {output_file}")
        
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python philosophical_analyzer.py --test")
        print("  python philosophical_analyzer.py --cids CID1 CID2 CID3 --depth detailed")
