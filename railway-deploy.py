#!/usr/bin/env python3
"""
EduForge AI - Railway Deployment Script
"""
import urllib.request
import urllib.parse
import json
import os
import sys

PROJECT_ID = "3d1fbc84-0967-4b43-8b36-98ad4ff8afd2"

def deploy_to_railway():
    print("=" * 50)
    print("EduForge AI - Railway Deployment")
    print("=" * 50)
    print()
    print("STEP 1: Get Railway Token")
    print("-" * 50)
    print("1. Go to: https://railway.com/project/" + PROJECT_ID)
    print("2. Click Settings (gear icon)")
    print("3. Click 'API'")
    print("4. Click 'Create Token'")
    print("5. Copy the token and paste it below")
    print()
    
    token = input("Paste Railway Token here: ").strip()
    
    if not token:
        print("Token is required!")
        return
    
    print()
    print("[*] Connecting to Railway...")
    
    # Set up headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Get project info
    try:
        req = urllib.request.Request(
            f'https://api.railway.app/v1/projects/{PROJECT_ID}',
            headers=headers
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(f"[+] Connected to project: {data.get('name', 'Unknown')}")
    except Exception as e:
        print(f"[-] Error: {e}")
        return
    
    print()
    print("[+] Creating deployment...")
    
    # Create deployment payload
    payload = {
        'serviceId': None,  # Will create new service
        'branch': 'main',
        'repo': 'https://github.com/zeyadsaeed2025-wq/zezo.edu.Ai',
        'rootDirectory': 'backend'
    }
    
    try:
        req = urllib.request.Request(
            f'https://api.railway.app/v1/projects/{PROJECT_ID}/deployments',
            data=json.dumps(payload).encode(),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(f"[+] Deployment started!")
            print(f"    Check status at: https://railway.com/project/{PROJECT_ID}")
    except Exception as e:
        print(f"[-] Error starting deployment: {e}")
        print()
        print("Please add environment variables manually:")
        print("  1. Go to Railway project settings")
        print("  2. Add DATABASE_URL = sqlite+aiosqlite:///./eduforge.db")
        print("  3. Add SECRET_KEY = eduforge-secret-2024")
        print("  4. Add OPENAI_API_KEY = (your OpenAI key)")

if __name__ == "__main__":
    deploy_to_railway()
