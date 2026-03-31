"""
Configuration Module - Centralized Settings

Manages all configuration constants and environment variables:
- Gmail API settings
- Ollama/LLM settings
- ntfy.sh notification settings
- File paths
"""

import os
from typing import Final

# ==================== Gmail API Configuration ====================
GMAIL_SCOPES: Final[list] = ['https://www.googleapis.com/auth/gmail.readonly']
GMAIL_MAX_RESULTS: Final[int] = int(os.getenv('GMAIL_MAX_RESULTS', '5'))

# File paths for OAuth2
TOKEN_FILE: Final[str] = 'token.json'
CREDENTIALS_FILE: Final[str] = 'credentials.json'

# ==================== Ollama/LLM Configuration ====================
OLLAMA_API_URL: Final[str] = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')
OLLAMA_MODEL: Final[str] = os.getenv('OLLAMA_MODEL', 'gpt-oss:120b-cloud')
OLLAMA_TIMEOUT: Final[int] = int(os.getenv('OLLAMA_TIMEOUT', '180'))  # seconds

# LLM Summarization prompt
LLM_SUMMARIZATION_PROMPT: Final[str] = """Please create a summary of the following emails UNDER 64 words each mail, and STRICTLY UNDER 3.5MB (megabytes) in total.
Organize it clearly by numbering each email. Include sender, subject, and key information from each email.
Output ONLY the summary text, nothing else. Do not use any formatting like JSON or markdown, just plain text.
Ensure ALL important information is included and not truncated:

{combined_text}"""

# ==================== ntfy.sh Configuration ====================
NTFY_TOPIC: Final[str] = os.getenv('NTFY_TOPIC', 'gmail-summary')
NTFY_BASE_URL: Final[str] = 'https://ntfy.sh'
NTFY_FULL_URL: Final[str] = f"{NTFY_BASE_URL}/{NTFY_TOPIC}"
NTFY_TIMEOUT: Final[int] = int(os.getenv('NTFY_TIMEOUT', '30'))  # seconds

# ==================== Email Cleaning Configuration ====================
EMAIL_FOOTER_KEYWORDS: Final[list] = [
    'unsubscribe', 'preferences', 'view in browser',
    'forwarded', 'original message', 'begin forwarded',
    'footer', 'reply to this email', 'change your email'
]

TRACKING_PIXEL_SIZE_THRESHOLD: Final[int] = 10  # pixels

# ==================== Pipeline Configuration ====================
PIPELINE_SEPARATOR: Final[str] = "=" * 70
SECTION_SEPARATOR: Final[str] = "-" * 70
