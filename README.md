# Gmail Notification Service

<img width="347" height="96" alt="image" src="https://github.com/user-attachments/assets/4afc949c-6219-44e8-8e25-907d0c7cdea6" />
<img width="386" height="96" alt="image" src="https://github.com/user-attachments/assets/23ed4057-742f-47bb-8066-c13dd6041d15" />

Fetch unread Gmail emails, summarize with local Ollama LLM, send via ntfy.sh.

**Features:** Privacy-first (local processing) • Cleans email content • Summarizes multiple emails • Push notifications

## Quick Start

1. **Install:** See [INSTALL.md](INSTALL.md)
2. **Ollama:** `ollama serve` & `ollama pull gemma2:2b`
3. **Gmail API:** Get credentials from [Google Cloud Console](https://console.cloud.google.com) → save as `credentials.json`
4. **Run:** `python main.py`
5. **Schedule:** See [INSTALL.md](INSTALL.md#scheduling) for 3-hour automation

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

- **Web:** [https://ntfy.sh/gmail-summary](https://ntfy.sh/gmail-summary)
- **Mobile:** Install ntfy app, subscribe to `gmail-summary`

## File Structure

| File | Purpose |
| ---- | ------- |
| `src/config.py` | Centralized configuration & constants |
| `src/pipeline.py` | Main pipeline orchestrator (EmailPipeline class) |
| `src/services/gmail.py` | Gmail API service (GmailService class) |
| `src/services/email.py` | Email processing service (EmailService class) |
| `src/services/llm.py` | LLM integration service (LLMService class) |
| `src/services/notification.py` | Notification service (NotificationService class) |
| `src/utils/cleaning.py` | HTML cleaning & sanitization utilities |
| `main.py` | Entry point (simplified, uses EmailPipeline) |

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

See [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) for architectural details.

## License

MIT

---

**Happy emailing! 📧✨**
