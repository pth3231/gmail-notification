# Gmail Notification Service

A Python application that automatically fetches unread emails from Gmail, summarizes them using a local LLM (Ollama), and sends the summary via push notification (ntfy.sh).

## Motivation

Email overload is a common problem. With hundreds of daily emails, it's easy to miss important messages. This service:

- **Reduces email fatigue** by automatically summarizing multiple emails into a concise overview
- **Uses local LLM** (Ollama) for privacy - your emails stay on your machine, never sent to external APIs
- **Provides push notifications** via ntfy.sh so you stay informed without constantly checking Gmail
- **Cleans email content** by removing tracking pixels, URLs, CSS, and other web junk
- **Saves time** by intelligently combining and summarizing your most important messages

Perfect for:
- Busy professionals who need quick email summaries
- Privacy-conscious users who don't want cloud LLM services
- Anyone using digest emails or notification lists
- Teams wanting to monitor a shared inbox

## Folder Structure

```
gmail-notification/
├── README.md                      # This file
├── REFACTORING_SUMMARY.md         # Code refactoring documentation
├── main.py                        # Main entry point - orchestrates the pipeline
├── token.json                     # OAuth2 token (auto-generated, do not commit)
├── credentials.json               # Gmail API credentials (required)
│
├── gmail_service.py              # Gmail API authentication & email retrieval
├── email_processor.py            # Email extraction, cleaning, and combination
├── cleaning.py                   # HTML parsing and content sanitization
├── ollama_service.py             # Local LLM integration (Ollama)
├── ntfy_service.py               # Push notification delivery (ntfy.sh)
│
└── test.ipynb                    # Jupyter notebook for testing & debugging
```

### File Purposes

| File | Purpose |
|------|---------|
| `main.py` | Orchestrates the complete 5-step pipeline |
| `gmail_service.py` | OAuth2 authentication, email fetching |
| `email_processor.py` | Extract metadata, clean content, combine emails |
| `cleaning.py` | Remove URLs, CSS, HTML entities, tracking pixels |
| `ollama_service.py` | Send emails to local LLM for summarization |
| `ntfy_service.py` | Send summary notifications via ntfy.sh |
| `test.ipynb` | Interactive testing and debugging notebook |

## Setup

### Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Gmail account with API credentials
- ntfy.sh account (or local instance)
- Internet connection

### Step 1: Install Python Dependencies

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
pip install requests beautifulsoup4 lxml
pip install jupyter  # Optional, for testing with test.ipynb
```

Or install from requirements (if available):
```bash
pip install -r requirements.txt
```

### Step 2: Setup Ollama

1. **Install Ollama** from [ollama.ai](https://ollama.ai)

2. **Start Ollama server**:
   ```bash
   ollama serve
   ```
   (Keep this running in a separate terminal)

3. **Pull the model**:
   ```bash
   ollama pull gemma2:2b
   ```
   
   Alternatively, use a different model:
   ```bash
   ollama pull mistral:latest
   ollama pull neural-chat:latest
   ollama pull dolphin-mixtral:latest
   ```

### Step 3: Setup Gmail API Credentials

1. **Go to Google Cloud Console**: https://console.cloud.google.com/

2. **Create a new project**:
   - Click on the project selector
   - Click "NEW PROJECT"
   - Enter project name: "Gmail Notification"
   - Click "CREATE"

3. **Enable Gmail API**:
   - Search for "Gmail API"
   - Click "Gmail API"
   - Click "ENABLE"

4. **Create OAuth2 Credentials**:
   - Go to "Credentials" in the left menu
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Desktop application"
   - Click "CREATE"

5. **Download credentials**:
   - Click the download icon next to your credential
   - Save as `credentials.json` in the project root directory

6. **Set API permissions** (first run):
   - When you run the script for the first time, it will open a browser
   - Grant the requested Gmail read permissions
   - `token.json` will be created automatically

### Step 4: Configure Environment Variables (Optional)

Create a `.env` file or set environment variables to customize behavior:

```bash
# Ollama Configuration
OLLAMA_API_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=gemma2:2b
OLLAMA_TIMEOUT=180

# ntfy.sh Configuration
NTFY_TOPIC=gmail-summary
NTFY_BASE_URL=https://ntfy.sh

# Email Configuration
GMAIL_MAX_RESULTS=5
```

### Step 5: Run the Application

**First run** (sets up OAuth token):
```bash
python main.py
```

The script will:
1. Open a browser for Gmail authentication
2. Fetch your unread emails
3. Clean and combine them
4. Send to Ollama for summarization
5. Send summary via ntfy.sh
6. Display results in terminal

**Subsequent runs**:
Just run the same command - the cached token will be reused.

### Receiving Notifications

After running the script, you can receive notifications via:

**Option 1: Web Browser**
- Visit `https://ntfy.sh/gmail-summary`
- Notifications appear in real-time

**Option 2: Desktop Notifications (ntfy iOS/Android app)**
- Install the ntfy app
- Subscribe to topic: `gmail-summary`
- Notifications arrive as push alerts

**Option 3: Mobile App**
- Download ntfy app (iOS/Android)
- Search for topic: `gmail-summary`
- Get native push notifications

## Pipeline Overview

The application follows a 5-step pipeline:

