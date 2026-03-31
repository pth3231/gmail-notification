import sys
import os

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))

from src.services.gmail import GmailService

print("==== Fetching unread emails from Gmail ====")

gmail_service = GmailService()
result = gmail_service.fetch_unread_emails(max_results=3)
    
if not result:
    print("No emails to process.")
    exit(1)

messages, service = result

print(f"Fetched {len(messages)} unread email(s)\n")
print(messages)

extracted_data = []
    
print("==== Fetching unread emails from Gmail ====")
for msg in messages:
    msg_detail = service.users().messages().get(
        userId='me', 
        id=msg['id'], 
        format='full'
    ).execute()
    
    print(msg_detail)
