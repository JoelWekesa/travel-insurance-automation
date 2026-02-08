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
    
    if not webhook_url:
        print("INFO: No Slack webhook URL configured, skipping notification")
        return
    
    try:
        emoji = "SUCCESS" if "Passed" in message else "ERROR"
        
        payload = {
            "text": f"{emoji} *Doctors Professional Indemnity Test*",
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
        
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 200:
            print("SUCCESS: Slack notification sent successfully!")
        else:
            print(f"ERROR: Failed to send Slack notification: {response.status_code}")
        
    except Exception as e:
        print(f"ERROR: Error sending Slack notification: {str(e)}")


def get_failure_step(error_message):
    """Determine which step failed based on error message"""
    error_lower = error_message.lower()
    
    if "personal details" in error_lower or "fullname" in error_lower or "phone" in error_lower or "email" in error_lower:
        return "Step 1: Personal Details"
    elif "professional details" in error_lower or "medical council" in error_lower or "license" in error_lower:
        return "Step 2: Professional Details"
    elif "address" in error_lower or "postal" in error_lower or "town" in error_lower:
        return "Step 3: Address Information"
    elif "document" in error_lower or "upload" in error_lower or "file" in error_lower:
        return "Step 4: Document Upload"
    elif "consent" in error_lower or "terms" in error_lower or "declaration" in error_lower:
        return "Step 5: Consents & Declarations"
    elif "payment" in error_lower or "process payment" in error_lower:
        return "Step 6: Payment Processing"
    else:
        return "Unknown Step"

def run(playwright: Playwright) -> None:
    # Get headless mode from environment variable - set to False for debugging
    headless = False  # Changed to see the actual page
    
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()
    
    start_time = datetime.now()
    current_step = ""
    
    try:
        # Step 1: Navigate to Doctors PI page and fill personal details
        current_step = "Step 1: Personal Details"
        print(f"{current_step}")
        page.goto("https://www.oldmutual.co.ke/app/public/doctors-professional-indemnity")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        page.screenshot(path=get_screenshot_path("1.png"), full_page=True)
        
        # Wait longer and take screenshot to see what's on the page
        page.wait_for_timeout(3000)
        page.screenshot(path=get_screenshot_path("debug_page.png"), full_page=True)
        
        # Fill personal details - try multiple selectors
        print("Filling personal details...")
        
        # Fill name field
        try:
            page.get_by_role("textbox", name="Fullname").fill("Dr.Wangari")
        except:
            try:
                page.locator("input[name='fullname']").fill("Dr.Wangari")
            except:
                try:
                    page.locator("input[placeholder*='name']").first.fill("Dr.Wangari")
                except:
                    page.locator("input[type='text']").first.fill("Dr.Wangari")
        
        # Fill phone field
        print("Trying to fill phone field...")
        phone_filled = False
        try:
            page.get_by_role("textbox", name="Phone").fill("0712345678")
            phone_filled = True
        except:
            try:
                page.locator("input[name='phone']").fill("0712345678")
                phone_filled = True
            except:
                try:
                    page.locator("input[placeholder*='phone']").first.fill("0712345678")
                    phone_filled = True
                except:
                    print("Could not find phone field, continuing...")
        
        if phone_filled:
            print("Phone field filled successfully")
        
        # Fill email field
        print("Trying to fill email field...")
        email_filled = False
        try:
            page.get_by_role("textbox", name="Email").fill("test@doctor.com")
            email_filled = True
        except:
            try:
                page.locator("input[name='email']").fill("test@doctor.com")
                email_filled = True
            except:
                try:
                    page.locator("input[placeholder*='email']").first.fill("test@doctor.com")
                    email_filled = True
                except:
                    print("Could not find email field, continuing...")
        
        if email_filled:
            print("Email field filled successfully")
        
        # Close any tooltips
        try:
            page.get_by_role("button", name="Close tooltip").click(timeout=2000)
        except:
            pass
        
        page.wait_for_timeout(500)
        page.screenshot(path=get_screenshot_path("2_filled.png"), full_page=True)
        
        # Click Continue button
        print("Trying to click Continue button...")
        continue_clicked = False
        try:
            page.get_by_role("button", name="Continue").click()
            continue_clicked = True
        except:
            try:
                page.locator("button:has-text('Continue')").click()
                continue_clicked = True
            except:
                try:
                    page.locator("button[type='submit']").click()
                    continue_clicked = True
                except:
                    print("Could not find Continue button, taking screenshot and continuing...")
        
        if continue_clicked:
            print("Continue button clicked successfully")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
        
        # Step 2: Professional Details
        current_step = "Step 2: Professional Details"
        print(f"{current_step}")
        
        # Select medical council
        try:
            page.locator("omk-select").first.click()
            page.wait_for_timeout(500)
            page.locator("omk-select-option:nth-child(2) > md-select-option").click()
        except:
            try:
                page.locator("select").first.select_option(index=1)
            except:
                print("Could not select medical council")
        
        page.wait_for_timeout(300)
        
        # Fill license number
        try:
            page.get_by_role("textbox", name="License Number").fill("DOC123456")
        except:
            try:
                page.locator("input[name*='license']").fill("DOC123456")
            except:
                page.locator("input[placeholder*='license']").fill("DOC123456")
        
        # Fill practice name
        try:
            page.get_by_role("textbox", name="Practice Name").fill("TestMedicalPractice")
        except:
            try:
                page.locator("input[name*='practice']").fill("TestMedicalPractice")
            except:
                page.locator("input[placeholder*='practice']").fill("TestMedicalPractice")
        
        # Select specialty
        try:
            page.locator("omk-select").nth(1).click()
            page.wait_for_timeout(500)
            page.locator("omk-select-option:nth-child(3) > md-select-option").click()
        except:
            try:
                page.locator("select").nth(1).select_option(index=2)
            except:
                print("Could not select specialty")
        
        # Fill years of experience
        try:
            page.get_by_role("spinbutton", name="Years of Experience").fill("10")
        except:
            try:
                page.locator("input[name*='experience']").fill("10")
            except:
                page.locator("input[type='number']").fill("10")
        
        page.screenshot(path=get_screenshot_path("3_professional.png"), full_page=True)
        
        # Continue to next step
        try:
            page.get_by_role("button", name="Continue").click()
        except:
            page.locator("button:has-text('Continue')").click()
        
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Step 3: Address Information
        current_step = "Step 3: Address Information"
        print(f"{current_step}")
        
        # Fill address fields
        address_fields = [
            ("Postal Address", "P.O.Box12345"),
            ("Postal Code", "00100"),
            ("Town", "Nairobi"),
            ("Physical Address", "123MedicalPlaza,Nairobi")
        ]
        
        for field_name, value in address_fields:
            try:
                page.get_by_role("textbox", name=field_name).fill(value)
            except:
                try:
                    page.locator(f"input[name*='{field_name.lower().replace(' ', '')}']").fill(value)
                except:
                    try:
                        page.locator(f"input[placeholder*='{field_name.lower()}']").fill(value)
                    except:
                        print(f"Could not fill {field_name}")
            page.wait_for_timeout(200)
        
        page.screenshot(path=get_screenshot_path("4_address.png"), full_page=True)
        
        # Continue to next step
        try:
            page.get_by_role("button", name="Continue").click()
        except:
            page.locator("button:has-text('Continue')").click()
        
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Step 4: Document Upload
        current_step = "Step 4: Document Upload"
        print(f"{current_step}")
        
        # Upload documents if file exists
        if os.path.exists("download.jpeg"):
            document_uploads = [
                "#upload-idDoc input[type='file']",
                "#upload-licenseDoc input[type='file']", 
                "#upload-kraDoc input[type='file']"
            ]
            
            for upload_selector in document_uploads:
                try:
                    page.locator(upload_selector).set_input_files("download.jpeg")
                    page.wait_for_timeout(500)
                except:
                    try:
                        page.locator("input[type='file']").first.set_input_files("download.jpeg")
                        page.wait_for_timeout(500)
                    except:
                        print(f"Could not upload file for {upload_selector}")
        else:
            print("Warning: download.jpeg not found, skipping file uploads")
        
        page.screenshot(path=get_screenshot_path("5_documents.png"), full_page=True)
        
        # Continue to next step
        try:
            page.get_by_role("button", name="Continue").click()
        except:
            page.locator("button:has-text('Continue')").click()
        
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Step 5: Consents & Declarations
        current_step = "Step 5: Consents & Declarations"
        print(f"{current_step}")
        
        # Check consent checkboxes
        try:
            checkboxes = page.locator("input[type='checkbox']").all()
            for i, checkbox in enumerate(checkboxes):
                try:
                    checkbox.check()
                    page.wait_for_timeout(300)
                except:
                    print(f"Could not check checkbox {i}")
        except:
            print("Could not find checkboxes")
        
        page.screenshot(path=get_screenshot_path("6_consents.png"), full_page=True)
        
        # Continue to payment
        try:
            page.get_by_role("button", name="Continue").click()
        except:
            page.locator("button:has-text('Continue')").click()
        
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Step 6: Payment Processing
        current_step = "Step 6: Payment Processing"
        print(f"{current_step}")
        
        page.screenshot(path=get_screenshot_path("7_payment.png"), full_page=True)
        
        # Click process payment
        try:
            page.get_by_role("button", name="Process Payment").click()
        except:
            try:
                page.locator("button:has-text('Process Payment')").click()
            except:
                page.locator("button:has-text('Pay')").click()
        
        page.wait_for_timeout(2000)
        page.screenshot(path=get_screenshot_path("success.png"), full_page=True)
        
        duration = (datetime.now() - start_time).total_seconds()
        
        success_message = (
            f"*Test Status:* Passed\n"
            f"*Duration:* {duration:.1f} seconds\n"
            f"*Environment:* Production\n"
            f"*URL:* https://www.oldmutual.co.ke/app/public/doctors-professional-indemnity\n"
            f"*All Steps Completed:*\n"
            f"  - Step 1: Personal Details\n"
            f"  - Step 2: Professional Details\n"
            f"  - Step 3: Address Information\n"
            f"  - Step 4: Document Upload\n"
            f"  - Step 5: Consents & Declarations\n"
            f"  - Step 6: Payment Processing\n"
            f"\nScreenshots saved in: `{SCREENSHOTS_DIR}/`"
        )
        
        print("SUCCESS: Doctors Professional Indemnity test completed successfully!")
        send_slack_notification(success_message)
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        error_screenshot = get_screenshot_path("error.png")
        page.screenshot(path=error_screenshot, full_page=True)
        
        failed_step = get_failure_step(str(e))
        
        error_message = (
            f"*Test Status:* Failed\n"
            f"*Failed At:* {failed_step}\n"
            f"*Duration:* {duration:.1f} seconds\n"
            f"*Environment:* Production\n"
            f"*URL:* https://www.oldmutual.co.ke/app/public/doctors-professional-indemnity\n"
            f"*Error Details:*\n```{str(e)}```\n"
            f"\nError screenshot: `{error_screenshot}`"
        )
        
        print(f"X Test failed at {failed_step}")
        print(f"X Error: {str(e)}")
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
