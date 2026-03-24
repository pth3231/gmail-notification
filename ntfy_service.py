"""
Ntfy Service - Push Notifications

Provides functions to:
- Send notifications to ntfy.sh service
- Handle UTF-8 encoding for international characters
- Sanitize headers for HTTP compatibility
"""

import os
from typing import Optional
import requests
import cleaning

# ntfy.sh configuration
NTFY_TOPIC = os.getenv('NTFY_TOPIC', 'gmail-summary')
NTFY_BASE_URL = 'https://ntfy.sh'
NTFY_FULL_URL = f"{NTFY_BASE_URL}/{NTFY_TOPIC}"
NTFY_TIMEOUT = 30  # seconds


def send_notification(title: str, message: str) -> bool:
    """
    Send notification to ntfy.sh push notification service.
    
    Features:
    - UTF-8 encoding for international characters
    - Header sanitization to ASCII-safe characters
    - Timeout handling
    
    Args:
        title: Notification title (will be sanitized)
        message: Notification body (UTF-8 encoded)
    
    Returns:
        True if successful, False on error
    """
    try:
        # Prepare headers with sanitized title
        headers = {
            'Title': cleaning.sanitize_header(title),
            'Tags': 'email,notification',
            'Content-Type': 'text/plain; charset=utf-8'
        }
        
        # Encode message as UTF-8 bytes
        message_bytes = message.encode('utf-8')
        message_char_count = len(message)
        message_byte_count = len(message_bytes)
        
        print(f"Sending notification to ntfy.sh/{NTFY_TOPIC}")
        print(f"  - Title: {title}")
        print(f"  - Size: {message_char_count} chars ({message_byte_count} bytes)")
        
        # Send POST request
        response = requests.post(
            NTFY_FULL_URL,
            data=message_bytes,
            headers=headers,
            timeout=NTFY_TIMEOUT
        )
        response.raise_for_status()
        
        print(f"✓ Sent successfully (HTTP {response.status_code})")
        return True
    except requests.exceptions.Timeout:
        print(f"✗ ntfy.sh timeout after {NTFY_TIMEOUT}s")
        return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to {NTFY_BASE_URL}")
        return False
    except Exception as e:
        print(f"✗ Error sending notification: {type(e).__name__}: {e}")
        return False
