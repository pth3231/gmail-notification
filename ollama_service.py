"""
Ollama Service - Local LLM Integration

Provides functions to:
- Connect to local Ollama instance
- Send email text for summarization
- Handle timeouts and connection errors gracefully
"""

import os
from typing import Optional
import requests

# Ollama configuration
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'gpt-oss:20b-cloud')
OLLAMA_TIMEOUT = 180  # seconds


def summarize_emails(combined_text: str) -> Optional[str]:
    """
    Send combined email text to Ollama for LLM summarization.
    
    Process:
    1. Create comprehensive summarization prompt
    2. Post to Ollama API with combined email text
    3. Return generated summary
    
    Resilience:
    - Handles connection errors (Ollama not running)
    - Handles timeouts (slow model)
    - Falls back to first 2000 chars of original text on error
    
    Args:
        combined_text: All email text combined as single string
    
    Returns:
        LLM-generated summary or fallback text on error
    """
    try:
        prompt = f"""Please create a summary of the following emails UNDER 64 words each mail, and UNDER 4MB (megabytes) in total.
Organize it clearly by numbering each email. Include sender, subject, and key information from each email.
Output ONLY the summary text, nothing else. Do not use any formatting like JSON or markdown, just plain text.
Ensure ALL important information is included and not truncated:

{combined_text}"""
        
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        print(f"\nSending to Ollama:")
        print(f"  - Model: {OLLAMA_MODEL}")
        print(f"  - Prompt length: {len(prompt)} chars")
        print(f"  - Combined text length: {len(combined_text)} chars")
        print(f"  - Prompt preview (first 300 chars):\n{prompt[:300]}\n")
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=OLLAMA_TIMEOUT)
        response.raise_for_status()
        
        result = response.json()
        summary = result.get('response', 'Failed to generate summary').strip()
        print(f"Summary received ({len(summary)} chars, {len(summary.encode('utf-8'))} bytes)")
        print(f"Summary preview (first 300 chars):\n{summary[:300]}\n")
        
        return summary
    except requests.exceptions.Timeout:
        print(f"✗ Ollama timeout after {OLLAMA_TIMEOUT}s")
        print("  Try: faster model or increase OLLAMA_TIMEOUT environment variable")
        return combined_text[:2000]
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to Ollama at {OLLAMA_API_URL}")
        print("  Is Ollama running? Start with: ollama serve")
        return combined_text[:2000]
    except Exception as e:
        print(f"✗ Ollama error: {type(e).__name__}: {e}")
        return combined_text[:2000]
