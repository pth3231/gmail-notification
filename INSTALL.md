# Installation & Scheduling Guide

## Installation

### Windows

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Linux / macOS

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Troubleshooting

**PEP 668 Error on Ubuntu/Debian:**
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Module Not Found:**
```bash
# Verify virtualenv is activated (should show (venv) in prompt)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

**Permission Denied (Linux):**
```bash
# Use virtualenv instead of sudo pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**SSL Certificate Errors:**
```bash
pip install --upgrade certifi
pip install -r requirements.txt
```

### Development Setup

```bash
pip install -r requirements-dev.txt  # Adds Jupyter, linting, type checking
```

### Note on Dependencies

This project uses BeautifulSoup4 with Python's built-in `html.parser` (no external compiler needed):
- ✓ Works on Windows without build tools
- ✓ Faster installation than lxml
- ✓ All HTML parsing functionality included

---

## Scheduling

### Windows (Task Scheduler)

**Quick setup:**
1. Open PowerShell as Administrator
2. Run: `.\scripts\run_every_3h.bat`
3. Verify: Open Task Scheduler (`Win+R` → `taskschd.msc`)

**Manual setup:**
```powershell
schtasks /Create /SC HOURLY /MO 3 /TN "GmailNotification3Hour" /TR "C:\Python312\python.exe D:\Code\gmail-notification\main.py" /ST 00:00 /F
```

**Disable/Remove:**
```powershell
schtasks /Change /TN "GmailNotification3Hour" /DISABLE
schtasks /Delete /TN "GmailNotification3Hour" /F
```

### Linux / macOS (Cron)

**Quick setup:**
1. Run: `chmod +x scripts/run_every_3h.sh`
2. Run: `./scripts/run_every_3h.sh`
3. Verify: `crontab -l`

**Manual setup:**
```bash
crontab -e
# Add: 0 */3 * * * cd /path/to/gmail-notification && python3 main.py >> logs/run.log 2>&1
```

**Monitor/Disable:**
```bash
tail -f logs/run_every_3h_*.log    # Monitor execution
crontab -e                         # Edit and remove the line to disable
```

### Run Times

Both Windows and Linux/macOS run at:
- 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00

---

## Testing

Run manually to test:
```bash
python main.py
```

Check notifications at: [https://ntfy.sh/gmail-summary](https://ntfy.sh/gmail-summary)
