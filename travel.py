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


def get_failure_step(error_message):
    """Determine which step failed based on error message"""
    error_lower = error_message.lower()
    
    if "select cover" in error_lower:
        return "Step 1: Select Cover Type"
    elif "fullname" in error_lower or "phone" in error_lower or "email" in error_lower:
        if "beneficiary" in error_lower or "step 6" in error_lower:
            return "Step 6: Beneficiary Details"
        else:
            return "Step 2: Personal Information"
    elif "traveller" in error_lower or "departure" in error_lower or "return" in error_lower or "omk-select" in error_lower:
        return "Step 3: Travel Details"
    elif "proceed to buy" in error_lower:
        return "Step 4: Review & Proceed"
    elif "add details" in error_lower or "date of birth" in error_lower or "id number" in error_lower or "passport" in error_lower or "kra" in error_lower or "upload" in error_lower:
        return "Step 5: Traveller Details & Documents"
    elif "consent" in error_lower or "terms" in error_lower:
        return "Step 7: Terms & Conditions"
    elif "process payment" in error_lower:
        return "Step 8: Payment Processing"
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
        # Step 1: Navigate and select cover
        current_step = "Step 1: Select Cover Type"
        print(f"{current_step}")
        page.goto("https://www.oldmutual.co.ke/app/public/travel-insurance")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)
        
        # Handle unexpected window dialogs (e.g., Double Insurance alert)
        def handle_dialog(dialog):
            print(f"Dialog appeared: '{dialog.message}'. Accepting...")
            dialog.accept()
        page.on("dialog", handle_dialog)
        
        page.screenshot(path=get_screenshot_path("1.png"), full_page=True)
        
        page.get_by_test_id("retail").get_by_role("button", name="Select Cover").click()
        page.wait_for_timeout(500)
        
        # Step 1 & Step 2: Dynamic Flow (Forms are randomly swapped under "Step 1 of 6")
        for i in range(2):
            page.wait_for_timeout(3000)
            
            # Form A: Personal Information
            if page.get_by_role("textbox", name="Fullname").is_visible():
                current_step = f"Page {i+1}: Personal Information"
                print(f"{current_step}")
                page.get_by_role("textbox", name="Fullname").fill("Test User")
                page.get_by_role("textbox", name="Phone").fill("0712345678")
                page.get_by_role("textbox", name="Email").fill("test@user.com")
                
                try:
                    page.get_by_role("button", name="Close tooltip").click(timeout=1000)
                except:
                    pass
                
                page.wait_for_timeout(300)
                page.screenshot(path=get_screenshot_path(f"dynamic_step_{i+1}.png"), full_page=True)
                
            # Form B: Travel Details
            elif page.locator(".inner-circle").first.is_visible():
                current_step = f"Page {i+1}: Travel Details"
                print(f"{current_step}")
                page.locator(".inner-circle").first.click()
                page.wait_for_timeout(300)
                
                # DOB
                try:
                    page.get_by_placeholder(re.compile("Traveller", re.IGNORECASE)).first.fill("01/01/1990")
                except Exception:
                    page.get_by_role("textbox", name=re.compile("Traveller", re.IGNORECASE)).first.fill("01/01/1990")
                page.wait_for_timeout(500)
                
                page.locator("omk-select").click()
                page.wait_for_timeout(500)
                
                page.locator("omk-select-option:nth-child(5) > md-select-option").click()
                page.wait_for_timeout(300)
                
                departure_date = (datetime.now() + timedelta(days=5)).strftime("%d/%m/%Y")
                return_date = (datetime.now() + timedelta(days=6)).strftime("%d/%m/%Y")
                
                page.get_by_role("textbox", name="Departure Date").fill(departure_date)
                page.wait_for_timeout(1500)
                
                # Double Insurance Handling
                try:
                    # Sometimes an explicit NO radio button appears here
                    radio_no = page.get_by_text("No", exact=True).locator("..").locator(".inner-circle").last
                    if radio_no.is_visible():
                        radio_no.click()
                        page.wait_for_timeout(500)
                except:
                    pass
                
                page.get_by_role("textbox", name="Return Date").fill(return_date)
                page.wait_for_timeout(200)
                
                # Second Double Insurance attempt (native dialog is handled in setup)
                try:
                    if page.get_by_role("radio", name="No").is_visible():
                        page.get_by_role("radio", name="No").click()
                except:
                    pass
                
                page.screenshot(path=get_screenshot_path(f"dynamic_step_{i+1}.png"), full_page=True)
            
            else:
                print(f"Page {i+1}: Unknown Form encountered!")
                
            # Standard navigation forward
            btn = page.get_by_role("button", name="Continue", exact=True).last
            if not btn.is_visible():
                btn = page.locator("button:has-text('Continue')").last
            btn.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
        
        # Page 3: Select a Plan (was Review and proceed)
        current_step = "Page 3: Select a Plan"
        print(f"{current_step}")
        page.screenshot(path=get_screenshot_path("4.png"), full_page=True)
        page.wait_for_load_state("networkidle")
        
        btn = page.get_by_role("button", name="Continue", exact=True).last
        if btn.is_visible():
            btn.click()
        else:
            page.locator("button:has-text('Continue')").last.click()
            
        page.wait_for_timeout(2000)
        
        # Page 4: Final Quotation Summary
        current_step = "Page 4: Final quotation summary"
        print(f"{current_step}")
        page.screenshot(path=get_screenshot_path("5.png"), full_page=True)
        page.wait_for_load_state("networkidle")
        page.get_by_role("button", name="Proceed to buy").click()
        page.wait_for_timeout(2000)
        
        # Page 5: Traveller Details (Before we begin)
        current_step = "Page 5: Traveller Details - Before We Begin"
        print(f"{current_step}")
        page.screenshot(path=get_screenshot_path("6.png"), full_page=True)
        page.wait_for_load_state("networkidle")
        
        btn = page.get_by_role("button", name="Continue", exact=True).last
        if btn.is_visible():
            btn.click()
        else:
            page.locator("button:has-text('Continue')").last.click()
            
        page.wait_for_timeout(2000)
        
        # Page 6: Traveller Details & Documents Form
        current_step = "Page 6: Traveller Details & Documents Form"
        print(f"{current_step}")
        page.screenshot(path=get_screenshot_path("7.png"), full_page=True)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Expand Principal Details
        try:
            page.get_by_role("button", name=re.compile("Add details", re.IGNORECASE)).click()
        except:
            page.locator("text='Add details'").first.click()
        page.wait_for_timeout(500)
        
        # Emergency Contact
        try:
            page.locator("input[name*='nokName' i], input[name*='kinName' i], input[name*='emergencyName' i]").first.fill("Jane Doe")
            page.locator("input[name*='nokPhone' i], input[name*='kinPhone' i], input[name*='emergencyPhone' i]").first.fill("0712345678")
        except:
            page.get_by_role("textbox", name=re.compile("Fullname", re.IGNORECASE)).last.fill("Jane Doe")
            page.get_by_role("textbox", name=re.compile("Phone", re.IGNORECASE)).last.fill("0712345678")
        page.wait_for_timeout(200)

        # Id Number
        try:
            page.get_by_role("textbox", name=re.compile("Id Number", re.IGNORECASE)).fill("12345675")
        except:
            try:
                page.get_by_role("spinbutton", name=re.compile("Id Number", re.IGNORECASE)).fill("12345675")
            except:
                try:
                    page.locator("input[name*='idNumber' i], input[name*='nationalid' i]").first.fill("12345675")
                except:
                    page.locator("text='Id Number'").locator("xpath=ancestor::div[1]//input").first.fill("12345675")
        page.wait_for_timeout(200)
        
        # Passport No
        try:
            page.get_by_role("textbox", name=re.compile("Passport No", re.IGNORECASE)).fill("12345678")
        except:
            try:
                page.locator("input[name*='passport' i]").first.fill("12345678")
            except:
                page.locator("text='Passport No'").locator("xpath=ancestor::div[1]//input").first.fill("12345678")
        page.wait_for_timeout(200)
        
        # KRA PIN
        try:
            page.get_by_role("textbox", name=re.compile("KRA PIN", re.IGNORECASE)).fill("A123456789K")
        except:
            try:
                page.locator("input[name*='kra' i]").first.fill("A123456789K")
            except:
                page.locator("text='KRA PIN'").locator("xpath=ancestor::div[1]//input").first.fill("A123456789K")
        page.wait_for_timeout(200)
        
        page.locator("#upload-idDoc input[type='file']").set_input_files("download.jpeg")
        page.wait_for_timeout(500)
        
        page.locator("#upload-kraDoc input[type='file']").set_input_files("download.jpeg")
        page.wait_for_timeout(500)
        
        page.locator("#upload-passportDoc input[type='file']").set_input_files("download.jpeg")
        page.wait_for_timeout(500)
        
        page.screenshot(path=get_screenshot_path("7.png"), full_page=True)
        page.get_by_role("button", name="Continue").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Step 6: Beneficiary details
        current_step = "Step 6: Beneficiary Details"
        print(f"{current_step}")
        page.get_by_role("textbox", name="Fullname").fill("Test User")
        page.wait_for_timeout(200)
        
        page.get_by_role("textbox", name="Phone").fill("0712345678")
        page.wait_for_timeout(200)
        
        page.get_by_role("textbox", name="Email").fill("test@user.com")
        page.wait_for_timeout(1000)
        
        page.screenshot(path=get_screenshot_path("8.png"), full_page=True)
        page.get_by_role("button", name="Continue").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Step 7: Terms and conditions
        current_step = "Step 7: Terms & Conditions"
        print(f"{current_step}")
        page.get_by_test_id("consentForProductsAndServicesRelatedWithMyPolicy").locator("#input").check()
        page.wait_for_timeout(200)
        
        page.get_by_test_id("termsAndConditions").locator("#input").check()
        page.wait_for_timeout(1000)
        
        page.screenshot(path=get_screenshot_path("9.png"), full_page=True)
        page.get_by_role("button", name="Continue").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Step 8: Process payment
        current_step = "Step 8: Payment Processing"
        print(f"{current_step}")
        page.get_by_role("button", name="Process Payment").click()
        page.wait_for_timeout(2000)
        
        success_screenshot = get_screenshot_path("success.png")
        page.screenshot(path=success_screenshot, full_page=True)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        
        print(f"\nTest completed successfully!")
        print(f"Duration: {duration:.1f} seconds")
        print(f"Screenshots saved in: {SCREENSHOTS_DIR}/")
        
        success_message = (
            f"*Test Status:* Passed ✓\n"
            f"*Duration:* {duration:.1f} seconds\n"
            f"*Environment:* Production\n"
            f"*URL:* https://www.oldmutual.co.ke/app/public/travel-insurance\n"
            f"*All Steps Completed:*\n"
            f"  ✓ Step 1: Select Cover Type\n"
            f"  ✓ Step 2: Personal Information\n"
            f"  ✓ Step 3: Travel Details\n"
            f"  ✓ Step 4: Review & Proceed\n"
            f"  ✓ Step 5: Traveller Details\n"
            f"  ✓ Step 6: Beneficiary Details\n"
            f"  ✓ Step 7: Terms & Conditions\n"
            f"  ✓ Step 8: Payment Processing\n"
            f"\nScreenshots saved in: `{SCREENSHOTS_DIR}/`"
        )
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
            f"*Test Status:* Failed ✗\n"
            f"*Failed At:* {failure_step}\n"
            f"*Duration:* {duration:.1f} seconds\n"
            f"*Environment:* Production\n"
            f"*URL:* https://www.oldmutual.co.ke/app/public/travel-insurance\n"
            f"*Error Details:*\n```{str(e)}```\n"
            f"\n📸 Error screenshot: `{error_screenshot}`"
        )
        
        print(f"\n❌ Test failed at {failure_step}: {str(e)}")
        print(f"Error screenshot saved: {error_screenshot}")
        print(f"\nFull traceback:\n{error_traceback}")
        
        send_slack_notification(error_message)
        
        raise
    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)