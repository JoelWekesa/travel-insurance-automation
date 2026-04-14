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
            "text": f"{emoji} Lengo One Off Test - {emoji}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} Lengo One Off Test Alert"
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

def run_lengo_oneoff():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        start_time = datetime.now()
        current_step = ""
        
        try:
            # Step 1: Navigate directly to Lengo app
            current_step = "Step 1: Navigate to Lengo"
            print(f"{current_step}")
            page.goto("https://oldmutual.co.ke/app/public/lengo-digital-savings", timeout=60000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            close_zoho_if_present(page)
            page.screenshot(path=get_screenshot_path("1_navigate.png"), full_page=True)
            
            page1 = page
            
            # Step 2: Personal Details
            current_step = "Step 2: Personal Details"
            print(f"{current_step}")
            page1.get_by_role("textbox", name="First Name").fill("test")
            page1.get_by_role("textbox", name="Surname").fill("test")
            page1.get_by_role("textbox", name="Phone Number").fill("0742587248")
            page1.get_by_role("textbox", name="Email").fill("faith.njeri@oldmutual.com")
            
            try:
                page1.get_by_role("button", name="Close tooltip").click(timeout=2000)
            except:
                pass
            
            close_zoho_if_present(page1)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_load_state("networkidle")
            page1.screenshot(path=get_screenshot_path("2_personal.png"), full_page=True)
            
            # Step 3: Plan Selection - One Off
            current_step = "Step 3: Plan Selection - One Off"
            print(f"{current_step}")
            page1.wait_for_timeout(1000)
            page1.get_by_role("button", name="SELECT").nth(1).click()
            page1.wait_for_timeout(2000)
            
            # Fill One Off details
            page1.get_by_role("spinbutton", name="Lumpsum Contribution").fill("300000")
            page1.get_by_role("textbox", name="When would you like to start").fill("12/12/2026")
            page1.get_by_role("spinbutton", name="How long are you saving for").fill("60")
            
            close_zoho_if_present(page1)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_load_state("networkidle")
            page1.screenshot(path=get_screenshot_path("3_plan.png"), full_page=True)
            
            # Step 4: Review and Continue
            current_step = "Step 4: Review Quote"
            print(f"{current_step}")
            page1.wait_for_timeout(1000)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_timeout(500)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_load_state("networkidle")
            page1.screenshot(path=get_screenshot_path("4_review.png"), full_page=True)
            
            # Step 5: Additional Personal Info
            current_step = "Step 5: Additional Personal Info"
            print(f"{current_step}")
            page1.wait_for_timeout(1000)
            
            # Title - use keyboard
            page1.locator(".display-value").first.click()
            page1.wait_for_timeout(500)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("Enter")
            page1.wait_for_timeout(500)
            
            # Date of birth
            page1.get_by_role("textbox", name="Date of birth").fill("01/01/2000")
            
            # Gender
            page1.locator("div:nth-child(5) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page1.wait_for_timeout(500)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("Enter")
            page1.wait_for_timeout(500)
            
            # Nationality
            page1.locator("div:nth-child(6) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page1.wait_for_timeout(500)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("Enter")
            page1.wait_for_timeout(500)
            
            # Occupation
            page1.locator("div:nth-child(7) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page1.wait_for_timeout(500)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("Enter")
            page1.wait_for_timeout(500)
            
            # Source of funds
            page1.locator("div:nth-child(8) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page1.wait_for_timeout(500)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("Enter")
            page1.wait_for_timeout(500)
            
            # Employer name (if visible)
            try:
                page1.get_by_role("textbox", name="Employer name").fill("test", timeout=3000)
            except:
                pass
            
            # Income range (try different selectors)
            try:
                page1.locator("div:nth-child(10) > omk-select > .anchor-wrapper > #materialField > .display-value").click(timeout=5000)
                page1.wait_for_timeout(500)
                page1.keyboard.press("ArrowDown")
                page1.wait_for_timeout(300)
                page1.keyboard.press("ArrowDown")
                page1.wait_for_timeout(300)
                page1.keyboard.press("Enter")
                page1.wait_for_timeout(500)
            except:
                # Try alternative selector
                try:
                    page1.locator("div:nth-child(9) > omk-select > .anchor-wrapper > #materialField > .display-value").click(timeout=5000)
                    page1.wait_for_timeout(500)
                    page1.keyboard.press("ArrowDown")
                    page1.wait_for_timeout(300)
                    page1.keyboard.press("ArrowDown")
                    page1.wait_for_timeout(300)
                    page1.keyboard.press("Enter")
                    page1.wait_for_timeout(500)
                except:
                    print("  Income range field not found, skipping")
            
            # ID and KRA
            page1.get_by_role("textbox", name="National ID/Passport number").fill("38787377333")
            page1.get_by_role("textbox", name="KRA number").fill("A123456789k")
            page1.get_by_role("textbox", name="Full Postal Address").fill("0100")
            
            close_zoho_if_present(page1)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_timeout(500)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_load_state("networkidle")
            page1.screenshot(path=get_screenshot_path("5_personal_info.png"), full_page=True)
            
            # Step 6: Beneficiary Details
            current_step = "Step 6: Beneficiary Details"
            print(f"{current_step}")
            page1.wait_for_timeout(1000)
            page1.get_by_role("button", name="Add Beneficiary").click()
            page1.wait_for_timeout(1000)
            
            page1.get_by_role("textbox", name="First name").fill("test")
            page1.get_by_role("textbox", name="Last name").fill("test")
            
            # Relationship
            page1.locator(".display-value").click()
            page1.wait_for_timeout(500)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("ArrowDown")
            page1.wait_for_timeout(300)
            page1.keyboard.press("Enter")
            page1.wait_for_timeout(500)
            
            page1.get_by_role("textbox", name="Mobile number").fill("0742587248")
            page1.get_by_role("textbox", name="Email address").fill("faith@oldmutual.com")
            page1.get_by_role("textbox", name="Full postal address").fill("0100")
            page1.get_by_role("spinbutton", name="Percentage split (%)").fill("100")
            
            close_zoho_if_present(page1)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_timeout(500)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_load_state("networkidle")
            page1.screenshot(path=get_screenshot_path("6_beneficiary.png"), full_page=True)
            
            # Step 7: Document Upload
            current_step = "Step 7: Document Upload"
            print(f"{current_step}")
            page1.wait_for_timeout(1000)
            
            page1.locator("#upload-nationalId input#file-upload").first.set_input_files("../download.jpeg")
            page1.wait_for_timeout(1000)
            page1.locator("#upload-kraPin input#file-upload").first.set_input_files("../download.jpeg")
            page1.wait_for_timeout(1000)
            
            close_zoho_if_present(page1)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_load_state("networkidle")
            page1.screenshot(path=get_screenshot_path("7_documents.png"), full_page=True)
            
            # Step 8: Terms & Conditions
            current_step = "Step 8: Terms & Conditions"
            print(f"{current_step}")
            page1.wait_for_timeout(1000)
            
            page1.get_by_test_id("personalDataProcessingConsent").locator("#input").check()
            page1.get_by_test_id("childDataProcessingConsent").locator("#input").check()
            page1.get_by_test_id("consentForNewProductsAndServices").locator("#input").check()
            page1.get_by_test_id("consentForProductsAndServicesRelatedWithMyPolicy").locator("#input").check()
            page1.get_by_test_id("termsAndConditions").locator("#input").check()
            
            close_zoho_if_present(page1)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_timeout(500)
            page1.get_by_role("button", name="Continue").click()
            page1.wait_for_load_state("networkidle")
            page1.screenshot(path=get_screenshot_path("8_terms.png"), full_page=True)
            
            # Step 9: Payment
            current_step = "Step 9: Payment Processing"
            print(f"{current_step}")
            page1.wait_for_timeout(1000)
            
            page1.get_by_role("heading", name="Bank Transfer").click()
            page1.wait_for_timeout(500)
            
            page1.screenshot(path=get_screenshot_path("9_payment.png"), full_page=True)
            page1.get_by_role("button", name="Check payment status").click()
            page1.wait_for_timeout(3000)
            
            # Success
            duration = (datetime.now() - start_time).total_seconds()
            success_message = (
                f"*Lengo One Off Test Passed!*\n"
                f"*Duration:* {duration:.1f} seconds\n\n"
                f"All 9 steps completed successfully!"
            )
            print(success_message)
            send_slack_notification(success_message)
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            error_traceback = traceback.format_exc()
            error_screenshot = get_screenshot_path("error.png")
            
            try:
                page1.screenshot(path=error_screenshot, full_page=True)
            except:
                page.screenshot(path=error_screenshot, full_page=True)
            
            error_message = (
                f"*Lengo One Off Test Failed!*\n"
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
    run_lengo_oneoff()
