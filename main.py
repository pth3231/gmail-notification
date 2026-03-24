"""
Gmail Notification Service

Main orchestrator for the email notification pipeline:
1. Fetches unread emails from Gmail
2. Extracts and cleans email content
3. Combines emails for processing
4. Summarizes content using local LLM (Ollama)
5. Sends summary via ntfy.sh notification service
"""

import gmail_service
import email_processor
import ollama_service
import ntfy_service


def main() -> None:
    """
    Main entry point - orchestrates the complete email processing pipeline.
    
    Workflow:
        1. Fetch unread emails from Gmail
        2. Extract sender, subject, and cleaned body for each email
        3. Combine all emails into single text
        4. Generate summary using Ollama LLM
        5. Send summary via ntfy.sh
    """
    print("=" * 70)
    print("Gmail Notification Service - Starting...")
    print("=" * 70 + "\n")
    
    # ========== STEP 1: Fetch emails from Gmail ==========
    print("[Step 1] Fetching unread emails from Gmail...")
    emails_result = gmail_service.fetch_unread_emails(max_results=5)
    
    if not emails_result:
        print("✗ No unread emails found. Exiting.")
        return
    
    messages, gmail_service_obj = emails_result
    print(f"✓ Fetched {len(messages)} unread email(s)\n")
    
    # ========== STEP 2: Extract email details ==========
    print("[Step 2] Extracting and cleaning email content...")
    extracted_emails = email_processor.extract_emails_data(messages, gmail_service_obj)
    
    if not extracted_emails:
        print("✗ Failed to extract email data. Exiting.")
        return
    
    print(f"✓ Extracted {len(extracted_emails)} email(s)\n")
    
    # ========== STEP 3: Combine emails ==========
    print("[Step 3] Combining emails for processing...")
    combined_email_text = email_processor.combine_emails(extracted_emails)
    
    if not combined_email_text:
        print("✗ No email content to process. Exiting.")
        return
    
    print()
    
    # ========== STEP 4: Summarize with LLM ==========
    print("[Step 4] Generating summary with Ollama LLM...")
    summary_text = ollama_service.summarize_emails(combined_email_text)
    
    if not summary_text:
        print("✗ Failed to generate summary. Exiting.")
        return
    
    print()
    
    # ========== STEP 5: Send notification ==========
    print("[Step 5] Sending summary via ntfy.sh...")
    notification_title = f"Gmail Summary ({len(extracted_emails)} emails)"
    success = ntfy_service.send_notification(notification_title, summary_text)
    
    if success:
        print("\n" + "=" * 70)
        print("✓ Pipeline completed successfully!")
        print("=" * 70)
    else:
        print("\n✗ Pipeline completed with notification errors.")


if __name__ == '__main__':
    main()
