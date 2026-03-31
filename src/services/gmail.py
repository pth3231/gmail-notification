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

from .. import config


class GmailService:
    """Gmail API service wrapper for OAuth2 authentication and email retrieval."""
    
    def __init__(self) -> None:
        """Initialize Gmail service."""
        self.service: Optional[Resource] = None
    
    def authenticate(self) -> Resource:
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
        if os.path.exists(config.TOKEN_FILE):
            credentials = Credentials.from_authorized_user_file(
                config.TOKEN_FILE, config.GMAIL_SCOPES
            )
        
        # Handle token validity and refresh
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print("Refreshing expired OAuth token...")
                try:
                    credentials.refresh(Request())
                    print("✓ Token refreshed successfully")
                except Exception as e:
                    print(f"✗ Token refresh failed: {e}")
                    print("Initiating new Gmail OAuth2 authentication...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        config.CREDENTIALS_FILE, config.GMAIL_SCOPES
                    )
                    credentials = flow.run_local_server(port=0)
            else:
                print("Initiating new Gmail OAuth2 authentication...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.CREDENTIALS_FILE, config.GMAIL_SCOPES
                )
                credentials = flow.run_local_server(port=0)
            
            # Save token for future use
            with open(config.TOKEN_FILE, 'w') as token_file:
                token_file.write(credentials.to_json())
        
        self.service = build('gmail', 'v1', credentials=credentials)
        return self.service
    
    def get_service(self) -> Resource:
        """Get authenticated Gmail service, authenticating if needed."""
        if not self.service:
            self.authenticate()
        return self.service
    
    def fetch_unread_emails(self, max_results: int = 5) -> Optional[Tuple[List[Dict[str, Any]], Resource]]:
        """
        Fetch unread emails from Gmail inbox.
        
        Args:
            max_results: Maximum number of emails to fetch (default: 5)
        
        Returns:
            Tuple of (messages list, Gmail service) or None if no emails found
            Each message contains: {'id': str, 'threadId': str}
        """
        service = self.get_service()
        
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
