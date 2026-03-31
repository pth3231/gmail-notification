#!/usr/bin/env python3
"""
Diagnostic script to check Ollama configuration and connectivity
"""

import os
import requests
from src import config

def check_ollama_connection():
    """Check if Ollama is running and accessible."""
    print("=" * 70)
    print("Ollama Configuration Check")
    print("=" * 70 + "\n")
    
    print(f"Ollama API URL: {config.OLLAMA_API_URL}")
    print(f"Ollama Model: {config.OLLAMA_MODEL}")
    print(f"Ollama Timeout: {config.OLLAMA_TIMEOUT}s\n")
    
    try:
        # Try to connect to Ollama
        response = requests.get(
            config.OLLAMA_API_URL.replace('/api/generate', '/api/tags'),
            timeout=5
        )
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("✓ Ollama is running!")
            print(f"\n  Available models ({len(models)}):")
            for model in models:
                name = model.get('name', 'unknown')
                size = model.get('size', 0)
                size_mb = size / (1024**3)
                print(f"    - {name} ({size_mb:.1f} GB)")
            
            # Check if configured model is available
            available_model_names = [m.get('name', '') for m in models]
            if config.OLLAMA_MODEL in available_model_names:
                print(f"\n✓ Model '{config.OLLAMA_MODEL}' is installed")
            else:
                print(f"\n✗ Model '{config.OLLAMA_MODEL}' is NOT installed")
                print(f"  To install: ollama pull {config.OLLAMA_MODEL}")
        else:
            print(f"✗ Ollama returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Ollama")
        print("  Make sure Ollama is running: ollama serve")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    check_ollama_connection()
