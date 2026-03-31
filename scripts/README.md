# Quick Start - Run Every 3 Hours

## Windows Users

1. **Open PowerShell as Administrator**
   - Right-click PowerShell → "Run as Administrator"

2. **Navigate to scripts directory:**
   ```powershell
   cd D:\Code\gmail-notification\scripts
   ```

3. **Run the setup script:**
   ```powershell
   .\run_every_3h.bat
   ```

4. **Verify in Task Scheduler:**
   - Press `Win + R`, type `taskschd.msc`
   - Look for "GmailNotification3Hour"
   - Should be "Enabled"

---

## Linux / macOS Users

1. **Make script executable:**
   ```bash
   chmod +x scripts/run_every_3h.sh
   ```

2. **Run the setup script:**
   ```bash
   ./scripts/run_every_3h.sh
   ```

3. **Verify cron job:**
   ```bash
   crontab -l
   ```
   Should show:
   ```
   0 */3 * * * cd /path/to/gmail-notification && python3 main.py
   ```

---

## Schedule

Both Windows Task Scheduler and Linux cron run at:
- **00:00** (midnight)
- **03:00** (3 AM)
- **06:00** (6 AM)
- **09:00** (9 AM)
- **12:00** (noon)
- **15:00** (3 PM)
- **18:00** (6 PM)
- **21:00** (9 PM)

---

## Monitor Execution

**Windows:** Open Task Scheduler → Right-click task → View Event History

**Linux/macOS:** Check logs:
```bash
tail -f logs/run_every_3h_*.log
```

---

## Test Manually

```bash
python main.py
```

Should exit with code 0 if successful.

---

## Troubleshoot

**Task not running?**
- Windows: Verify running as Administrator, check Task Scheduler History
- Linux: Check `crontab -l`, verify Python path with `which python3`

**Notifications not received?**
- Check Ollama is running: `curl http://localhost:11434/api/tags`
- Check ntfy.sh: Go to `https://ntfy.sh/gmail-summary`

**Python not found?**
- Windows: Edit `.bat` with full Python path
- Linux: Use `/usr/bin/python3` instead of `python3`

---

For detailed information, see [SCHEDULING.md](SCHEDULING.md)
