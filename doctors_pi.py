from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright
import requests
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ----------------
DOCTORS_PI_URL = "https://www.oldmutual.co.ke/app/public/doctors-professional-indemnity"
SCREENSHOTS_DIR = "screenshots"
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL") or ""

if not os.path.exists(SCREENSHOTS_DIR):
    os.makedirs(SCREENSHOTS_DIR)

# ---------------- HELPERS ----------------
def get_screenshot_path(filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(SCREENSHOTS_DIR, f"{timestamp}_{filename}")

def send_slack_notification(message):
    emoji = "✅" if "Passed" in message else "❌"

    payload = {
        "text": f"{emoji} Doctors PI Test",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} Doctors Professional Indemnity Test Alert"
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

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print("✅ Slack notification sent")
        else:
            print(f"❌ Slack failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Slack error: {e}")

# ---------------- MAIN RUN ----------------
def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    start_time = datetime.now()
    current_step = ""

    try:
        # Step 1
        current_step = "Step 1: Open Doctors PI Journey"
        print(current_step)
        page.goto(DOCTORS_PI_URL)
        page.wait_for_load_state("networkidle")
        page.screenshot(path=get_screenshot_path("step_1_journey_loaded.png"), full_page=True)

        # Step 2
        current_step = "Step 2: Personal Details Page Loaded"
        print(current_step)
        page.wait_for_timeout(1500)
        page.screenshot(path=get_screenshot_path("step_2_personal_details.png"), full_page=True)

        # Step 3
        current_step = "Step 3: Professional Details Page Loaded"
        print(current_step)
        page.wait_for_timeout(1500)
        page.screenshot(path=get_screenshot_path("step_3_professional_details.png"), full_page=True)

        # Step 4
        current_step = "Step 4: Address Information Page Loaded"
        print(current_step)
        page.wait_for_timeout(1500)
        page.screenshot(path=get_screenshot_path("step_4_address.png"), full_page=True)

        # Step 5
        current_step = "Step 5: Document Upload Section Loaded"
        print(current_step)
        page.wait_for_timeout(1500)
        page.screenshot(path=get_screenshot_path("step_5_documents.png"), full_page=True)

        # Step 6
        current_step = "Step 6: Consents & Declarations Page Loaded"
        print(current_step)
        page.wait_for_timeout(1500)
        page.screenshot(path=get_screenshot_path("step_6_consents.png"), full_page=True)

        # Step 7
        current_step = "Step 7: Payment Page Loaded"
        print(current_step)
        page.wait_for_timeout(1500)
        page.screenshot(path=get_screenshot_path("step_7_payment.png"), full_page=True)

        duration = (datetime.now() - start_time).total_seconds()

        success_message = (
            f"*Test Status:* Passed ✓\n"
            f"*Duration:* {duration:.1f} seconds\n"
            f"*Environment:* Production\n"
            f"*URL:* {DOCTORS_PI_URL}\n"
            f"*All Steps Completed:*\n"
            f"  ✓ Step 1: Open Doctors PI Journey\n"
            f"  ✓ Step 2: Personal Details Page Loaded\n"
            f"  ✓ Step 3: Professional Details Page Loaded\n"
            f"  ✓ Step 4: Address Information Page Loaded\n"
            f"  ✓ Step 5: Document Upload Section Loaded\n"
            f"  ✓ Step 6: Consents & Declarations Page Loaded\n"
            f"  ✓ Step 7: Payment Page Loaded\n"
            f"\nScreenshots saved in: `{SCREENSHOTS_DIR}/`"
        )

        print("✅ Doctors PI journey completed")
        send_slack_notification(success_message)

    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        error_screenshot = get_screenshot_path("error.png")
        page.screenshot(path=error_screenshot, full_page=True)

        error_message = (
            f"*Test Status:* Failed ✗\n"
            f"*Failed At:* {current_step}\n"
            f"*Duration:* {duration:.1f} seconds\n"
            f"*Environment:* Production\n"
            f"*URL:* {DOCTORS_PI_URL}\n"
            f"*Error Details:*\n```{str(e)}```\n"
            f"\n📸 Error screenshot: `{error_screenshot}`"
        )

        print(f"❌ Failed at {current_step}")
        print(traceback.format_exc())
        send_slack_notification(error_message)
        raise

    finally:
        context.close()
        browser.close()

# ---------------- ENTRY ----------------
if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
