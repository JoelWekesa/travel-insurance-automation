# Travel Insurance Automation Test

Automated end-to-end testing for Old Mutual Kenya's Travel Insurance purchase flow using Playwright and Python, with Slack notifications for test results. Runs automatically every schedule period in a Docker container.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Docker Installation (Recommended)](#docker-installation-recommended)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Local Usage](#local-usage)
  - [Docker Usage](#docker-usage)
- [Test Flow](#test-flow)
- [Slack Notifications](#slack-notifications)
- [Screenshots](#screenshots)
- [Monitoring](#monitoring)
  - [Viewing Logs](#viewing-logs)
  - [Container Health](#container-health)
  - [Screenshot Management](#screenshot-management)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [Contributing](#contributing)

## Overview

This automated test script validates the complete travel insurance purchase journey on the Old Mutual Kenya platform. It simulates a real user purchasing travel insurance, from initial form filling through to payment processing, while capturing screenshots at each step and sending notifications to Slack.

The application runs in a Docker container and automatically executes tests:
- **Immediately on startup**
- **Every 1 hour thereafter**

**Test URL:** https://www.oldmutual.co.ke/app/public/travel-insurance

## Features

- **Automated Testing**: Complete end-to-end automation of travel insurance purchase flow
- **Screenshot Capture**: Full-page screenshots with timestamps at each major step
- **Real-time Alerts**: Slack notifications on test completion (pass/fail)
- **Failure Detection**: Detailed failure reporting with exact step identification
- **Performance Tracking**: Test execution duration tracking
- **Docker Deployment**: Containerized application for easy deployment
- **Continuous Monitoring**: Tests run every schedule period automatically
- **Persistent Storage**: Screenshots and logs persist across container restarts

## Prerequisites

### For Local Development:
- **Python 3.7+**
- **pip** (Python package manager)
- **Slack workspace** (for notifications)

### For Docker Deployment (Recommended):
- **Docker** (20.10+)
- **Docker Compose** (1.29+)
- **Slack workspace** (for notifications)

## Installation

### Local Installation

#### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd travel-insurance-automation
```

#### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install Playwright Browsers
```bash
playwright install chromium
```

---

### Docker Installation (Recommended)

#### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd travel-insurance-automation
```

#### 2. Configure Environment Variables
Copy the example environment file and configure:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
ENVIRONMENT=production
HEADLESS_MODE=true
```

#### 3. Build and Run
```bash
# Build and start the container
docker-compose up -d --build

# View logs
docker-compose logs -f
```

That's it! The tests will start running immediately and then every 1 hour.

## Configuration

### 1. Set Up Slack Webhook

**Create New Webhook:**

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Name your app (e.g., "Test Automation Bot") and select your workspace
4. Click **"Incoming Webhooks"** → Toggle **ON**
5. Click **"Add New Webhook to Workspace"**
6. Select the channel for notifications (e.g., `#automation-tests`)
7. Copy the webhook URL

**Update Configuration:**

- **For Docker**: Update `.env` file
- **For Local**: Update `.env` file or the script directly

### 2. Environment Variables

Create a `.env` file with the following variables:
```env
# Required
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Optional (defaults shown)
ENVIRONMENT=production
HEADLESS_MODE=true
```

**Important:** Never commit your `.env` file to version control. Use `.env.example` as a template.

### 3. Test Files

Ensure you have a test image file named `download.jpeg` in the project directory for document uploads.

## Usage

### Local Usage

#### Run Single Test
```bash
python test_runner.py
```

#### Run with Scheduler
```bash
python scheduler.py
```

This will:
- Run test immediately
- Schedule tests every 1 hour
- Keep running until stopped (Ctrl+C)

---

### Docker Usage

#### Start the Container
```bash
docker-compose up -d
```

#### View Live Logs
```bash
docker-compose logs -f
```

#### Check Container Status
```bash
docker-compose ps
```

#### Stop the Container
```bash
docker-compose down
```

#### Restart After Changes
```bash
docker-compose down
docker-compose up -d --build
```

#### Access Container Shell
```bash
docker exec -it travel-insurance-test /bin/bash
```

#### View Screenshots
```bash
# From host machine
ls -lh screenshots/

# From container
docker exec travel-insurance-test ls -lh /app/screenshots/
```

## Test Flow

The test executes the following steps:

### Step 1: Select Cover Type
- Navigate to travel insurance page
- Select "Retail" cover option

### Step 2: Personal Information
- Fill in name, phone, and email
- Continue to next step

### Step 3: Travel Details
- Select single trip option
- Enter number of travellers (20)
- Select destination country
- Enter departure date (5 days from now)
- Enter return date (6 days from now)

### Step 4: Review & Proceed
- Review travel details
- Click "Proceed to buy"

### Step 5: Traveller Details & Documents
- Add traveller details
- Select title (Mr/Mrs/Ms)
- Select gender
- Enter date of birth
- Enter ID number
- Enter passport number
- Enter KRA PIN
- Upload ID document
- Upload KRA document
- Upload passport document

### Step 6: Beneficiary Details
- Enter beneficiary name
- Enter beneficiary phone
- Enter beneficiary email

### Step 7: Terms & Conditions
- Accept consent for products and services
- Accept terms and conditions

### Step 8: Payment Processing
- Click "Process Payment"
- Test completes successfully

## Slack Notifications

### Success Notification

When the test passes, you'll receive:
```
Travel Insurance Test Alert

Test Status: Passed
Duration: 45.3 seconds
Environment: Production
URL: https://www.oldmutual.co.ke/app/public/travel-insurance
All Steps Completed:
  Step 1: Select Cover Type
  Step 2: Personal Information
  Step 3: Travel Details
  Step 4: Review & Proceed
  Step 5: Traveller Details
  Step 6: Beneficiary Details
  Step 7: Terms & Conditions
  Step 8: Payment Processing

Screenshots saved in: screenshots/
```

### Failure Notification

When the test fails, you'll receive:
```
Travel Insurance Test Alert

Test Status: Failed
Failed At: Step 5: Traveller Details & Documents
Duration: 23.1 seconds
Environment: Production
URL: https://www.oldmutual.co.ke/app/public/travel-insurance
Error Details:
Locator.fill: Error: Element is not visible

Error screenshot: screenshots/20251208_031045_error.png
```

### Enable Mobile Notifications

1. Download Slack app on your phone (App Store/Play Store)
2. Sign in to your workspace
3. Open the notification channel
4. Tap the channel name and then the bell icon
5. Select **"All new messages"**

Now you'll receive push notifications on your phone for every test result!

## Screenshots

The test captures timestamped screenshots at each major step:

### Screenshot Naming Convention
All screenshots are saved with timestamps in the format: `YYYYMMDD_HHMMSS_<step>.png`

**Examples:**
- `20251208_093045_1.png` - Initial page load
- `20251208_093046_2.png` - Personal information filled
- `20251208_093047_3.png` - Travel details filled
- `20251208_093048_4.png` - Review page
- `20251208_093049_5.png` - After clicking continue
- `20251208_093050_6.png` - Before adding traveller details
- `20251208_093051_7.png` - Traveller details with documents
- `20251208_093052_8.png` - Beneficiary details
- `20251208_093053_9.png` - Terms and conditions
- `20251208_093054_success.png` - Final success screenshot
- `20251208_093054_error.png` - Error screenshot (if test fails)

All screenshots are saved in the `screenshots/` directory with `full_page=True` to capture the entire page.

### Screenshot Storage

- **Docker**: Screenshots persist in `./screenshots/` on the host machine
- **Local**: Screenshots saved in `./screenshots/` in the project directory

## Monitoring

### Viewing Logs

#### Container Logs (Real-time)

View live container logs as tests run:
```bash
# Follow container logs in real-time
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100

# View logs from last hour
docker-compose logs --since 1h

# View logs from last 5 minutes
docker-compose logs --since 5m
```

#### Scheduler Log File

The scheduler writes detailed logs to `logs/scheduler.log`. View them using:

**From Host Machine:**
```bash
# View entire log file
cat logs/scheduler.log

# View last 50 lines
tail -50 logs/scheduler.log

# Follow log file in real-time
tail -f logs/scheduler.log
```

**From Container:**
```bash
# View entire log file
docker exec travel-insurance-test cat logs/scheduler.log

# View last 50 lines
docker exec travel-insurance-test tail -50 logs/scheduler.log

# Follow log file in real-time
docker exec travel-insurance-test tail -f logs/scheduler.log
```

#### Search Logs

Find specific information in logs:
```bash
# Search for errors
docker-compose logs | grep "ERROR"

# Search for test failures
docker-compose logs | grep "Failed"

# Search for test successes
docker-compose logs | grep "completed successfully"

# Search for specific step
docker-compose logs | grep "Step 5"

# Count test runs
docker exec travel-insurance-test grep "Starting scheduled test" logs/scheduler.log | wc -l

# Count successful tests
docker exec travel-insurance-test grep "Test completed successfully" logs/scheduler.log | wc -l

# Count failed tests
docker exec travel-insurance-test grep "Test failed" logs/scheduler.log | wc -l
```

#### Copy Logs to Local Machine
```bash
# Copy log file from container to current directory
docker cp travel-insurance-test:/app/logs/scheduler.log ./scheduler.log
```

#### View Logs with Timestamps
```bash
# Container logs with timestamps
docker-compose logs -f -t

# Specific time range
docker-compose logs --since "2025-12-08T03:00:00" --until "2025-12-08T04:00:00"
```

### Container Health

Check container status and resource usage:
```bash
# Container status
docker-compose ps

# Resource usage (CPU, Memory, Network)
docker stats travel-insurance-test

# Detailed container information
docker inspect travel-insurance-test

# Check if process is running
docker exec travel-insurance-test ps aux | grep scheduler
```

### Screenshot Management

Manage screenshot storage:
```bash
# List all screenshots
ls -lh screenshots/ | tail -20

# Count total screenshots
ls screenshots/ | wc -l

# View most recent screenshots
ls -lht screenshots/ | head -10

# Find screenshots from today
find screenshots/ -name "*.png" -mtime 0

# Delete old screenshots (older than 7 days)
find screenshots/ -name "*.png" -mtime +7 -delete

# Check disk usage
du -sh screenshots/
```

## Troubleshooting

### Docker Issues

**Issue: Container keeps restarting**
```bash
# Check logs for errors
docker-compose logs --tail=50

# Check container status
docker-compose ps

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Issue: Playwright browser not found**
```bash
# Rebuild the container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Issue: Permission denied on screenshots/logs**
```bash
# Fix permissions on host
sudo chown -R $USER:$USER screenshots/ logs/
```

**Issue: Container running but no tests executing**
```bash
# Check scheduler logs
docker exec travel-insurance-test cat logs/scheduler.log

# Check if process is running
docker exec travel-insurance-test ps aux

# Check recent container logs
docker-compose logs --tail=100
```

**Issue: Environment variables not loading**
```bash
# Verify .env file exists
ls -la .env

# Check environment variables in container
docker exec travel-insurance-test env | grep -E "SLACK|HEADLESS|ENVIRONMENT"

# Restart after .env changes
docker-compose down
docker-compose up -d
```

### Common Test Issues

**Issue: `ModuleNotFoundError`**
```bash
# For local installation
pip install -r requirements.txt

# For Docker
docker-compose build --no-cache
```

**Issue: Slack notifications not being sent**

- Verify webhook URL is correct in `.env` file
- Check internet connectivity
- Test webhook manually:
```bash
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"Test message"}' \
YOUR_WEBHOOK_URL
```

**Issue: `Error: Element is not visible`**

- The page may be loading slowly
- Check the error screenshot in `screenshots/` folder
- Review logs: `docker exec travel-insurance-test cat logs/scheduler.log`
- Increase timeout values in `test_runner.py` if needed

**Issue: File upload fails**

- Ensure `download.jpeg` exists in the project directory
- Verify file is copied to container: `docker exec travel-insurance-test ls -l download.jpeg`
- Check Dockerfile includes: `COPY download.jpeg .`

**Issue: Test runs but no notifications on phone**

- Check Slack app notifications are enabled in phone settings
- Verify channel notification settings in Slack app
- Send a manual message to test notifications
- Check container logs: `docker-compose logs | grep "Slack notification"`

### Debug Mode

Enable verbose logging:

**For Docker:**
Add to your `.env` file:
```env
DEBUG=true
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

**For Local:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Architecture

### Project Structure
```
travel-insurance-automation/
├── test_runner.py            # Main test script
├── scheduler.py              # Scheduler for automated runs
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── .env                     # Environment variables (gitignored)
├── .env.example            # Environment template (committed)
├── .dockerignore           # Docker ignore file
├── .gitignore              # Git ignore file
├── download.jpeg           # Test upload file
├── screenshots/            # Screenshots directory (persisted)
├── logs/                   # Application logs (persisted)
└── README.md              # This file
```

### How It Works

1. **Container Starts**: Docker container initializes
2. **Scheduler Starts**: Python scheduler begins
3. **Initial Test**: Test runs immediately on startup
4. **Scheduled Tests**: Test runs every 1 hour
5. **Screenshot Capture**: Full-page screenshots saved with timestamps
6. **Slack Notification**: Alert sent on completion (pass/fail)
7. **Logging**: All activity logged to console and log file
8. **Persistence**: Screenshots and logs persist on host machine
9. **Auto-restart**: Container restarts automatically on failure or reboot

### Monitoring Strategy

This automation provides **Layer 3: Synthetic Monitoring** in your observability stack:
```
┌─────────────────────────────────────────┐
│  Layer 1: Infrastructure Monitoring     │  AWS CloudWatch, server metrics
├─────────────────────────────────────────┤
│  Layer 2: Application Monitoring        │  APM tools (Dynatrace, New Relic)
├─────────────────────────────────────────┤
│  Layer 3: Synthetic Monitoring          │  THIS AUTOMATION
├─────────────────────────────────────────┤
│  Layer 4: Real User Monitoring (RUM)    │  Analytics, user sessions
└─────────────────────────────────────────┘
```

**Benefits:**
- Detect issues before customers do
- Validate actual user experience
- Track uptime and performance
- Alert team immediately on failures
- Provide visual proof of issues

## Deployment

### Production Server Deployment
```bash
# SSH into your server
ssh user@your-server.com

# Clone repository
git clone <your-repo-url>
cd travel-insurance-automation

# Copy environment template and configure
cp .env.example .env
nano .env
# Add your SLACK_WEBHOOK_URL and other settings

# Start the container
docker-compose up -d --build

# Verify it's running
docker-compose ps
docker-compose logs -f

# The container will auto-restart on:
#   - Container crash
#   - Docker daemon restart
#   - Server reboot
```

### Update Deployment
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build

# Check logs
docker-compose logs -f
```

### Environment Setup for Team Members
```bash
# 1. Clone repository
git clone <your-repo-url>
cd travel-insurance-automation

# 2. Create environment file from template
cp .env.example .env

# 3. Edit .env and add your Slack webhook URL
nano .env

# 4. Build and run
docker-compose up -d --build

# 5. View logs
docker-compose logs -f
```

## Security Notes

- Never commit webhook URLs or tokens to version control
- Use environment variables for sensitive data
- The `.env` file is gitignored for security
- Use `.env.example` as a template for team members
- Rotate Slack webhook URLs periodically
- Use private channels for sensitive notifications
- Container runs as non-root user for security
- Review logs regularly and delete old screenshots containing sensitive data

## Performance Metrics

### Expected Results

- **Test Duration**: 40-60 seconds per run
- **Tests Per Hour**: 1
- **Tests Per Day**: 288
- **Tests Per Month**: Approximately 8,640

### Resource Usage

- **CPU**: 5-10% during test execution
- **Memory**: 200-300MB
- **Disk**: Approximately 1GB for 1 month of screenshots (can be cleaned periodically)
- **Network**: Minimal (Playwright + Slack webhook calls)

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone <your-fork-url>
cd travel-insurance-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run tests locally
python test_runner.py
```

## Support

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [Viewing Logs](#viewing-logs) for debugging
3. Check screenshot evidence in `screenshots/` folder
4. Review scheduler logs in `logs/scheduler.log`
5. Contact the team

## Contact

**Maintainer:** Joel Wekesa  
**Company:** Old Mutual East Africa  
**Team:** Digital & Data

For issues or questions, please contact [your-email@oldmutual.com]

## Acknowledgments

- Built with [Playwright](https://playwright.dev/)
- Notifications powered by [Slack](https://slack.com/)
- Containerized with [Docker](https://www.docker.com/)
- Scheduled with [schedule](https://github.com/dbader/schedule)
- Test automation inspired by best practices in continuous testing

---

**Last Updated:** December 2025  
**Version:** 2.0.0  
**Status:** Production Ready