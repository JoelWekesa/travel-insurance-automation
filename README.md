# Travel Insurance Automation Test

Automated end-to-end testing for Old Mutual Kenya's Travel Insurance purchase flow using Playwright and Python, with Slack notifications for test results.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Test Flow](#test-flow)
- [Slack Notifications](#slack-notifications)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

This automated test script validates the complete travel insurance purchase journey on the Old Mutual Kenya platform. It simulates a real user purchasing travel insurance, from initial form filling through to payment processing, while capturing screenshots at each step and sending notifications to Slack.

**Test URL:** https://www.oldmutual.co.ke/app/public/travel-insurance

## Features

- Complete end-to-end automation of travel insurance purchase flow
- Full-page screenshots captured at each major step
- Real-time Slack notifications on test completion (pass/fail)
- Detailed failure reporting with exact step identification
- Test execution duration tracking
- Step-by-step progress tracking
- Error screenshots for debugging

## Prerequisites

Before running this test, ensure you have the following installed:

- **Python 3.7+**
- **pip** (Python package manager)
- **Slack workspace** (for notifications)

## Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd travel-insurance-automation
```

### 2. Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
```bash
playwright install chromium
```

## Configuration

### 1. Set Up Slack Webhook

**Option A: Use Existing Webhook (Quick)**

If you already have a Slack webhook URL, update it in the script:
```python
slack_webhook_url = 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
```

**Option B: Create New Webhook**

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Name your app (e.g., "Test Automation Bot") and select your workspace
4. Click **"Incoming Webhooks"** → Toggle **ON**
5. Click **"Add New Webhook to Workspace"**
6. Select the channel for notifications
7. Copy the webhook URL

### 2. Get Your Slack User ID (Optional - for mentions)

To get mentioned on test failures:

1. In Slack, click your profile picture
2. Click **Profile** → **More (⋯)** → **Copy member ID**
3. Update the script:
```python
MY_SLACK_USER_ID = "U01234567"  # Your actual User ID
```

### 3. Environment Variables (Optional)

Create a `.env` file in the project root:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_USER_ID=U01234567
```

Then add to your script:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Test Files

Ensure you have a test image file named `download.jpeg` in the project directory for document uploads.

## Usage

### Run the Test
```bash
python3 travel.py
```

### Run in Headless Mode

To run without opening a browser window, modify the script:
```python
browser = playwright.chromium.launch(headless=True)
```

### Schedule Automated Runs

**Using Cron (Linux/Mac):**
```bash
# Edit crontab
crontab -e

# Add this line to run every day at 9 AM
0 9 * * * cd /path/to/project && /path/to/venv/bin/python travel.py
```

**Using Task Scheduler (Windows):**

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 9 AM)
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `travel.py`
7. Start in: `C:\path\to\project`

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

Test Status: Passed ✓
Duration: 45.3 seconds
Environment: Production
URL: https://www.oldmutual.co.ke/app/public/travel-insurance
All Steps Completed:
  ✓ Step 1: Select Cover Type
  ✓ Step 2: Personal Information
  ✓ Step 3: Travel Details
  ✓ Step 4: Review & Proceed
  ✓ Step 5: Traveller Details
  ✓ Step 6: Beneficiary Details
  ✓ Step 7: Terms & Conditions
  ✓ Step 8: Payment Processing

Screenshot saved: success.png
```

### Failure Notification

When the test fails, you'll receive:
```
Travel Insurance Test Alert
@YourName (if configured)

Test Status: Failed ✗
Failed At: Step 5: Traveller Details & Documents
Duration: 23.1 seconds
Environment: Production
URL: https://www.oldmutual.co.ke/app/public/travel-insurance
Error Details:
Locator.fill: Error: Element is not visible

Screenshot saved: error.png
```

### Enable Mobile Notifications

1. Download Slack app on your phone (App Store/Play Store)
2. Sign in to your workspace
3. Open the notification channel
4. Tap the channel name → Bell icon (🔔)
5. Select **"All new messages"**

## 📸 Screenshots

The test captures screenshots at each major step:

- `1.png` - Initial page load
- `2.png` - Personal information filled
- `3.png` - Travel details filled
- `4.png` - Review page
- `5.png` - After clicking continue
- `6.png` - Before adding traveller details
- `7.png` - Traveller details with documents
- `8.png` - Beneficiary details
- `9.png` - Terms and conditions
- `success.png` - Final success screenshot
- `error.png` - Error screenshot (if test fails)

All screenshots are saved in the project root directory with `full_page=True` to capture the entire page.

## Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'playwright'`**
```bash
pip install playwright
playwright install chromium
```

**Issue: Slack notifications not being sent**

- Verify webhook URL is correct
- Check internet connectivity
- Test webhook manually:
```bash
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"Test message"}' \
YOUR_WEBHOOK_URL
```

**Issue: `Error: Element is not visible`**

- The page may be loading slowly
- Increase timeout values:
```python
page.wait_for_timeout(1000)  # Increase from 500
```

**Issue: File upload fails**

- Ensure `download.jpeg` exists in the project directory
- Check file permissions
- Verify file path is correct

**Issue: Selector not found**

- The website may have changed
- Use Playwright codegen to regenerate selectors:
```bash
playwright codegen https://www.oldmutual.co.ke/app/public/travel-insurance
```

**Issue: Test runs but no notifications on phone**

- Check Slack app notifications are enabled in phone settings
- Verify channel notification settings in Slack app
- Test by sending a manual message to the channel

### Debug Mode

To see detailed logs, add verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Test Results

Test results are communicated through:

1. **Console Output** - Real-time progress in terminal
2. **Slack Notifications** - Success/failure alerts
3. **Screenshots** - Visual evidence of each step
4. **Exit Code** - 0 for success, 1 for failure

## 🔒 Security Notes

- Never commit webhook URLs or tokens to version control
- Use environment variables for sensitive data
- Consider using `.gitignore` to exclude `.env` files
- Rotate Slack webhook URLs periodically
- Use private channels for sensitive notifications

## License

[Your License Here - e.g., MIT License]

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Contact

**Maintainer:** Joel Wekesa  
**Company:** Old Mutual East Africa  
**Team:** Digital & Data

For issues or questions, please contact [your-email@oldmutual.com]

## Acknowledgments

- Built with [Playwright](https://playwright.dev/)
- Notifications powered by [Slack](https://slack.com/)
- Test automation inspired by best practices in continuous testing

---

**Last Updated:** December 2025  
**Version:** 1.0.0