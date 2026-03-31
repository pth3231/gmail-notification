"""
LLM Service - Local LLM Integration

Provides functions to:
- Connect to local Ollama instance
- Send email text for summarization
- Handle timeouts and connection errors gracefully
"""

from typing import Optional
import requests

from .. import config


class LLMService:
    """Local LLM (Ollama) integration service."""
    
    @staticmethod
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
            prompt = config.LLM_SUMMARIZATION_PROMPT.format(combined_text=combined_text)
            
            payload = {
                "model": config.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
            
            print(f"\nSending to Ollama:")
            print(f"  - Model: {config.OLLAMA_MODEL}")
            print(f"  - API URL: {config.OLLAMA_API_URL}")
            print(f"  - Prompt length: {len(prompt)} chars")
            print(f"  - Combined text length: {len(combined_text)} chars")
            print(f"  - Timeout: {config.OLLAMA_TIMEOUT}s")
            
            response = requests.post(
                config.OLLAMA_API_URL,
                json=payload,
                timeout=config.OLLAMA_TIMEOUT
            )
            response.raise_for_status()
            
            result = response.json()
            summary = result.get('response', '').strip()
            
            if not summary:
                print(f"✗ Empty response from Ollama")
                return combined_text[:2000]
            
            print(f"✓ Summary received ({len(summary)} chars, {len(summary.encode('utf-8'))} bytes)")
            print(f"Summary preview (first 200 chars):\n{summary[:200]}...\n")
            
            return summary
        except requests.exceptions.Timeout:
            print(f"✗ Ollama timeout after {config.OLLAMA_TIMEOUT}s")
            print(f"  Model: {config.OLLAMA_MODEL}")
            print("  Try: faster model, more memory, or increase OLLAMA_TIMEOUT")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"✗ Cannot connect to Ollama at {config.OLLAMA_API_URL}")
            print(f"  Error: {e}")
            print("  Is Ollama running? Start with: ollama serve")
            return None
        except Exception as e:
            print(f"✗ Ollama error: {type(e).__name__}: {e}")
            return None
