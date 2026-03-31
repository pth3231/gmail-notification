"""
Notification Service - Push Notifications

Provides functions to:
- Send notifications to ntfy.sh service
- Handle UTF-8 encoding for international characters
- Sanitize headers for HTTP compatibility
"""

from typing import Optional
import requests

from .. import config
from ..utils import cleaning


class NotificationService:
    """Push notification service for ntfy.sh."""
    
    @staticmethod
    def send_notification(title: str, message: str) -> bool:
        """
        Send notification to ntfy.sh push notification service.
        
        Features:
        - UTF-8 encoding for international characters
        - Header sanitization to ASCII-safe characters
        - Message truncation to fit ntfy.sh limits (4096 bytes)
        - Timeout handling
        
        Args:
            title: Notification title (will be sanitized)
            message: Notification body (UTF-8 encoded, will be truncated if needed)
        
        Returns:
            True if successful, False on error
        """
        try:
            if not message:
                print("✗ Empty message, cannot send notification")
                return False
            
            # Prepare headers with sanitized title
            headers = {
                'Title': cleaning.sanitize_header(title),
                'Tags': 'email,notification',
                'Content-Type': 'text/plain; charset=utf-8',
                'Priority': 'high',
            }
            
            # Encode message as UTF-8 bytes
            message_bytes = message.encode('utf-8')
            message_char_count = len(message)
            message_byte_count = len(message_bytes)
            
            # ntfy.sh has a limit of ~4096 bytes for messages
            # Reserve space for headers (~200 bytes)
            MAX_MESSAGE_BYTES = 4000
            if message_byte_count > MAX_MESSAGE_BYTES:
                print(f"⚠ Message too large ({message_byte_count} bytes), truncating to {MAX_MESSAGE_BYTES} bytes")
                # Truncate to byte limit, being careful with UTF-8
                truncated = message_bytes[:MAX_MESSAGE_BYTES]
                # Remove incomplete UTF-8 sequences at the end
                while truncated:
                    try:
                        message = truncated.decode('utf-8')
                        message_bytes = truncated
                        break
                    except UnicodeDecodeError:
                        truncated = truncated[:-1]
            
            message_byte_count = len(message_bytes)
            
            print(f"Sending notification to ntfy.sh/{config.NTFY_TOPIC}")
            print(f"  - Title: {title}")
            print(f"  - Size: {message_char_count} chars ({message_byte_count} bytes)")
            
            # Send POST request
            response = requests.post(
                config.NTFY_FULL_URL,
                data=message_bytes,
                headers=headers,
                timeout=config.NTFY_TIMEOUT
            )
            response.raise_for_status()
            
            print(f"✓ Sent successfully (HTTP {response.status_code})")
            return True
        except requests.exceptions.Timeout:
            print(f"✗ ntfy.sh timeout after {config.NTFY_TIMEOUT}s")
            return False
        except requests.exceptions.ConnectionError:
            print(f"✗ Cannot connect to {config.NTFY_BASE_URL}")
            return False
        except Exception as e:
            print(f"✗ Error sending notification: {type(e).__name__}: {e}")
            return False
