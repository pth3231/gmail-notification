# Scheduling Guide - Run Every 3 Hours

This guide explains how to automatically run the Gmail Notification Service every 3 hours on different operating systems.

## Windows (Task Scheduler)

### Quick Setup

1. **Open PowerShell as Administrator**
   - Right-click PowerShell → "Run as Administrator"

2. **Run the setup script:**
   ```powershell
   cd D:\Code\gmail-notification
   .\scripts\run_every_3h.bat
   ```

3. **Verify the task was created:**
   - Open "Task Scheduler" (Win + R, type `taskschd.msc`)
   - Look for "GmailNotification3Hour" in the task list
   - It should show "Enabled" status

### Manual Setup

If the script doesn't work, create the task manually:

```powershell
schtasks /Create `
  /SC HOURLY `
  /MO 3 `
  /TN "GmailNotification3Hour" `
  /TR "C:\Python312\python.exe D:\Code\gmail-notification\main.py" `
  /ST 00:00 `
  /F
```

Replace paths with your actual Python path and project directory.

### Run Times

The task will execute at:
- **00:00** (midnight)
- **03:00** (3 AM)
- **06:00** (6 AM)
- **09:00** (9 AM)
- **12:00** (noon)
- **15:00** (3 PM)
- **18:00** (6 PM)
- **21:00** (9 PM)

### Verify It's Working

1. **View in Task Scheduler:**
   - Right-click task → Properties
   - Check "Triggers" tab for 3-hour interval
   - Check "Actions" tab for correct Python command

2. **Check task history:**
   - In Task Scheduler, click "Event Viewer" (bottom right)
   - Look for recent executions
   - Success = "Task started"

3. **Manual test:**
   ```powershell
   cd D:\Code\gmail-notification
   python main.py
   ```

### Disable or Remove

```powershell
# Disable the task
schtasks /Change /TN "GmailNotification3Hour" /DISABLE

# Delete the task
schtasks /Delete /TN "GmailNotification3Hour" /F
```

---

## Linux / macOS (Cron)

### Quick Setup

1. **Make the script executable:**
   ```bash
   chmod +x scripts/run_every_3h.sh
   ```

2. **Run the setup script:**
   ```bash
   ./scripts/run_every_3h.sh
   ```

3. **Verify the cron job:**
   ```bash
   crontab -l
   ```
   You should see a line like:
   ```
   0 */3 * * * cd /path/to/gmail-notification && python3 main.py
   ```

### Manual Setup

Edit your crontab:

```bash
crontab -e
```

Add this line:

```bash
0 */3 * * * cd /home/user/gmail-notification && python3 main.py >> /home/user/gmail-notification/logs/cron.log 2>&1
```

Replace `/home/user/gmail-notification` with your actual project path.

### Run Times

The cron expression `0 */3 * * *` runs at:
- **00:00** (midnight)
- **03:00** (3 AM)
- **06:00** (6 AM)
- **09:00** (9 AM)
- **12:00** (noon)
- **15:00** (3 PM)
- **18:00** (6 PM)
- **21:00** (9 PM)

### Verify It's Working

1. **Check cron logs:**
   ```bash
   # macOS
   log stream --predicate 'process == "cron"' --level debug
   
   # Linux (varies by distro)
   sudo tail -f /var/log/syslog | grep CRON
   sudo tail -f /var/log/cron
   ```

2. **Check application logs:**
   ```bash
   tail -f logs/run_every_3h_*.log
   ```

3. **Manual test:**
   ```bash
   cd /path/to/gmail-notification
   python3 main.py
   ```

### Disable or Remove

```bash
# Edit crontab and remove the line
crontab -e

# Or remove all cron jobs
crontab -r
```

### Troubleshooting

**Cron not running:**
- Ensure virtualenv is activated in cron command
- Use full paths to Python and scripts
- Check cron logs for errors
- Add logging to capture output

**Permissions:**
- Make sure script is executable: `chmod +x scripts/run_every_3h.sh`
- Ensure log directory exists: `mkdir -p logs`

**Python not found:**
- Use full path to Python: `/usr/bin/python3`
- Or activate virtualenv in cron: `source venv/bin/activate`

---

## Systemd Timer (Linux Alternative)

For modern Linux systems, you can use systemd timers instead of cron:

### Create service file

`~/.config/systemd/user/gmail-notification.service`

```ini
[Unit]
Description=Gmail Notification Service
After=network.target

[Service]
Type=oneshot
WorkingDirectory=/home/user/gmail-notification
ExecStart=/usr/bin/python3 /home/user/gmail-notification/main.py
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

### Create timer file

`~/.config/systemd/user/gmail-notification.timer`

```ini
[Unit]
Description=Run Gmail Notification Service every 3 hours
Requires=gmail-notification.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=3h
Unit=gmail-notification.service
Persistent=true

[Install]
WantedBy=timers.target
```

### Enable and start

```bash
systemctl --user daemon-reload
systemctl --user enable gmail-notification.timer
systemctl --user start gmail-notification.timer
```

### Check status

```bash
systemctl --user status gmail-notification.timer
systemctl --user list-timers
journalctl --user -u gmail-notification.service -f
```

---

## Environment Variables

If using environment variables (`.env`), make sure they're set before running:

### Windows (Task Scheduler)

Set in the task's "Actions" tab:

```
cmd /c cd D:\Code\gmail-notification && set OLLAMA_MODEL=gemma2:2b && python main.py
```

### Linux/macOS (Cron)

Add to crontab:

```bash
0 */3 * * * export OLLAMA_MODEL=gemma2:2b && cd /path/to/gmail-notification && python3 main.py
```

---

## Monitoring

### Check Recent Executions

**Windows:**
```powershell
Get-ScheduledTaskInfo "GmailNotification3Hour" | Select-Object LastRunTime, LastTaskResult
```

**Linux/macOS:**
```bash
grep CRON /var/log/syslog | tail -10
tail -f logs/run_every_3h_*.log
```

### Receive Notifications

Go to: `https://ntfy.sh/gmail-summary`

Or subscribe in the ntfy app to see all notifications sent.

---

## Troubleshooting

### Task not running

**Windows:**
1. Check Task Scheduler History
2. Verify Python path is correct
3. Ensure token.json and credentials.json exist
4. Run manually to test

**Linux/macOS:**
1. Check cron logs
2. Verify Python path and project directory
3. Check file permissions
4. Test manually first

### Notifications not received

- Check if Ollama is running
- Verify ntfy.sh connectivity
- Check application logs for errors
- Manually run `python main.py` to diagnose

### Python not found

Use full path to Python:
- Windows: `C:\Python312\python.exe` (adjust version)
- Linux/macOS: `/usr/bin/python3`

### Wrong working directory

Always use `cd /path/to/project` before running Python to ensure relative paths work correctly.
