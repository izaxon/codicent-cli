#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '/home/johan/codicent-cli')

from auth import CodicentAuth

def test_auth_flow():
    auth = CodicentAuth()
    
    # Test getting cached token (should be None initially)
    cached = auth.get_cached_token()
    print(f"Cached token: {'Found' if cached else 'None'}")
    
    # Test request preparation (without actually sending)
    print("Auth handler initialized successfully")
    print(f"Base URL: {auth.base_url}")
    print(f"Client ID: {auth.client_id}")
    print(f"Token file location: {auth.token_file}")
    
if __name__ == "__main__":
    test_auth_flow()
