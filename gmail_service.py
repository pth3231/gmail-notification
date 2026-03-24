"""
Gmail Service - OAuth2 Authentication & Email Retrieval

Provides functions to:
- Authenticate with Gmail API using OAuth2
- Fetch unread emails from inbox
- Return service object for further API calls
"""

import os.path
from typing import Optional, Tuple, List, Dict, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.discovery import Resource

# Gmail API configuration
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'


def get_gmail_service() -> Resource:
    """
    Authenticate with Gmail API and return authenticated service object.
    
    Uses OAuth2 flow with token persistence:
    - Loads cached token.json if available and valid
    - Refreshes token if expired but refresh token exists
    - Initiates new OAuth2 flow if no token or refresh fails
    
    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail API service
    """
    credentials = None
    
    # Try to load existing token
    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, GMAIL_SCOPES)
    
    # Handle token validity and refresh
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            # Token expired but can be refreshed
            print("Refreshing expired OAuth token...")
            credentials.refresh(Request())
        else:
            # Need new authentication via OAuth2 flow
            print("Initiating new Gmail OAuth2 authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, GMAIL_SCOPES
            )
            credentials = flow.run_local_server(port=0)
        
        # Save token for future use
        with open(TOKEN_FILE, 'w') as token_file:
            token_file.write(credentials.to_json())
    
    return build('gmail', 'v1', credentials=credentials)


def fetch_unread_emails(
    max_results: int = 7
) -> Optional[Tuple[List[Dict[str, Any]], Resource]]:
    """
    Fetch unread emails from Gmail inbox.
    
    Args:
        max_results: Maximum number of emails to fetch (default: 7)
    
    Returns:
        Tuple of (messages list, Gmail service) or None if no emails found
        Each message contains: {'id': str, 'threadId': str}
    """
    service = get_gmail_service()
    
    # Query for unread emails in inbox
    results = service.users().messages().list(
        userId='me',
        q='is:unread in:inbox',
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        return None
    
    return messages, service
