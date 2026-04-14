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
            "text": f"{emoji} Lengo Combination Test - {emoji}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} Lengo Combination Test Alert"
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

def run_lengo_combination():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        start_time = datetime.now()
        current_step = ""
        
        try:
            # Step 1: Navigate to Lengo
            current_step = "Step 1: Navigate to Lengo"
            print(f"{current_step}")
            page.goto("https://oldmutual.co.ke/app/public/lengo-digital-savings", timeout=60000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            close_zoho_if_present(page)
            page.screenshot(path=get_screenshot_path("1_navigate.png"), full_page=True)
            
            # Step 2: Personal Details
            current_step = "Step 2: Personal Details"
            print(f"{current_step}")
            page.get_by_role("textbox", name="First Name").fill("test")
            page.get_by_role("textbox", name="Surname").fill("test")
            page.get_by_role("textbox", name="Phone Number").fill("0742587248")
            page.get_by_role("textbox", name="Email").fill("faith.njeri@oldmutual.com")
            
            try:
                page.get_by_role("button", name="Close tooltip").click(timeout=2000)
            except:
                pass
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("2_personal.png"), full_page=True)
            
            # Step 3: Plan Selection - Combination
            current_step = "Step 3: Plan Selection - Combination"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="SELECT").nth(2).click()
            page.wait_for_timeout(2000)
            
            # Select Yearly frequency using keyboard
            page.locator(".display-value").click()
            page.wait_for_timeout(1000)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Fill Combination details
            page.get_by_role("spinbutton", name="Desired Contribution").fill("36001")
            page.wait_for_timeout(500)
            page.get_by_role("spinbutton", name="Lumpsum Contribution").fill("300000")
            page.wait_for_timeout(500)
            page.get_by_role("textbox", name="When would you like to start").fill("01/01/2027")
            page.wait_for_timeout(500)
            page.get_by_role("spinbutton", name="How long are you saving for").fill("120")
            page.wait_for_timeout(1000)
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("3_plan.png"), full_page=True)
            
            # Step 4: Review and Continue
            current_step = "Step 4: Review Quote"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            # Close any tooltips
            try:
                page.locator(".flex.items-center > .hydrated > md-icon > slot").first.click(timeout=2000)
            except:
                pass
            
            page.get_by_role("button", name="Continue").click()
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("4_review.png"), full_page=True)
            
            # Step 5: Additional Personal Info
            current_step = "Step 5: Additional Personal Info"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            # Title - use keyboard
            page.locator(".display-value").first.click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Date of birth
            page.get_by_role("textbox", name="Date of birth").fill("01/01/2001")
            
            # Gender
            page.locator("div:nth-child(5) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Nationality
            page.locator("div:nth-child(6) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Occupation
            page.locator("div:nth-child(7) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Source of funds
            page.locator("div:nth-child(8) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # ID, Postal Address, and KRA
            page.get_by_role("textbox", name="National ID/Passport number").fill("1253663")
            page.get_by_role("textbox", name="Full Postal Address").fill("0100")
            page.get_by_role("textbox", name="KRA number").fill("A123456789k")
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("5_personal_info.png"), full_page=True)
            
            # Step 6: Intermediary Selection
            current_step = "Step 6: Intermediary Selection"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            # Select Yes and search for agent
            page.locator(".outer-circle").first.click()
            page.wait_for_timeout(500)
            page.get_by_role("searchbox", name="Search By First Name").fill("John")
            page.wait_for_timeout(1000)
            
            # Select agent using keyboard
            page.locator(".display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("6_intermediary.png"), full_page=True)
            
            # Step 7: Beneficiary Details
            current_step = "Step 7: Beneficiary Details"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Add Beneficiary").click()
            page.wait_for_timeout(1000)
            
            page.get_by_role("textbox", name="First name").fill("test")
            page.get_by_role("textbox", name="Last name").fill("test")
            
            # Relationship - use keyboard
            page.locator(".display-value").click()
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(300)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            page.get_by_role("textbox", name="Mobile number").fill("0742578765")
            page.get_by_role("textbox", name="Email address").fill("faith.njeri@oldmutual.com")
            page.get_by_role("textbox", name="Full postal address").fill("0100")
            page.get_by_role("spinbutton", name="Percentage split (%)").fill("100")
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("7_beneficiary.png"), full_page=True)
            
            # Step 8: Document Upload
            current_step = "Step 8: Document Upload"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            page.locator("#upload-nationalId input#file-upload").first.set_input_files("../download.jpeg")
            page.wait_for_timeout(1000)
            page.locator("#upload-kraPin input#file-upload").first.set_input_files("../download.jpeg")
            page.wait_for_timeout(1000)
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("8_documents.png"), full_page=True)
            
            # Step 9: Terms & Conditions
            current_step = "Step 9: Terms & Conditions"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            page.get_by_test_id("personalDataProcessingConsent").locator("#input").check()
            page.get_by_test_id("childDataProcessingConsent").locator("#input").check()
            page.get_by_test_id("consentForNewProductsAndServices").locator("#input").check()
            page.get_by_test_id("consentForProductsAndServicesRelatedWithMyPolicy").locator("#input").check()
            page.get_by_test_id("termsAndConditions").locator("#input").check()
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_timeout(500)
            page.get_by_role("button", name="Continue").click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("9_terms.png"), full_page=True)
            
            # Step 10: Payment
            current_step = "Step 10: Payment Processing"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            page.screenshot(path=get_screenshot_path("10_payment.png"), full_page=True)
            page.get_by_role("button", name="Check payment status").click()
            page.wait_for_timeout(3000)
            
            # Success
            duration = (datetime.now() - start_time).total_seconds()
            success_message = (
                f"*Lengo Combination Test Passed!*\n"
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
                f"*Lengo Combination Test Failed!*\n"
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
    run_lengo_combination()
