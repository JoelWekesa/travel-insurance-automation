import re
from datetime import datetime, timedelta
from playwright.sync_api import Playwright, sync_playwright, expect
import requests
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL") or ''

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
    
    if not webhook_url or "YOUR/WEBHOOK/URL" in webhook_url:
        print("ℹ️ Slack webhook not configured, skipping notification")
        return
    
    try:
        emoji = "[OK]" if "Passed" in message else "[X]"
        
        payload = {
            "text": f"{emoji} Motor Insurance Test - {emoji}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} Motor Insurance Test Alert"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
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
    """Close Zoho chat widget and tooltips"""
    try:
        page.locator("#zs-fl-tip").evaluate("el => el.style.display = 'none'")
    except:
        pass
    
    try:
        zoho_btn = page.get_by_role("button", name="Minimize live chat window")
        if zoho_btn.is_visible(timeout=1000):
            zoho_btn.click()
    except:
        pass
    
    try:
        page.locator("[data-id='zsalesiq']").evaluate("el => el.style.display = 'none'")
    except:
        pass

def run_motor_insurance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        start_time = datetime.now()
        current_step = ""
        
        try:
            # Step 1: Navigate and Select Cover Type
            current_step = "Step 1: Navigate and Select Cover Type"
            print(f"{current_step}")
            page.goto("https://oldmutual.co.ke/app/public/motor-private", timeout=60000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            
            page.get_by_test_id("third-party-select").get_by_role("button", name="Select").click()
            page.wait_for_timeout(1000)
            
            try:
                page.get_by_role("button", name="Close tooltip").click(timeout=2000)
            except:
                pass
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("1_cover_type.png"), full_page=True)
            
            # Step 2: Personal Details
            current_step = "Step 2: Personal Details"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_role("textbox", name="Fullname").fill("test doe")
            page.get_by_role("textbox", name="Phone").fill("0742587238")
            page.get_by_role("textbox", name="Email").fill("faith.njeri@oldmutual.com")
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("2_personal.png"), full_page=True)
            
            # Step 3: Vehicle Details
            current_step = "Step 3: Vehicle Details"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            # Select Car
            page.locator("div").filter(has_text=re.compile(r"^Car$")).click()
            page.wait_for_timeout(500)
            
            # Vehicle type
            page.get_by_test_id("ke-vehicle-type-0").locator("omk-radio-button").click()
            page.wait_for_timeout(500)
            
            # Make - BMW using keyboard
            page.locator(".display-value").first.click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Model using keyboard
            page.locator("div:nth-child(6) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Year of manufacture
            page.get_by_role("spinbutton", name="Year of manufacture").fill("2011")
            
            # Start date
            page.get_by_role("textbox", name="When would you like your").fill("01/01/2027")
            
            # Alarm and tracking
            page.get_by_test_id("ke-alarm-installed-0").locator("omk-radio-button").click()
            page.wait_for_timeout(300)
            page.locator("#ke-tracking-installed-1 > .sc-omk-radio.hydrated > .outer-circle").click()
            page.wait_for_timeout(500)
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("3_vehicle.png"), full_page=True)
            
            # Step 4: Buy Now and Additional Details
            current_step = "Step 4: Additional Personal Details"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Buy Now").click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
            
            # Nationality using keyboard
            page.locator(".display-value").first.click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # National ID
            page.get_by_role("textbox", name="National ID").fill("17837723")
            
            # Date of Birth
            page.get_by_role("textbox", name="Date of Birth").fill("01/01/2001")
            
            # Gender
            page.locator("#ke-gender-type-1 > .sc-omk-radio.hydrated > .outer-circle").click()
            page.wait_for_timeout(500)
            
            # Occupation using keyboard
            page.locator("div:nth-child(7) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # KRA PIN
            try:
                page.get_by_role("textbox", name="KRA PIN").fill("A123456789k", timeout=5000)
            except:
                print("  KRA PIN field not found, skipping")
            
            # Postal Address
            try:
                page.get_by_role("textbox", name="Postal Address").fill("0100", timeout=5000)
            except:
                print("  Postal Address field not found, skipping")
            
            # Agent select - No
            page.locator("#ke-agent-select-1 > .sc-omk-radio.hydrated > .outer-circle > .inner-circle").click()
            page.wait_for_timeout(500)
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Next").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("4_additional_details.png"), full_page=True)
            
            # Step 5: Vehicle Registration Details
            current_step = "Step 5: Vehicle Registration Details"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            page.get_by_role("textbox", name="Vehicle registration number").fill("KHA123k")
            page.get_by_role("textbox", name="Chassis number").fill("GH12-283")
            page.get_by_role("textbox", name="Engine Number").fill("GDHY-097YUIy")
            
            # Fuel type using keyboard
            page.locator(".display-value").first.click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Body type using keyboard
            page.locator("div:nth-child(5) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Sitting capacity
            page.get_by_role("spinbutton", name="Sitting capacity").fill("1")
            
            # Color using keyboard
            page.locator("div:nth-child(7) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Years with driving license
            page.get_by_role("spinbutton", name="Years with driving license").fill("3")
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Next").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("5_vehicle_registration.png"), full_page=True)
            
            # Step 6: Review and Continue
            current_step = "Step 6: Review Details"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("6_review.png"), full_page=True)
            
            # Step 7: Document Upload
            current_step = "Step 7: Document Upload"
            print(f"{current_step}")
            page.wait_for_timeout(2000)
            
            # Upload documents using simpler selectors
            try:
                # Find all file upload buttons and upload to each
                upload_buttons = page.locator("#button").all()
                for i, button in enumerate(upload_buttons[:3]):  # Upload to first 3 buttons
                    try:
                        button.set_input_files("../download.jpeg")
                        page.wait_for_timeout(500)
                        print(f"  Document {i+1} uploaded")
                    except:
                        print(f"  Document {i+1} upload skipped")
            except Exception as e:
                print(f"  Document upload error: {e}")
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("7_documents.png"), full_page=True)
            
            # Step 8: Declarations
            current_step = "Step 8: Declarations"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            page.get_by_test_id("hasDeclinedProposal").locator("#input").check()
            page.get_by_test_id("hasIncreasedPremium").locator("#input").check()
            page.get_by_test_id("hasCancelledPolicy").locator("#input").check()
            page.get_by_test_id("hasPhysicalCondition").locator("#input").check()
            page.get_by_test_id("hasDrivingOffense").locator("#input").check()
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("8_declarations.png"), full_page=True)
            
            # Step 9: Terms & Conditions
            current_step = "Step 9: Terms & Conditions"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            page.get_by_test_id("ke-personalDataProcessingConsent-0").locator("omk-radio-button").click()
            page.locator("#ke-childDataProcessingConsent-0 > .sc-omk-radio.hydrated > .outer-circle > .inner-circle").click()
            page.get_by_test_id("consentForNewProductsAndServices").locator("#input").check()
            page.get_by_test_id("consentForProductsAndServicesRelatedWithMyPolicy").locator("#input").check()
            page.get_by_test_id("termsAndConditions").locator("#input").check()
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("9_terms.png"), full_page=True)
            
            # Step 10: Payment
            current_step = "Step 10: Payment Processing"
            print(f"{current_step}")
            page.wait_for_timeout(2000)
            
            page.screenshot(path=get_screenshot_path("10_payment.png"), full_page=True)
            page.get_by_role("button", name="Process Payment").click()
            page.wait_for_timeout(3000)
            
            # Success
            duration = (datetime.now() - start_time).total_seconds()
            success_message = (
                f"*Motor Insurance Test Passed!*\n"
                f"*Duration:* {duration:.1f} seconds\n\n"
                f"All 10 steps completed successfully!"
            )
            print(success_message)
            send_slack_notification(success_message)
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            error_traceback = traceback.format_exc()
            error_screenshot = get_screenshot_path("error.png")
            
            try:
                page.screenshot(path=error_screenshot, full_page=True)
            except:
                pass
            
            error_message = (
                f"*Motor Insurance Test Failed!*\n"
                f"*Failure Step:* {current_step}\n"
                f"*Duration:* {duration:.1f} seconds\n"
                f"*Error:* {str(e)[:200]}\n"
                f"*Screenshot:* {error_screenshot}"
            )
            print(error_message)
            send_slack_notification(error_message)
            
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    run_motor_insurance()
