"""
Email Service - Extraction, Cleaning, and Combination

Provides functions to:
- Extract email metadata (sender, subject) from Gmail messages
- Extract and clean email body content
- Combine multiple emails into formatted text
"""

from typing import List, Dict, Any
from googleapiclient.discovery import Resource

from ..utils import cleaning


class EmailService:
    """Email extraction and processing service."""
    
    @staticmethod
    def extract_emails_data(
        messages: List[Dict[str, Any]],
        gmail_service: Resource
    ) -> List[Dict[str, str]]:
        """
        Extract sender, subject, and cleaned body from Gmail messages.
        
        Args:
            messages: List of message objects from Gmail API (each has 'id')
            gmail_service: Authenticated Gmail API service object
        
        Returns:
            List of dicts with keys: 'sender', 'subject', 'body'
        """
        extracted_emails = []
        
        for msg_index, msg in enumerate(messages, 1):
            msg_detail = gmail_service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            payload = msg_detail['payload']
            headers = payload.get('headers', [])
            
            # Extract sender and subject from headers
            sender = EmailService._extract_header_value(headers, 'From', 'Unknown Sender')
            subject = EmailService._extract_header_value(headers, 'Subject', 'No Subject')
            
            # Extract raw email body and apply aggressive cleaning
            raw_body = cleaning.extract_email_body(payload)
            cleaned_body = cleaning.clean_email_content(raw_body)
            
            extracted_emails.append({
                'sender': sender,
                'subject': subject,
                'body': cleaned_body
            })
            
            print(f"  [{msg_index}] {subject}")
        
        return extracted_emails
    
    @staticmethod
    def combine_emails(emails_data: List[Dict[str, str]]) -> str:
        """
        Combine multiple emails into single formatted text block.
        
        Format:
            EMAIL 1:
            From: sender@example.com
            Subject: Email Subject
            Body:
            Email content here...
            ------
            
            EMAIL 2:
            ...
        
        Args:
            emails_data: List of email dicts with 'sender', 'subject', 'body'
        
        Returns:
            Single string combining all emails with clear separators
        """
        if not emails_data:
            return ""
        
        combined_text = ""
        
        for email_index, email in enumerate(emails_data, 1):
            combined_text += f"EMAIL {email_index}:\n"
            combined_text += f"From: {email['sender']}\n"
            combined_text += f"Subject: {email['subject']}\n"
            combined_text += f"Body:\n{email['body']}\n"
            combined_text += "-" * 70 + "\n\n"
        
        # Log statistics
        text_chars = len(combined_text)
        text_bytes = len(combined_text.encode('utf-8'))
        email_count = len(emails_data)
        
        print(f"Combined {email_count} emails: {text_chars} chars, {text_bytes} bytes")
        if combined_text:
            print(f"Preview: {combined_text[:200]}...\n")
        
        return combined_text
    
    @staticmethod
    def _extract_header_value(
        headers: List[Dict[str, str]],
        header_name: str,
        default_value: str
    ) -> str:
        """
        Extract specific header value from email headers list.
        
        Args:
            headers: List of {'name': str, 'value': str} dicts
            header_name: Name of header to find (case-sensitive)
            default_value: Value to return if header not found
        
        Returns:
            Header value or default value
        """
        return next(
            (header['value'] for header in headers if header['name'] == header_name),
            default_value
        )
