#!/usr/bin/env python3
"""
File: orcid_device_flow.py
Tool: CADMIES ORCID Device Flow
Version: 1.1.0
System: CADMIES / tools/core
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: OAuth device flow for ORCID owner-verified concept stamping.
         Reads credentials from .env file.

Usage:
    python tools/core/orcid_device_flow.py <concept_cid>

Version History:
    v1.1.0 (2026-08-12): Added scientific documentation YAML metadata block.
        Fixed hardcoded .env path to use PROJECT_ROOT from paths.py.
        Terminal emojis retained for user experience.
    v1.0.0: Initial release. ORCID OAuth device flow.
"""

import os
import sys
import time
import requests
import webbrowser
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))
from paths import PROJECT_ROOT
from verification_manager import add_verification_statement

VERSION = "1.1.0"

# Load .env from CADMIES root
env_path = PROJECT_ROOT.parent / ".env"
if not env_path.exists():
    env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
                elif ':' in line:
                    key, value = line.split(':', 1)
                    os.environ[key] = value

CLIENT_ID = os.environ.get("ORCID_CLIENT_ID")
CLIENT_SECRET = os.environ.get("ORCID_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: ORCID_CLIENT_ID and ORCID_CLIENT_SECRET must be in .env")
    print(f"Looking for .env at: {env_path}")
    sys.exit(1)

# ORCID API endpoints
ORCID_DEVICE_AUTH_URL = "https://orcid.org/oauth/device_authorization"
ORCID_TOKEN_URL = "https://orcid.org/oauth/token"
ORCID_API_URL = "https://pub.orcid.org/v3.0"

def device_authorization():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "client_id": CLIENT_ID,
        "scope": "/authenticate"
    }
    resp = requests.get(ORCID_DEVICE_AUTH_URL, params=data, headers=headers)
    if resp.status_code != 200:
        print(f"Error: {resp.status_code}")
        print(f"Response: {resp.text}")
        return None
    return resp.json()

def poll_for_token(device_code, interval, verification_url, user_code):
    print(f"\nGo to: {verification_url}")
    print(f"Enter code: {user_code}")
    webbrowser.open(verification_url)
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
    }
    
    while True:
        time.sleep(interval)
        resp = requests.post(ORCID_TOKEN_URL, data=data, headers=headers)
        if resp.status_code == 200:
            return resp.json().get("access_token")
        
        try:
            result = resp.json()
        except:
            print(f"\nInvalid response: {resp.text}")
            return None
            
        err = result.get("error")
        if err == "authorization_pending":
            print(".", end="", flush=True)
        elif err == "expired_token":
            print("\nAuthorization code expired. Try again.")
            return None
        else:
            print(f"\n{err}: {result.get('error_description', 'Unknown error')}")
            return None

def fetch_orcid_profile(token):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    resp = requests.get(f"{ORCID_API_URL}/record", headers=headers)
    if resp.status_code != 200:
        print(f"Error fetching profile: {resp.status_code}")
        return None, None
    
    data = resp.json()
    orcid_id = data.get("orcid-identifier", {}).get("path")
    
    name = orcid_id
    person_resp = requests.get(f"{ORCID_API_URL}/{orcid_id}/person", headers=headers)
    if person_resp.status_code == 200:
        person_data = person_resp.json()
        given = person_data.get("name", {}).get("given-names", {}).get("value", "")
        family = person_data.get("name", {}).get("family-name", {}).get("value", "")
        if given or family:
            name = f"{given} {family}".strip()
    
    return orcid_id, name

def stamp_with_orcid_device_flow(concept_cid):
    print("=== ORCID Device Flow ===\n")
    
    device_data = device_authorization()
    if not device_data:
        return None
    
    device_code = device_data["device_code"]
    user_code = device_data["user_code"]
    verification_url = device_data["verification_uri"]
    interval = device_data.get("interval", 5)
    
    access_token = poll_for_token(device_code, interval, verification_url, user_code)
    if not access_token:
        return None
    
    print("\nAuthorized!")
    
    orcid_id, name = fetch_orcid_profile(access_token)
    if not orcid_id:
        return None
    
    print(f"Verified: {name} ({orcid_id})")
    
    metadata = {
        "orcid_id": orcid_id,
        "orcid_name": name,
        "verification_method": "oauth_device_flow",
        "authenticated": True,
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }
    
    provenance_cid = add_verification_statement(
        verifier_key=f"orcid-oauth-{orcid_id}",
        concept_cid=concept_cid,
        statement_type="endorses",
        source="orcid",
        metadata=metadata
    )
    
    print(f"\nVerification block created: {provenance_cid}")
    print(f"   Badge will show GREEN (owner-verified)")
    
    return provenance_cid

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=f"ORCID OAuth verification v{VERSION} (device flow)")
    parser.add_argument("concept_cid", help="CID of concept to verify")
    args = parser.parse_args()
    
    stamp_with_orcid_device_flow(args.concept_cid)