```
[Step 1] Fetch unread emails
    ↓
[Step 2] Extract & clean email content
    ↓
[Step 3] Combine emails into single text
    ↓
[Step 4] Summarize with local LLM (Ollama)
    ↓
[Step 5] Send notification via ntfy.sh
```

### Step-by-Step Details

**Step 1: Fetch unread emails from Gmail**
- Queries Gmail API for unread messages
- Default: 5 emails (configurable)
- Returns sender, subject, and message ID

**Step 2: Extract and clean content**
- Converts HTML email to plain text
- Removes: URLs, tracking pixels, CSS, HTML entities
- Filters: footer text, "unsubscribe" links, metadata
- Result: Clean, readable email content

**Step 3: Combine emails**
- Merges all cleaned emails into single text block
- Format: `EMAIL 1: From: ... Subject: ... Body: ...`
- Clear separators between emails
- Logs statistics (character count, byte count)

**Step 4: Summarize with Ollama**
- Sends combined text to local Ollama instance
- Uses specified LLM model (default: gemma2:2b)
- Prompt ensures all emails are covered
- 180-second timeout for slow models
- Returns comprehensive summary

**Step 5: Send notification**
- Encodes summary as UTF-8
- Sanitizes title for HTTP headers
- Posts to ntfy.sh/{NTFY_TOPIC}
- Returns success/failure status

## Example Output

```
======================================================================
Gmail Notification Service - Starting...
======================================================================

[Step 1] Fetching unread emails from Gmail...
✓ Fetched 5 unread email(s)

[Step 2] Extracting and cleaning email content...
  [1] Project Update - Q1 Goals
  [2] Team Meeting Tomorrow
  [3] New Feature Request
  [4] Performance Report
  [5] Client Feedback
✓ Extracted 5 email(s)

[Step 3] Combining emails for processing...
Combined 5 emails: 3245 chars, 3521 bytes
Preview: EMAIL 1:
From: manager@company.com
Subject: Project Update - Q1 Goals
Body: ...

[Step 4] Generating summary with Ollama LLM...
Sending to Ollama:
  - Model: gemma2:2b
  - Prompt length: 4234 chars
Summary received (892 chars, 964 bytes)

[Step 5] Sending summary via ntfy.sh...
Sending notification to ntfy.sh/gmail-summary
  - Title: Gmail Summary (5 emails)
  - Size: 892 chars (964 bytes)
✓ Sent successfully (HTTP 200)

======================================================================
✓ Pipeline completed successfully!
======================================================================
```

## Testing & Debugging

### Use Jupyter Notebook

```bash
jupyter notebook test.ipynb
```

This provides interactive testing of:
- Gmail email fetching
- Email extraction and cleaning
- Email body preview (raw vs. cleaned)
- Text statistics

### Debug Output

The script includes detailed logging:
- Email counts at each stage
- Character and byte counts
- Preview text samples
- HTTP response codes
- Error messages with suggestions

## Troubleshooting

### "No unread emails found"
- Check Gmail for unread messages
- Ensure you have the `is:unread in:inbox` filter working

### "Ollama timeout"
- Ensure Ollama is running: `ollama serve`
- Try a faster model: `ollama pull mistral:latest`
- Increase timeout: `OLLAMA_TIMEOUT=300`

### "Cannot connect to Ollama"
- Start Ollama server: `ollama serve`
- Check if running on correct port: `http://localhost:11434`

### "Gmail authentication failed"
- Delete `token.json` and re-run
- Verify `credentials.json` is valid
- Check Gmail API is enabled in Google Cloud Console

### "Notification not received"
- Check ntfy.sh website: `https://ntfy.sh/gmail-summary`
- Verify NTFY_TOPIC is set correctly
- Check internet connection

## Privacy & Security

✓ **Emails stay local** - Never sent to external services (except ntfy.sh for notification)
✓ **No cloud LLM** - Uses your own Ollama instance on your machine
✓ **OAuth2 token** - Stored locally in `token.json`, only read permissions requested
✓ **Credentials file** - Kept locally, never uploaded
✓ **Token refresh** - Automatic, no manual intervention needed

## Performance

- Typical runtime: 10-30 seconds
- Ollama summarization: 5-20 seconds (depends on model)
- Gmail fetch: 1-2 seconds
- Notification delivery: <1 second
- Overall: Depends on Ollama model choice

### Model Recommendations

| Model | Speed | Quality | VRAM | Notes |
|-------|-------|---------|------|-------|
| `gemma2:2b` | Fast | Good | ~5GB | Default, balanced |
| `mistral` | Medium | Better | ~15GB | Better summaries |
| `neural-chat` | Medium | Very Good | ~15GB | Optimized for chat |
| `dolphin-mixtral` | Slower | Best | ~50GB+ | Highest quality |

## Future Enhancements

- [ ] Email scheduling (cron/systemd timer)
- [ ] Multiple topics/filters
- [ ] Custom summarization prompts
- [ ] Email archiving after processing
- [ ] Web dashboard for configuration
- [ ] Multi-language support
- [ ] Attachment processing

## License

MIT License - feel free to use and modify

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review error messages and logs
3. Test with `test.ipynb` for debugging
4. Check Ollama is running and accessible

---

**Happy emailing! 📧✨**
