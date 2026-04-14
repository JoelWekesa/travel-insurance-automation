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
        emoji = "✅" if "Passed" in message else "❌"
        
        payload = {
            "text": f"{emoji} *Travel Insurance Test*",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} Travel Insurance Test Alert"
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
            print("✅ Slack notification sent successfully!")
        else:
            print(f"❌ Failed to send Slack notification: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error sending Slack notification: {str(e)}")

def close_zoho_if_present(page):
    try:
        zoho_btn = page.get_by_role("button", name="Minimize live chat window")
        if zoho_btn.is_visible(timeout=3000):
            zoho_btn.click()
            print("ℹ️ Zoho chat minimized")
    except:
        print("ℹ️ Zoho chat not present")

def run_afya_imara():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(
            "https://www.oldmutual.co.ke/app/public/afya-imara?product=1",
            timeout=60000
        )
        page.wait_for_load_state("networkidle")
        close_zoho_if_present(page)

        # ------------------ STEP 1 GET QUOTE: PRINCIPAL ------------------
        page.get_by_role("textbox", name="Your name").wait_for(state="visible")
        page.get_by_role("textbox", name="Your name").fill("Tester Wangari")
        page.get_by_role("textbox", name="Email").fill("kareynjeri@gmail.com")
        page.get_by_role("spinbutton", name="Phone number").fill("0742587248")
        page.get_by_role("button", name="Continue").click()

        # ------------------ -- FAMILY SETUP ------------------
        page.wait_for_load_state("networkidle")
        page.get_by_role("textbox", name="What is your age?").fill("24")
        page.get_by_test_id("spouseIncluded").locator("#input").check()
        page.get_by_test_id("childrenIncluded").locator("#input").check()
        page.get_by_role("button", name="Increase number of children").click()
        page.get_by_role("button", name="Increase number of children").click()
        page.get_by_role("button", name="Continue").click()

        # ------------------ -: AGES ------------------
        page.wait_for_load_state("networkidle")
        page.get_by_role("textbox", name="Spouse / Partner Age").fill("30")
        page.get_by_test_id("childAge0").get_by_role("textbox").fill("2")
        page.get_by_test_id("childAge1").get_by_role("textbox").fill("2")
        page.get_by_role("button", name="Continue").click()

        # ------------------ --: COVER OPTIONS ------------------
        page.wait_for_load_state("networkidle")
        page.locator("omk-select").click()
        
        # For Inpatient limit
        page.get_by_test_id("afyaImaraInpatientLimit").locator("#label").click()
        page.get_by_role("option", name="10,000,000").click()

        # For Outpatient limit
        page.get_by_test_id("afyaImaraOutpatientLimit").locator("#label").click()
        page.get_by_role("option", name="250,000").click()
        page.locator("omk-select-option:nth-child(5) > md-select-option").click()
        page.wait_for_timeout(500)
        page.get_by_test_id("afyaImaraInpatientLimit").click() 
        page.get_by_role("button", name="Continue").click()

        # -------------------: ADD-ONS ------------------
        page.wait_for_load_state("networkidle")
        page.locator("#rescue-plus").check()
        page.get_by_role("button", name="Continue").click()

        # ------------------ -@: PERSONAL DETAILS ------------------
        page.wait_for_load_state("networkidle")
        page.get_by_role("textbox", name="Date of Birth").fill("12/12/2000")
        page.get_by_role("textbox", name="ID/Passport Number").fill("123123123")
        page.get_by_role("textbox", name="Social Health Authority (SHA").fill("123123123")
        page.get_by_role("textbox", name="KRA Pin Number").fill("A123123123E")
        page.get_by_role("button", name="Continue").click()

        # ------------------ CONSENTS ------------------
        page.wait_for_load_state("networkidle")
        page.get_by_test_id("termsAndConditions").locator("#input").check()
        page.get_by_role("button", name="Continue").click()

        print("✅ Afya Imara journey completed up to payment")

        context.close()
        browser.close()

if __name__ == "__main__":
    run_afya_imara()
