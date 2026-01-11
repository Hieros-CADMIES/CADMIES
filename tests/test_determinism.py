#!/usr/bin/env python3
"""
Test CID Determinism - Critical Verification
Ensures same content always produces same CID
"""

import json
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_same_content_same_cid():
    """Test that identical content produces identical CIDs."""
    print("🧪 Testing CID Determinism...")
    
    # Create identical test concepts
    concept1 = {
        "schema_version": "1.0.0",
        "human_id": "test_determinism",
        "title": "Test Determinism",
        "definition": "Testing that same content produces same CID",
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
    
    concept2 = concept1.copy()  # Exact copy
    
    # Import and use cid_generator
    from cid_generator_v1_1_0 import CIDGenerator_v1_1_0
    generator = CIDGenerator_v1_1_0()
    
    # Generate CIDs
    result1 = generator.generate_cid(concept1)
    result2 = generator.generate_cid(concept2)
    
    # Verify both succeeded
    assert result1["success"], "First generation failed"
    assert result2["success"], "Second generation failed"
    
    # Get CIDs
    cid1 = result1["cid"]
    cid2 = result2["cid"]
    
    print(f"  CID 1: {cid1}")
    print(f"  CID 2: {cid2}")
    
    # Critical assertion
    assert cid1 == cid2, f"CIDs differ: {cid1} != {cid2}"
    
    print("  ✅ Determinism verified: same content → same CID")
    return True

def test_different_content_different_cid():
    """Test that different content produces different CIDs."""
    print("🧪 Testing CID Uniqueness...")
    
    from cid_generator_v1_1_0 import CIDGenerator_v1_1_0
    generator = CIDGenerator_v1_1_0()
    
    # Create two different concepts
    concept1 = {
        "schema_version": "1.0.0",
        "human_id": "test_concept_a",
        "title": "Concept A",
        "definition": "First test concept",
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
    
    concept2 = {
        "schema_version": "1.0.0",
        "human_id": "test_concept_b",  # Different human_id
        "title": "Concept B",          # Different title
        "definition": "Second test concept",
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
    
    # Generate CIDs
    result1 = generator.generate_cid(concept1)
    result2 = generator.generate_cid(concept2)
    
    assert result1["success"] and result2["success"], "Generation failed"
    
    cid1 = result1["cid"]
    cid2 = result2["cid"]
    
    print(f"  CID for Concept A: {cid1}")
    print(f"  CID for Concept B: {cid2}")
    
    # Critical assertion
    assert cid1 != cid2, f"Different content produced same CID: {cid1}"
    
    print("  ✅ Uniqueness verified: different content → different CID")
    return True

def test_whitespace_insensitivity():
    """Test that JSON formatting doesn't affect CID."""
    print("🧪 Testing Whitespace Insensitivity...")
    
    from cid_generator_v1_1_0 import CIDGenerator_v1_1_0
    generator = CIDGenerator_v1_1_0()
    
    # Same content, different formatting
    concept_minified = json.dumps({
        "schema_version": "1.0.0",
        "human_id": "test_whitespace",
        "title": "Test Whitespace",
        "definition": "Testing whitespace insensitivity",
        "type": "Test",
        "domain": "Testing",
        "metadata": {
            "created": "2026-01-07T12:00:00Z",
            "creator": "TestUser",
            "certainty_score": 0.9,
            "version": 1,
            "purpose": "testing"
        }
    }, separators=(',', ':'))  # Minified
    
    concept_pretty = json.dumps({
        "schema_version": "1.0.0",
        "human_id": "test_whitespace",
        "title": "Test Whitespace",
        "definition": "Testing whitespace insensitivity",
        "type": "Test",
        "domain": "Testing",
        "metadata": {
            "created": "2026-01-07T12:00:00Z",
            "creator": "TestUser",
            "certainty_score": 0.9,
            "version": 1,
            "purpose": "testing"
        }
    }, indent=2)  # Pretty printed
    
    # Parse back to dict (normalizes formatting)
    concept1 = json.loads(concept_minified)
    concept2 = json.loads(concept_pretty)
    
    # Generate CIDs
    result1 = generator.generate_cid(concept1)
    result2 = generator.generate_cid(concept2)
    
    assert result1["success"] and result2["success"], "Generation failed"
    
    cid1 = result1["cid"]
    cid2 = result2["cid"]
    
    print(f"  Minified CID: {cid1}")
    print(f"  Pretty CID:   {cid2}")
    
    assert cid1 == cid2, "Whitespace affected CID generation"
    
    print("  ✅ Whitespace insensitivity verified")
    return True

def run_all_determinism_tests():
    """Run all determinism tests."""
    print("=" * 60)
    print("DETERMINISM TEST SUITE")
    print("Critical verification for content-addressed systems")
    print("=" * 60)
    
    tests = [
        ("Same Content → Same CID", test_same_content_same_cid),
        ("Different Content → Different CID", test_different_content_different_cid),
        ("Whitespace Insensitivity", test_whitespace_insensitivity),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n🔬 {test_name}")
            success = test_func()
            results.append((test_name, success, None))
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            results.append((test_name, False, str(e)))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, error in results:
        status = "✅ PASS" if success else f"❌ FAIL: {error}"
        print(f"{test_name:40} {status}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All determinism tests passed!")
        print("System can be trusted for content-addressed knowledge.")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed")
        print("System determinism cannot be guaranteed.")
        return False

if __name__ == "__main__":
    success = run_all_determinism_tests()
    sys.exit(0 if success else 1)