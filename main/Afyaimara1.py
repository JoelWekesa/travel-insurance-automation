import re
from datetime import datetime, timedelta
from playwright.sync_api import Playwright, sync_playwright, expect
import requests
import os
import traceback
from dotenv import load_dotenv

load_dotenv()
load_dotenv()
print("WEBHOOK URL:", os.environ.get("SLACK_WEBHOOK_URL"))

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
    
    # Check if webhook URL is configured and not placeholder
    if not webhook_url or "YOUR/WEBHOOK/URL" in webhook_url:
        print("ℹ️ Slack webhook not configured, skipping notification")
        return
    
    try:
        emoji = "[OK]" if "Passed" in message else "[X]"
        
        payload = {
            "text": f"{emoji} *Afya Imara Test*",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} Afya Imara Test Alert"
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
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("[OK] Slack notification sent successfully!")
        else:
            print(f"[X] Failed to send Slack notification: {response.status_code} - {response.text}")
        
    except Exception as e:
        print(f"[X] Error sending Slack notification: {str(e)}")

def close_zoho_if_present(page):
    try:
        zoho_btn = page.get_by_role("button", name="Minimize live chat window")
        if zoho_btn.is_visible(timeout=2000):
            zoho_btn.click()
            print("ℹ️ Zoho chat minimized")
    except:
        pass

