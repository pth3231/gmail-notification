# Gmail Notification Service

Fetch unread Gmail emails, summarize with local Ollama LLM, send via ntfy.sh.

**Features:** Privacy-first (local processing) • Cleans email content • Summarizes multiple emails • Push notifications

## Quick Start

1. **Install:** `pip install -r requirements.txt`
2. **Ollama:** `ollama serve` & `ollama pull gemma2:2b`
3. **Gmail API:** Get credentials from [Google Cloud Console](https://console.cloud.google.com) → save as `credentials.json`
4. **Run:** `python main.py`

**For development:** `pip install -r requirements-dev.txt` (adds Jupyter, linting, type checking)

## Pipeline

1. Fetch unread emails from Gmail
2. Extract & clean content (remove HTML, URLs, tracking pixels, CSS)
3. Combine emails into single text
4. Summarize with Ollama LLM
5. Send via ntfy.sh

## Configuration (Optional)

Set environment variables:
```bash
OLLAMA_API_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=gemma2:2b
OLLAMA_TIMEOUT=180
NTFY_TOPIC=gmail-summary
NTFY_BASE_URL=https://ntfy.sh
```

## Receive Notifications

- **Web:** https://ntfy.sh/gmail-summary
- **Mobile:** Install ntfy app, subscribe to `gmail-summary`

## File Structure

| File | Purpose |
|------|--------|
| `main.py` | Pipeline orchestrator |
| `gmail_service.py` | Gmail API & authentication |
| `email_processor.py` | Extract & clean content |
| `cleaning.py` | Remove URLs, CSS, tracking pixels |
| `ollama_service.py` | Ollama LLM summarization |
| `ntfy_service.py` | ntfy.sh notifications |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No emails found | Check Gmail for unread messages |
| Ollama timeout | Start: `ollama serve`, try faster model, increase `OLLAMA_TIMEOUT` |
| Can't connect Ollama | Start Ollama on port 11434 |
| Gmail auth failed | Delete `token.json` and re-run |
| No notifications | Check `https://ntfy.sh/gmail-summary` |

## Performance

- Runtime: 10-30 seconds (depends on Ollama model)
- Recommended: `gemma2:2b` (fast, ~5GB RAM) or `mistral` (better quality, ~15GB RAM)

## Code Quality

✓ Type hints throughout
✓ Comprehensive docstrings
✓ Clear error messages  
✓ Refactored for maintainability

## License

MIT

---

**Happy emailing! 📧✨**
