"""
Gmail Notification Service - Main Entry Point

Orchestrates the complete email notification pipeline:
1. Fetches unread emails from Gmail
2. Extracts and cleans email content
3. Combines emails for processing
4. Summarizes content using local LLM
5. Sends summary via ntfy.sh notification service
"""

from src.pipeline import EmailPipeline


def main() -> None:
    """Main entry point - orchestrates the complete email processing pipeline."""
    pipeline = EmailPipeline(max_emails=5)
    success = pipeline.run()
    exit(0 if success else 1)


if __name__ == '__main__':
    main()