def run_afya_imara():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        start_time = datetime.now()
        current_step = ""
        
        try:
            # Step 1: Navigate to Afya Imara
            current_step = "Step 1: Navigate to Afya Imara"
            print(f"{current_step}")
            page.goto(
                "https://www.oldmutual.co.ke/app/public/afya-imara?product=1",
                timeout=60000
            )
            page.wait_for_load_state("networkidle")
            close_zoho_if_present(page)
            page.screenshot(path=get_screenshot_path("1_navigate.png"), full_page=True)
            
            # Step 2: Fill principal details
            current_step = "Step 2: Principal Details"
            print(f"{current_step}")
            page.get_by_role("textbox", name="Your name").wait_for(state="visible", timeout=10000)
            page.get_by_role("textbox", name="Your name").fill("Tester Wangari")
            page.get_by_role("textbox", name="Email").fill("kareynjeri@gmail.com")
            page.get_by_role("spinbutton", name="Phone number").fill("0742587248")
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("2_principal.png"), full_page=True)
            
            # Step 3: Family setup
            current_step = "Step 3: Family Setup"
            print(f"{current_step}")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)  # Extra wait for page transition
            page.screenshot(path=get_screenshot_path("3_before_age.png"), full_page=True)
            
            # Try multiple ways to find the age field
            age_locator = None
            try:
                # Try exact name first
                age_locator = page.get_by_role("textbox", name="What is your age?")
                age_locator.wait_for(state="visible", timeout=10000)
                print("✓ Found age field by exact name")
            except Exception as e:
                print(f"✗ Exact name failed: {e}")
                try:
                    # Try partial name
                    age_locator = page.get_by_role("textbox").filter(has_text=re.compile(r"age", re.IGNORECASE)).first
                    age_locator.wait_for(state="visible", timeout=5000)
                    print("✓ Found age field by partial name")
                except Exception as e:
                    print(f"✗ Partial name failed: {e}")
                    try:
                        # Try by placeholder or label
                        age_locator = page.locator("input[placeholder*='age']").first
                        age_locator.wait_for(state="visible", timeout=5000)
                        print("✓ Found age field by placeholder")
                    except Exception as e:
                        print(f"✗ Placeholder failed: {e}")
                        # Last resort: look for any number input
                        try:
                            age_locator = page.locator("input[type='number']").first
                            age_locator.wait_for(state="visible", timeout=5000)
                            print("✓ Found age field by type=number")
                        except Exception as e:
                            print(f"✗ Type=number failed: {e}")
                            # Debug: save page content
                            page.screenshot(path=get_screenshot_path("3_debug.png"), full_page=True)
                            with open(get_screenshot_path("3_page.html"), "w", encoding="utf-8") as f:
                                f.write(page.content())
                            raise Exception("Could not find age input field - check debug files")
            
            if age_locator:
                age_locator.fill("24")
                print("✓ Age field filled successfully")
            else:
                raise Exception("Could not find age input field")
            
            page.get_by_test_id("spouseIncluded").locator("#input").check()
            page.get_by_test_id("childrenIncluded").locator("#input").check()
            page.get_by_role("button", name="Increase number of children").click()
            page.get_by_role("button", name="Increase number of children").click()
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("3_family.png"), full_page=True)
            
            # Step 4: Ages
            current_step = "Step 4: Family Ages"
            print(f"{current_step}")
            page.wait_for_load_state("networkidle")
            page.get_by_role("textbox", name="Spouse / Partner Age").fill("30")
            page.get_by_test_id("childAge0").get_by_role("textbox").fill("2")
            page.get_by_test_id("childAge1").get_by_role("textbox").fill("2")
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("4_ages.png"), full_page=True)
            
            # Step 5: Cover options
            current_step = "Step 5: Cover Options"
            print(f"{current_step}")
            page.wait_for_load_state("networkidle")
            
            # For Inpatient limit
            inpatient_select = page.get_by_test_id("afyaImaraInpatientLimit").locator("#label")
            inpatient_select.wait_for(state="visible", timeout=10000)
            inpatient_select.click()
            page.get_by_role("option", name="10,000,000").click()
            
            # For Outpatient limit
            outpatient_select = page.get_by_test_id("afyaImaraOutpatientLimit").locator("#label")
            outpatient_select.click()
            page.get_by_role("option", name="250,000").click()
            
            # Wait for UI to update and close dropdown
            page.wait_for_timeout(500)
            page.get_by_test_id("afyaImaraInpatientLimit").click()
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("5_cover.png"), full_page=True)
            
            # Step 6: Add-ons
            current_step = "Step 6: Add-ons"
            print(f"{current_step}")
            page.wait_for_load_state("networkidle")
            page.locator("#rescue-plus").check()
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("6_addons.png"), full_page=True)
            
            # Step 7: Personal details
            current_step = "Step 7: Personal Details"
            print(f"{current_step}")
            page.wait_for_load_state("networkidle")
            page.get_by_role("textbox", name="Date of Birth").fill("12/12/2000")
            page.get_by_role("textbox", name="ID/Passport Number").fill("123123123")
            page.get_by_role("textbox", name="Social Health Authority (SHA").fill("123123123")
            page.get_by_role("textbox", name="KRA Pin Number").fill("A123123123E")
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("7_personal.png"), full_page=True)
            
            # Step 8: Consents
            current_step = "Step 8: Terms & Conditions"
            print(f"{current_step}")
            page.wait_for_load_state("networkidle")
            page.get_by_test_id("termsAndConditions").locator("#input").check()
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("8_consents.png"), full_page=True)
            
            # Step 9: Payment
            current_step = "Step 9: Payment Processing"
            print(f"{current_step}")
            page.wait_for_load_state("networkidle")
            
            # Select M-Pesa payment
            page.get_by_role("heading", name="M-Pesa").click()
            page.wait_for_timeout(500)
            page.get_by_role("textbox", name="M-Pesa number").fill("0742587248")
            page.wait_for_timeout(500)
            
            page.screenshot(path=get_screenshot_path("9_payment.png"), full_page=True)
            page.get_by_role("button", name="Process payment").click()
            page.wait_for_timeout(3000)
            
            # Success
            duration = (datetime.now() - start_time).total_seconds()
            success_message = (
                f"*Afya Imara Test Passed!*\n"
                f"*Duration:* {duration:.1f} seconds\n\n"
                f"✓ Step 1: Navigate to Afya Imara\n"
                f"✓ Step 2: Principal Details\n"
                f"✓ Step 3: Family Setup\n"
                f"✓ Step 4: Family Ages\n"
                f"✓ Step 5: Cover Options\n"
                f"✓ Step 6: Add-ons\n"
                f"✓ Step 7: Personal Details\n"
                f"✓ Step 8: Terms & Conditions\n"
                f"✓ Step 9: Payment Processing\n"
                f"\nScreenshots saved in: `{SCREENSHOTS_DIR}/`"
            )
            print(success_message)
            send_slack_notification(success_message)
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            
            # Get detailed error info
            error_traceback = traceback.format_exc()
            
            error_screenshot = get_screenshot_path("error.png")
            page.screenshot(path=error_screenshot, full_page=True)
            
            error_message = (
                f"*Afya Imara Test Failed!*\n"
                f"*Failure Step:* {current_step}\n"
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
    run_afya_imara()
