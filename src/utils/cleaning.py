"""
Email Cleaning Utilities - HTML Extraction and Content Sanitization

Provides functions to:
- Extract plain text from HTML email bodies
- Remove tracking pixels and web content
- Aggressively remove URLs, CSS, and junk from email content
- Sanitize headers for HTTP compatibility
"""

import base64
import re
import unicodedata
from typing import Optional
from bs4 import BeautifulSoup

from .. import config


def extract_email_body(payload: dict) -> str:
    """
    Extract email body from Gmail payload, converting HTML to plain text.
    
    Process:
    1. Check for direct text/plain or text/html in payload
    2. If multipart, recursively search parts for text content
    3. For HTML: Parse with BeautifulSoup, remove content-free tags
    4. Extract text and filter out footer/tracking patterns
    
    Args:
        payload: Email payload dict from Gmail API
    
    Returns:
        Clean email body text as string
    """
    if 'data' in payload['body']:
        encoded_data = payload['body']['data']
        decoded_data = base64.urlsafe_b64decode(encoded_data).decode('utf-8')
        return decoded_data
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                return extract_email_body(part)
            elif part['mimeType'] == 'text/html':
                html_data = extract_email_body(part)
                soup = BeautifulSoup(html_data, 'html.parser')
                
                # Remove style tags and their content FIRST
                for style in soup.find_all('style'):
                    style.decompose()
                
                # Remove script tags
                for script in soup.find_all('script'):
                    script.decompose()
                
                # Remove anchor tags completely (text and all)
                for tag in soup.find_all('a'):
                    tag.decompose()
                
                # Remove all non-content tags
                for tag in soup(["meta", "link", "head", "title",
                                "noscript", "iframe", "object", "embed",
                                "table", "tbody", "tr", "td", "tfoot", "thead",
                                "button", "form", "input", "textarea", "select"]):
                    tag.decompose()
                
                # Remove tracking pixels and spacer images
                for img in soup.find_all('img'):
                    width = img.get('width', '0')
                    height = img.get('height', '0')
                    try:
                        if (int(str(width).split('px')[0]) < config.TRACKING_PIXEL_SIZE_THRESHOLD and 
                            int(str(height).split('px')[0]) < config.TRACKING_PIXEL_SIZE_THRESHOLD):
                            img.decompose()
                    except:
                        if not img.get('alt'):
                            img.decompose()
                
                # Get clean text
                text = soup.get_text(separator='\n')
                lines = text.split('\n')
                
                # Filter out tracking URLs and web beacons
                filtered_lines = []
                for line in lines:
                    if line.strip().startswith('http') or line.strip().startswith('www.'):
                        continue
                    if any(keyword in line.lower() for keyword in config.EMAIL_FOOTER_KEYWORDS):
                        continue
                    filtered_lines.append(line)
                
                text = '\n'.join(filtered_lines)
                return text
    return ""


def clean_email_content(text: str) -> str:
    """
    Aggressively clean email text by removing URLs, CSS, HTML entities, and junk.
    
    Removal targets:
    - All URLs (http://, https://, ftp://, www.)
    - Action prefixes (View job, Read more, See all, etc.)
    - CSS blocks and properties (font-size, padding, etc.)
    - HTML entities (&nbsp;, &#123;, etc.)
    - Email addresses
    - Symbol-only lines and excessive whitespace
    - Separator lines (-----, ====, etc.)
    
    Args:
        text: Raw email text to clean
    
    Returns:
        Cleaned email text with URLs and junk removed
    """
    if not text:
        return ""
    
    # AGGRESSIVE URL REMOVAL
    text = re.sub(r'https?://[^\s\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'ftp://[^\s\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'www\.[^\s\n]*', '', text, flags=re.IGNORECASE)
    
    # Remove action prefixes
    action_prefixes = ['View job', 'View profile', 'View post', 'Read more', 'See all', 
                       'Click here', 'Edit alert', 'View on', 'Learn more', 'More info',
                       'Apply now', 'Apply here', 'Learn', 'Discover', 'Check out', 'View ',
                       'Join ', 'Accept ', 'Manage ']
    for prefix in action_prefixes:
        text = re.sub(rf'\b{prefix}[:\-\s]*\n?', '', text, flags=re.IGNORECASE)
    
    # AGGRESSIVE CSS REMOVAL
    text = re.sub(r'\{[^}]*\}', '', text, flags=re.DOTALL)
    text = re.sub(r'(font|padding|margin|display|color|background|border|width|height|line-height|size|weight|family|style|text)\s*:\s*[^;]*;?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(px|pt|em|rem|important|!important|none|block|inline|flex|grid)\b', '', text, flags=re.IGNORECASE)
    
    # Remove separator lines
    text = re.sub(r'^-{5,}$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^={5,}$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^_{5,}$', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', text)
    
    # Remove HTML entities and special codes
    text = re.sub(r'&[a-z]+;', '', text, flags=re.IGNORECASE)
    text = re.sub(r'&#\d+;', '', text)
    text = re.sub(r'&#x[0-9a-fA-F]+;', '', text, flags=re.IGNORECASE)
    
    # Remove lines that are purely whitespace or symbols
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r'^[\s\.\-_#>+~\*\[\]{};:="\',|()@]+$', stripped):
            continue
        cleaned_lines.append(stripped)
    
    # Aggressively remove excessive newlines
    text = '\n'.join(cleaned_lines)
    text = re.sub(r'\n\n+', '\n', text)
    
    # Remove excessive spaces
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\t+', ' ', text)
    
    return text.strip()


def sanitize_header(text: str) -> str:
    """
    Convert Unicode characters to ASCII-safe equivalents for HTTP headers.
    
    Some HTTP services (like ntfy.sh) have strict header encoding requirements.
    This function normalizes Unicode characters and replaces incompatible ones.
    
    Args:
        text: Header text potentially containing Unicode characters
    
    Returns:
        ASCII-safe header text
    """
    text = unicodedata.normalize('NFKD', text)
    return text.encode('ascii', errors='replace').decode('ascii')
