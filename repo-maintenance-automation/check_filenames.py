#!/usr/bin/env python3
"""
File: check_filenames.py
Tool: CADMIES Filename Convention Checker
Version: 1.2.0
System: CADMIES / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Checks that all polished phase notes and raw session notes
         follow the filename convention from the Note-Taking Protocol.

         Phase notes: Phase-XX-Description.md or Phase-XX — Description.md
         Session notes: Session-XXX — YYYY-MM-DD — Description.md

Usage:
    python repo-maintenance-automation/check_filenames.py

Version History:
  v1.0.0 (2026-07-28): Initial release with title matching.
  v1.1.0 (2026-07-28): Relaxed title matching.
  v1.2.0 (2026-07-28): Filename-only check, no title matching.
"""

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = (SCRIPT_DIR / "../CADMIES-IPLD/Scientific Obsidian").resolve()

# Phase-XX-Description.md or Phase-XXx-Description.md or Phase-XX — Description.md
PHASE_PATTERN = re.compile(r"^Phase-\d+[A-Za-z]?-.+\.md$")

# Session-XXX — YYYY-MM-DD — Description.md
SESSION_PATTERN = re.compile(r"^Session-\d+[A-Za-z]? — \d{4}-\d{2}-\d{2} — .+\.md$")

# Old format: Session-XXX — Description.md (missing date)
OLD_SESSION_PATTERN = re.compile(r"^Session-\d+[A-Za-z]? — .+\.md$")


def check_folder(folder, pattern, old_pattern, label):
    issues = []
    if not folder.exists():
        return issues
    
    for filepath in sorted(folder.glob("*.md")):
        filename = filepath.name
        if filename.startswith("."):
            continue
        if filename == "Decisions-Log.md":
            continue  # Not a phase note
        
        if not pattern.match(filename):
            if old_pattern and old_pattern.match(filename):
                issues.append(f"MISSING_DATE: {filename}")
            else:
                issues.append(f"NONSTANDARD: {filename}")
    
    return issues


def main():
    phase_folder = VAULT_ROOT / "Polished-CADMIES/03-Development"
    session_folder = VAULT_ROOT / "Raw-CADMIES/Session-Notes"
    
    phase_issues = check_folder(phase_folder, PHASE_PATTERN, None, "Phase")
    session_issues = check_folder(session_folder, SESSION_PATTERN, OLD_SESSION_PATTERN, "Session")
    
    print(f"\n{'='*60}")
    print(f"  📄 FILENAME CONVENTION CHECK")
    print(f"{'='*60}\n")
    
    print("── Polished Phase Notes ──")
    if phase_issues:
        for i in phase_issues:
            print(f"  ⚠️  {i}")
    else:
        print(f"  ✅ All phase filenames follow convention")
    
    print(f"\n── Raw Session Notes ──")
    if session_issues:
        for i in session_issues:
            print(f"  ⚠️  {i}")
    else:
        print(f"  ✅ All session filenames follow convention")
    
    total = len(phase_issues) + len(session_issues)
    print(f"\n{'='*60}")
    print(f"  📊 {total} issues found")
    if total == 0:
        print(f"  ✅ All filenames uniform.")
    print(f"{'='*60}\n")
    
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
