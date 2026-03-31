"""
Pipeline Module - Email Processing Pipeline Orchestrator

Provides the EmailPipeline class that orchestrates the complete email processing workflow:
1. Fetch unread emails from Gmail
2. Extract and clean email content
3. Combine emails for processing
4. Summarize content using local LLM
5. Send summary via notification service
"""

from typing import Optional, List, Dict, Any

from . import config
from .services.gmail import GmailService
from .services.email import EmailService
from .services.llm import LLMService
from .services.notification import NotificationService


class EmailPipeline:
    """
    Email processing pipeline orchestrator.
    
    Manages the complete workflow of fetching, processing, summarizing, and
    notifying about unread emails.
    """
    
    def __init__(self, max_emails: int = 5) -> None:
        """
        Initialize the pipeline.
        
        Args:
            max_emails: Maximum number of emails to process in each run
        """
        self.max_emails = max_emails
        self.gmail_service = GmailService()
        self.email_service = EmailService()
        self.llm_service = LLMService()
        self.notification_service = NotificationService()
    
    def run(self) -> bool:
        """
        Execute the complete email processing pipeline.
        
        Workflow:
        1. Fetch unread emails from Gmail
        2. Extract sender, subject, and cleaned body for each email
        3. Combine all emails into single text
        4. Generate summary using LLM
        5. Send summary via notification service
        
        Returns:
            True if pipeline completed successfully, False on error
        """
        self._print_header("Starting Email Pipeline")
        
        # Step 1: Fetch emails
        if not self._step_fetch_emails():
            return False
        
        # Step 2: Extract email data
        if not self._step_extract_emails():
            return False
        
        # Step 3: Combine emails
        if not self._step_combine_emails():
            return False
        
        # Step 4: Summarize with LLM
        if not self._step_summarize():
            return False
        
        # Step 5: Send notification
        if not self._step_send_notification():
            return False
        
        self._print_footer("Pipeline completed successfully!")
        return True
    
    def _step_fetch_emails(self) -> bool:
        """Step 1: Fetch unread emails from Gmail."""
        print("[Step 1] Fetching unread emails from Gmail...")
        
        result = self.gmail_service.fetch_unread_emails(max_results=self.max_emails)
        
        if not result:
            print("✗ No unread emails found. Exiting.")
            return False
        
        self.messages, self.gmail_service_obj = result
        print(f"✓ Fetched {len(self.messages)} unread email(s)\n")
        return True
    
    def _step_extract_emails(self) -> bool:
        """Step 2: Extract and clean email content."""
        print("[Step 2] Extracting and cleaning email content...")
        
        self.extracted_emails = self.email_service.extract_emails_data(
            self.messages,
            self.gmail_service_obj
        )
        
        if not self.extracted_emails:
            print("✗ Failed to extract email data. Exiting.")
            return False
        
        print(f"✓ Extracted {len(self.extracted_emails)} email(s)\n")
        return True
    
    def _step_combine_emails(self) -> bool:
        """Step 3: Combine emails into single text."""
        print("[Step 3] Combining emails for processing...")
        
        self.combined_email_text = self.email_service.combine_emails(
            self.extracted_emails
        )
        
        if not self.combined_email_text:
            print("✗ No email content to process. Exiting.")
            return False
        
        print()
        return True
    
    def _step_summarize(self) -> bool:
        """Step 4: Summarize emails with LLM."""
        print("[Step 4] Generating summary with LLM...")
        
        self.summary_text = self.llm_service.summarize_emails(
            self.combined_email_text
        )
        
        if not self.summary_text:
            print("✗ Failed to generate summary. Exiting.")
            return False
        
        print()
        return True
    
    def _step_send_notification(self) -> bool:
        """Step 5: Send notification via ntfy.sh."""
        print("[Step 5] Sending summary via ntfy.sh...")
        
        # Ensure summary exists before sending
        if not self.summary_text:
            print("✗ No summary to send. Exiting.")
            return False
        
        notification_title = f"Gmail Summary ({len(self.extracted_emails)} emails)"
        success = self.notification_service.send_notification(
            notification_title,
            self.summary_text
        )
        
        if not success:
            print("✗ Failed to send notification.")
            return False
        
        return True
    
    def _print_header(self, message: str) -> None:
        """Print formatted pipeline header."""
        print(config.PIPELINE_SEPARATOR)
        print(f"{message}...")
        print(config.PIPELINE_SEPARATOR + "\n")
    
    def _print_footer(self, message: str) -> None:
        """Print formatted pipeline footer."""
        print("\n" + config.PIPELINE_SEPARATOR)
        print(f"✓ {message}")
        print(config.PIPELINE_SEPARATOR)
