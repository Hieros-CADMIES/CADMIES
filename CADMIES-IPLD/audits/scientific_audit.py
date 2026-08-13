#!/usr/bin/env python3
---
System: CADMIES / audits
Document_ID: CA-2026-046-AUDIT
Version: 1.1.0
Classification: INTERNAL
Author: The Gardener
Reviewers: [The Gardener, DeepSeek]
Status: ACTIVE
Created: 2026-08-12
Modified: 2026-08-12
Related_Docs: [cid_generator.py, paths.py]
---
"""
File: scientific_audit.py
Tool: CADMIES Scientific Audit
Version: 1.1.0
System: CADMIES / audits
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Comprehensive verification of system rigor and standards
         across the CADMIES ecosystem.

Usage:
    python audits/scientific_audit.py

Version History:
    v1.1.0 (2026-08-12): Added scientific documentation YAML metadata block.
        Added VERSION constant for dynamic version display.
        Fixed CID Generator import path (tools.core, not tools).
        Terminal emojis retained for report formatting.
    v1.0.0: Initial release. Four-part scientific audit.
"""

import os
import sys
import json
import random
import subprocess
from pathlib import Path
from datetime import datetime, timezone

VERSION = "1.1.0"

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "core"))

from paths import PROJECT_ROOT

class ScientificAudit:
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.issues = []
        self.warnings = []
        self.successes = []
    
    def log_issue(self, category, message):
        self.issues.append(f"[{category}] {message}")
        print(f"ISSUE: {message}")
    
    def log_warning(self, category, message):
        self.warnings.append(f"[{category}] {message}")
        print(f"WARNING: {message}")
    
    def log_success(self, category, message):
        self.successes.append(f"[{category}] {message}")
        print(f"OK: {message}")
    
    def audit_structure(self):
        """Audit 1: Directory Structure"""
        print("\n" + "="*60)
        print("AUDIT 1: DIRECTORY STRUCTURE AND ORGANIZATION")
        print("="*60)
        
        required_dirs = ['tools', 'docs', 'store']
        for dir_name in required_dirs:
            if (self.project_root / dir_name).exists():
                self.log_success("Structure", f"Directory exists: {dir_name}/")
            else:
                self.log_issue("Structure", f"Missing directory: {dir_name}/")
        
        store = self.project_root / 'store'
        if store.exists():
            subdirs = ['blocks', 'index', 'logs']
            for subdir in subdirs:
                if (store / subdir).exists():
                    self.log_success("Store", f"Store subdirectory: {subdir}/")
                else:
                    self.log_warning("Store", f"Missing store subdirectory: {subdir}/")
    
    def audit_metadata(self):
        """Audit 2: Scientific Metadata"""
        print("\n" + "="*60)
        print("AUDIT 2: SCIENTIFIC METADATA AND DOCUMENTATION")
        print("="*60)
        
        tools_dir = self.project_root / 'tools'
        if tools_dir.exists():
            for py_file in tools_dir.glob("*.py"):
                content = py_file.read_text()
                
                checks = [
                    ("Version History", "Version history"),
                    ("System:", "System metadata"),
                    ("Status", "Status metadata"),
                ]
                
                all_present = True
                for field, desc in checks:
                    if field not in content:
                        self.log_warning("Metadata", f"{py_file.name} missing {desc}")
                        all_present = False
                
                if all_present:
                    self.log_success("Metadata", f"{py_file.name} has complete metadata")
        
        core_dir = self.project_root / 'tools' / 'core'
        if core_dir.exists():
            for py_file in core_dir.glob("*.py"):
                content = py_file.read_text()
                
                checks = [
                    ("Version History", "Version history"),
                    ("System:", "System metadata"),
                    ("Status", "Status metadata"),
                ]
                
                all_present = True
                for field, desc in checks:
                    if field not in content:
                        self.log_warning("Metadata", f"{py_file.name} missing {desc}")
                        all_present = False
                
                if all_present:
                    self.log_success("Metadata", f"{py_file.name} has complete metadata")
    
    def audit_functionality(self):
        """Audit 3: Functional Verification"""
        print("\n" + "="*60)
        print("AUDIT 3: FUNCTIONAL VERIFICATION")
        print("="*60)
        
        try:
            from cid_generator import CIDGenerator
            gen = CIDGenerator()
            
            test_data = {'test': 'reproducible'}
            result1 = gen.generate_cid(test_data)
            result2 = gen.generate_cid(test_data)
            
            if result1.get('cid') == result2.get('cid'):
                self.log_success("Functionality", "CID Generator: Deterministic (reproducible)")
            else:
                self.log_issue("Functionality", "CID Generator: Non-deterministic!")
            
            data1 = {'test': 'data1'}
            data2 = {'test': 'data2'}
            cid1 = gen.generate_cid(data1)
            cid2 = gen.generate_cid(data2)
            
            if cid1.get('cid') != cid2.get('cid'):
                self.log_success("Functionality", "CID Generator: Immutable (different content, different CID)")
            else:
                self.log_issue("Functionality", "CID Generator: Not immutable! Same CID for different content")
                
        except Exception as e:
            self.log_issue("Functionality", f"CID Generator test failed: {e}")
        
        index_file = self.project_root / 'store' / 'index' / 'human_id_to_cid.json'
        if index_file.exists():
            try:
                with open(index_file) as f:
                    index = json.load(f)
                
                blocks_dir = self.project_root / 'store' / 'blocks'
                if blocks_dir.exists():
                    blocks = list(blocks_dir.glob("*.cbor"))
                    
                    index_count = len(index)
                    block_count = len(blocks)
                    
                    if index_count <= block_count:
                        self.log_success("Integrity", f"Store consistent: {index_count} index entries, {block_count} blocks")
                    else:
                        self.log_issue("Integrity", f"Store inconsistency: {index_count} index entries > {block_count} blocks")
                        
                    if index:
                        sample_cids = random.sample(list(index.values()), min(3, len(index)))
                        for cid in sample_cids:
                            block_file = blocks_dir / f"{cid}.cbor"
                            if not block_file.exists():
                                block_file = blocks_dir / cid
                            if block_file.exists():
                                self.log_success("Integrity", f"CID {cid[:12]}... has corresponding block")
                            else:
                                self.log_issue("Integrity", f"Missing block for CID: {cid[:12]}...")
                
            except Exception as e:
                self.log_issue("Integrity", f"Store verification failed: {e}")
    
    def audit_standards(self):
        """Audit 4: Code Standards"""
        print("\n" + "="*60)
        print("AUDIT 4: CODE STANDARDS AND BEST PRACTICES")
        print("="*60)
        
        tools_dir = self.project_root / 'tools'
        
        total_py = len(list(tools_dir.glob("*.py"))) if tools_dir.exists() else 0
        total_core = len(list((self.project_root / 'tools' / 'core').glob("*.py"))) if (self.project_root / 'tools' / 'core').exists() else 0
        total_py += total_core
        
        with_docstrings = 0
        with_type_hints = 0
        with_error_handling = 0
        
        for directory in [tools_dir, self.project_root / 'tools' / 'core']:
            if not directory.exists():
                continue
            for py_file in directory.glob("*.py"):
                content = py_file.read_text()
                
                if '"""' in content or "'''" in content:
                    with_docstrings += 1
                
                if 'from typing' in content or 'import typing' in content:
                    with_type_hints += 1
                
                if 'try:' in content and 'except' in content:
                    with_error_handling += 1
        
        if total_py > 0:
            self.log_success("Standards", f"Total Python files: {total_py}")
            
            doc_percent = (with_docstrings / total_py) * 100
            if doc_percent > 80:
                self.log_success("Standards", f"Documentation: {with_docstrings}/{total_py} files ({doc_percent:.0f}%)")
            elif doc_percent > 50:
                self.log_warning("Standards", f"Documentation: {with_docstrings}/{total_py} files ({doc_percent:.0f}%) - could improve")
            else:
                self.log_issue("Standards", f"Documentation: {with_docstrings}/{total_py} files ({doc_percent:.0f}%) - needs work")
            
            type_percent = (with_type_hints / total_py) * 100
            if type_percent > 50:
                self.log_success("Standards", f"Type hints: {with_type_hints}/{total_py} files ({type_percent:.0f}%)")
            else:
                self.log_warning("Standards", f"Type hints: {with_type_hints}/{total_py} files ({type_percent:.0f}%) - consider adding more")
            
            error_percent = (with_error_handling / total_py) * 100
            if error_percent > 60:
                self.log_success("Standards", f"Error handling: {with_error_handling}/{total_py} files ({error_percent:.0f}%)")
            else:
                self.log_warning("Standards", f"Error handling: {with_error_handling}/{total_py} files ({error_percent:.0f}%) - could improve robustness")
    
    def generate_report(self):
        """Generate final audit report"""
        print("\n" + "="*60)
        print("FINAL AUDIT REPORT")
        print("="*60)
        
        total_checks = len(self.successes) + len(self.warnings) + len(self.issues)
        score = (len(self.successes) / total_checks) * 100 if total_checks > 0 else 0
        
        print(f"\nSUMMARY:")
        print(f"   Successes: {len(self.successes)}")
        print(f"   Warnings: {len(self.warnings)}")
        print(f"   Issues: {len(self.issues)}")
        print(f"   Score: {score:.1f}%")
        
        print(f"\nSYSTEM STATUS: ", end="")
        if score >= 90:
            print("EXCELLENT - Scientifically rigorous")
        elif score >= 75:
            print("GOOD - Meets most standards")
        elif score >= 60:
            print("FAIR - Needs some improvements")
        else:
            print("NEEDS WORK - Significant improvements needed")
        
        if self.issues:
            print(f"\nCRITICAL ISSUES NEEDING ATTENTION:")
            for issue in self.issues:
                print(f"   - {issue}")
        
        if self.warnings:
            print(f"\nRECOMMENDED IMPROVEMENTS:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        print(f"\nMYCELIAL NETWORK ASSESSMENT:")
        if score >= 80:
            print("   The knowledge garden is thriving with scientific rigor!")
        elif score >= 60:
            print("   The mycelial network is growing but needs nourishment.")
        else:
            print("   The garden needs tending to reach full potential.")
        
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": "CADMIES IPLD Content-Addressed Knowledge System",
            "audit_version": VERSION,
            "score": score,
            "successes": len(self.successes),
            "warnings": len(self.warnings),
            "issues": len(self.issues),
            "details": {
                "successes": self.successes,
                "warnings": self.warnings,
                "issues": self.issues
            }
        }
        
        report_file = self.project_root / "scientific_audit_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nFull report saved to: {report_file}")
    
    def run_full_audit(self):
        """Run all audits"""
        print("CADMIES IPLD SYSTEM - SCIENTIFIC AUDIT")
        print("Verifying mycelial network integrity...")
        
        self.audit_structure()
        self.audit_metadata()
        self.audit_functionality()
        self.audit_standards()
        self.generate_report()

if __name__ == "__main__":
    auditor = ScientificAudit()
    auditor.run_full_audit()
