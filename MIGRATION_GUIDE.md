# Refactoring Migration Guide

## What Changed

The codebase has been refactored from a flat, function-based structure to a modular, class-based architecture.

## New Directory Structure

```
gmail-notification/
├── src/                          # New: All source code
│   ├── __init__.py
│   ├── config.py                # New: Centralized configuration
│   ├── pipeline.py              # New: Pipeline orchestrator
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gmail.py             # Refactored: GmailService class
│   │   ├── email.py             # Refactored: EmailService class
│   │   ├── llm.py               # Refactored: LLMService class
│   │   └── notification.py      # Refactored: NotificationService class
│   └── utils/
│       ├── __init__.py
│       └── cleaning.py          # Moved: Email cleaning utilities
├── main.py                       # Updated: Simplified entry point
├── README.md                     # Updated: New structure documented
├── REFACTORING_SUMMARY.md        # Updated: Detailed changes
└── ... (config files unchanged)
```

## Old Files (No Longer Used)

The following files are **still in the root directory** but are superseded:

- `gmail_service.py` → `src/services/gmail.py`
- `email_processor.py` → `src/services/email.py`
- `cleaning.py` → `src/utils/cleaning.py`
- `ollama_service.py` → `src/services/llm.py`
- `ntfy_service.py` → `src/services/notification.py`

**You can delete these old files** after verifying the new structure works.

## How to Use

### Running the Application

```bash
# Make sure you're in the root directory
python main.py
```

The new `main.py` is much simpler:

```python
from src.pipeline import EmailPipeline

pipeline = EmailPipeline(max_emails=5)
success = pipeline.run()
```

### Accessing Configuration

**Old way:**

```python
from gmail_service import GMAIL_SCOPES, TOKEN_FILE
from ollama_service import OLLAMA_MODEL
```

**New way:**

```python
from src import config

GMAIL_SCOPES = config.GMAIL_SCOPES
OLLAMA_MODEL = config.OLLAMA_MODEL
```

### Using Services Directly

**Old way:**

```python
import gmail_service
import email_processor

emails_result = gmail_service.fetch_unread_emails()
extracted = email_processor.extract_emails_data(messages, service)
```

**New way:**

```python
from src.services.gmail import GmailService
from src.services.email import EmailService

gmail_svc = GmailService()
emails_result = gmail_svc.fetch_unread_emails()

email_svc = EmailService()
extracted = email_svc.extract_emails_data(messages, service)
```

### Complete Pipeline

**Old way:**

```python
# Manual step-by-step in main.py
emails_result = gmail_service.fetch_unread_emails()
extracted_emails = email_processor.extract_emails_data(...)
combined = email_processor.combine_emails(extracted_emails)
summary = ollama_service.summarize_emails(combined)
ntfy_service.send_notification(title, summary)
```

**New way:**

```python
from src.pipeline import EmailPipeline

pipeline = EmailPipeline(max_emails=5)
success = pipeline.run()
```

## Backward Compatibility

✓ **Configuration is unchanged:**

- All environment variables still work
- `credentials.json` and `token.json` are still used
- `.env` file support unchanged

✓ **Functionality is unchanged:**

- Same workflow
- Same error handling
- Same output format

## Benefits of New Structure

1. **Services are classes** - Easier to mock, test, and extend
2. **Configuration is centralized** - One place to find all settings
3. **Pipeline is clear** - Step-by-step flow is explicit
4. **Better organization** - Related functions grouped together
5. **Easier to extend** - Add new services without modifying existing ones
6. **Ready for features** - Scheduling, logging, and monitoring are now easier

## Testing Individual Services

You can now test services independently:

```python
from src.services.gmail import GmailService
from src.services.email import EmailService
from src.utils.cleaning import clean_email_content

# Test Gmail service
gmail = GmailService()
gmail.authenticate()
emails = gmail.fetch_unread_emails(max_results=3)

# Test email cleaning
text = "Visit https://example.com to learn more"
cleaned = clean_email_content(text)
# Output: "Visit  to learn more"
```

## Cleanup (Optional)

After verifying everything works, you can remove the old files:

```bash
rm gmail_service.py email_processor.py cleaning.py ollama_service.py ntfy_service.py
```

Or keep them as backup reference.

## Need Help?

- Check `README.md` for file purposes
- Check `REFACTORING_SUMMARY.md` for detailed changes
- Read docstrings in service classes
- Check `src/config.py` for all configuration options
