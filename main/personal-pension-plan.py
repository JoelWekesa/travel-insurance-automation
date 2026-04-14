import re
from datetime import datetime, timedelta
from playwright.sync_api import Playwright, sync_playwright, expect
import requests
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL") or ''

# Create screenshots directory if it doesn't exist
SCREENSHOTS_DIR = "screenshots"
if not os.path.exists(SCREENSHOTS_DIR):
    os.makedirs(SCREENSHOTS_DIR)

def get_screenshot_path(filename):
    """Generate screenshot path with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(SCREENSHOTS_DIR, f"{timestamp}_{filename}")


def send_slack_notification(message):
    """Send simple Slack notification via webhook"""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL") or slack_webhook_url
    
    try:
        emoji = "[OK]" if "Passed" in message else "[X]"
        
        payload = {
            "text": f"{emoji} *Personal Pension Plan Test*",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} Personal Pension Plan Test Alert"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Timestamp:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 200:
            print("[OK] Slack notification sent successfully!")
        else:
            print(f"[X] Failed to send Slack notification: {response.status_code}")
        
    except Exception as e:
        print(f"[X] Error sending Slack notification: {str(e)}")


def get_failure_step(error_message):
    """Determine which step failed based on error message"""
    error_lower = error_message.lower()
    
    if "select plan" in error_lower or "pension" in error_lower:
        return "Step 1: Select Pension Plan"
    elif "fullname" in error_lower or "phone" in error_lower or "email" in error_lower:
        return "Step 2: Personal Information"
    elif "contribution" in error_lower or "amount" in error_lower or "frequency" in error_lower:
        return "Step 3: Contribution Details"
    elif "beneficiary" in error_lower:
        return "Step 4: Beneficiary Details"
    elif "upload" in error_lower or "document" in error_lower or "id" in error_lower or "kra" in error_lower:
        return "Step 5: Document Upload"
    elif "consent" in error_lower or "terms" in error_lower:
        return "Step 6: Terms & Conditions"
    elif "process payment" in error_lower or "m-pesa" in error_lower:
        return "Step 7: Payment Processing"
    else:
        return "Unknown Step"


def run(playwright: Playwright) -> None:
    # Get headless mode from environment variable
    headless = os.getenv("HEADLESS_MODE", "true").lower() == "true"
    
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()
    
    start_time = datetime.now()
    current_step = ""
    
    try:
        # Step 1: Navigate and select pension plan
        current_step = "Step 1: Select Pension Plan"
        print(f"{current_step}")
        page.goto("https://www.oldmutual.co.ke/app/public/personal-pension-plan")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(300)
        page.screenshot(path=get_screenshot_path("1.png"), full_page=True)
        
        # Assuming there's a select button for personal pension plan
        page.get_by_role("button", name="Select Plan").click()
        page.wait_for_timeout(500)
        
        # Step 2: Fill personal details
        current_step = "Step 2: Personal Information"
        print(f"{current_step}")
        page.get_by_role("textbox", name="Fullname").fill("Test User")
        page.get_by_role("textbox", name="Phone").fill("0712345678")
        page.get_by_role("textbox", name="Email").fill("test@user.com")
        
        try:
            page.get_by_role("button", name="Close tooltip").click(timeout=2000)
        except:
            pass
        
        page.wait_for_timeout(300)
        page.screenshot(path=get_screenshot_path("2.png"), full_page=True)
        
        page.get_by_role("button", name="Continue").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(500)
        
        # Step 3: Fill contribution details
        current_step = "Step 3: Contribution Details"
        print(f"{current_step}")
        # Assuming contribution amount and frequency selection
        page.get_by_role("spinbutton", name="Contribution Amount").fill("50000")
        page.wait_for_timeout(200)
        
        # Select frequency (monthly, quarterly, etc.)
        page.locator("omk-select").filter(has_text="Frequency").click()
        page.wait_for_timeout(500)
        page.locator("omk-select-option:nth-child(2) > md-select-option").click()  # Monthly
        page.wait_for_timeout(300)
        
        page.screenshot(path=get_screenshot_path("3.png"), full_page=True)
        
        page.get_by_role("button", name="Continue").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Step 4: Beneficiary details
        current_step = "Step 4: Beneficiary Details"
        print(f"{current_step}")
        page.screenshot(path=get_screenshot_path("4.png"), full_page=True)
        page.get_by_role("button", name="Add Beneficiary").click()
        page.wait_for_timeout(500)
        
        page.get_by_role("textbox", name="Beneficiary Name").fill("Test Beneficiary")
        page.wait_for_timeout(200)
        page.get_by_role("textbox", name="Beneficiary Phone").fill("0712345678")
        page.wait_for_timeout(200)
        page.get_by_role("textbox", name="Beneficiary Email").fill("beneficiary@test.com")
        page.wait_for_timeout(200)
        
        page.get_by_role("button", name="Continue").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Step 5: Document upload
        current_step = "Step 5: Document Upload"
        print(f"{current_step}")
        page.screenshot(path=get_screenshot_path("5.png"), full_page=True)
        
        # Upload ID document
        page.locator("#upload-idDoc input[type='file']").set_input_files("download.jpeg")
        page.wait_for_timeout(500)
        
        # Upload KRA document
        page.locator("#upload-kraDoc input[type='file']").set_input_files("download.jpeg")
        page.wait_for_timeout(500)
        
        page.get_by_role("button", name="Continue").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Step 6: Terms & Conditions
        current_step = "Step 6: Terms & Conditions"
        print(f"{current_step}")
        page.screenshot(path=get_screenshot_path("6.png"), full_page=True)
        
        # Accept terms
        page.get_by_role("checkbox", name="I agree to the terms and conditions").check()
        page.wait_for_timeout(300)
        
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(1000)
        
        # Step 7: Payment processing
        current_step = "Step 7: Payment Processing"
        print(f"{current_step}")
        page.screenshot(path=get_screenshot_path("7.png"), full_page=True)
        
        # Select M-Pesa payment
        page.get_by_role("heading", name="M-Pesa").click()
        page.wait_for_timeout(500)
        page.get_by_role("textbox", name="M-Pesa number").fill("0712345678")
        page.wait_for_timeout(500)
        
        page.get_by_role("button", name="Process payment").click()
        page.wait_for_timeout(3000)
        
        # Success
        duration = (datetime.now() - start_time).total_seconds()
        success_message = (
            f"*Personal Pension Plan Test Passed!*\n"
            f"*Duration:* {duration:.1f} seconds\n\n"
            f"✓ Step 1: Select Pension Plan\n"
            f"✓ Step 2: Personal Information\n"
            f"✓ Step 3: Contribution Details\n"
            f"✓ Step 4: Beneficiary Details\n"
            f"✓ Step 5: Document Upload\n"
            f"✓ Step 6: Terms & Conditions\n"
            f"✓ Step 7: Payment Processing\n"
            f"\nScreenshots saved in: `{SCREENSHOTS_DIR}/`"
        )
        print(success_message)
        send_slack_notification(success_message)
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        
        # Get detailed error info
        error_traceback = traceback.format_exc()
        failure_step = get_failure_step(str(e))
        
        # If we have current_step, use it as the failure point
        if current_step:
            failure_step = current_step
        
        error_screenshot = get_screenshot_path("error.png")
        page.screenshot(path=error_screenshot, full_page=True)
        
        error_message = (
            f"*Personal Pension Plan Test Failed!*\n"
            f"*Failure Step:* {failure_step}\n"
            f"*Duration:* {duration:.1f} seconds\n"
            f"*Error:* {str(e)}\n"
            f"*Error Screenshot:* `{error_screenshot}`\n"
            f"\nScreenshots saved in: `{SCREENSHOTS_DIR}/`"
        )
        print(error_message)
        send_slack_notification(error_message)
        
    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
