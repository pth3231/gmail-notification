# Installation Guide

## Windows

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies (no compilation needed!)
pip install -r requirements.txt
```

## Linux / macOS

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Troubleshooting

### PEP 668 Error on Ubuntu/Debian

**Error:** `error: externally-managed-environment`

**Solution:** Use virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Alternative:** If you must use system Python:

```bash
pip install -r requirements.txt --break-system-packages
```

⚠️ Not recommended - can break your system package manager

### Module Not Found Errors

Make sure virtual environment is activated:

```bash
# Check if activated (should show (venv) in prompt)
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Permission Denied on Linux

Use virtual environment instead of `sudo pip`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### SSL Certificate Errors

```bash
pip install --upgrade certifi
pip install -r requirements.txt
```

### Note on lxml

This project uses BeautifulSoup4 with Python's built-in `html.parser` instead of lxml. This means:

- ✓ No compilation required (works on Windows without build tools)

- ✓ Faster installation

- ✓ All HTML parsing functionality included

## Development Setup

For development with Jupyter, linting, and type checking:

```bash
pip install -r requirements-dev.txt
```

Then start Jupyter:

```bash
jupyter notebook test.ipynb
```
