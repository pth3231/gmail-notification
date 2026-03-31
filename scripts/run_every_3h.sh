#!/bin/bash
# Run the Gmail Notification Service every 3 hours (Linux/macOS)
# Usage: chmod +x run_every_3h.sh && ./run_every_3h.sh

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN=$(which python3 || which python)
LOG_DIR="$PROJECT_DIR/logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Get current timestamp for log file
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="$LOG_DIR/run_every_3h_$TIMESTAMP.log"

echo "=========================================="
echo "Gmail Notification Service - Cron Setup"
echo "=========================================="
echo ""
echo "Project Directory: $PROJECT_DIR"
echo "Python Binary: $PYTHON_BIN"
echo "Log Directory: $LOG_DIR"
echo ""

# Function to run the main script with logging
run_gmail_service() {
    {
        echo ""
        echo "=========================================="
        echo "Execution Time: $(date)"
        echo "=========================================="
        cd "$PROJECT_DIR"
        $PYTHON_BIN main.py
        echo "Exit code: $?"
        echo ""
    } >> "$LOG_FILE" 2>&1
}

# Add to crontab
# Cron expression for every 3 hours: 0 */3 * * *
# This runs at 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00

CRON_EXPRESSION="0 */3 * * * cd $PROJECT_DIR && $PYTHON_BIN main.py >> $LOG_FILE 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "GmailNotification"; then
    echo "Cron job already exists. Updating..."
    (crontab -l 2>/dev/null | grep -v "GmailNotification"; echo "# GmailNotification - Every 3 hours") | crontab -
else
    echo "Adding new cron job..."
    (crontab -l 2>/dev/null; echo "# GmailNotification - Every 3 hours"; echo "$CRON_EXPRESSION") | crontab -
fi

echo ""
echo "=========================================="
echo "SUCCESS: Cron job configured!"
echo "=========================================="
echo ""
echo "Cron Expression:"
echo "  $CRON_EXPRESSION"
echo ""
echo "The script will run at:"
echo "  00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00 daily"
echo ""
echo "View scheduled jobs:"
echo "  crontab -l"
echo ""
echo "View logs:"
echo "  tail -f $LOG_FILE"
echo ""
