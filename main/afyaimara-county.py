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
            "text": f"{emoji} Afya Imara County Test - {emoji}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} Afya Imara County Test Alert"
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
        # Try to close tooltip first
        page.locator("#zs-fl-tip").evaluate("el => el.style.display = 'none'")
        print("ℹ️ Zoho tooltip hidden")
    except:
        pass
    
    try:
        # Try to minimize chat
        zoho_btn = page.get_by_role("button", name="Minimize live chat window")
        if zoho_btn.is_visible(timeout=1000):
            zoho_btn.click()
            print("ℹ️ Zoho chat minimized")
    except:
        pass
    
    try:
        # Hide entire Zoho widget as last resort
        page.locator("[data-id='zsalesiq']").evaluate("el => el.style.display = 'none'")
        print("ℹ️ Zoho widget hidden")
    except:
        pass

def run_afya_imara_county():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        start_time = datetime.now()
        current_step = ""
        
        try:
            # Step 1: Navigate to Afya Imara County
            current_step = "Step 1: Navigate to Afya Imara County"
            print(f"{current_step}")
            page.goto("https://www.oldmutual.co.ke/personal/insure/health-insurance/", timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(5000)
            
            # Scroll to find BUY ONLINE links
            page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            page.wait_for_timeout(2000)
            
            # Find and click the 5th BUY ONLINE link (index 4)
            buy_links = page.get_by_role("link", name="BUY ONLINE")
            count = buy_links.count()
            print(f"Found {count} BUY ONLINE links")
            
            if count > 4:
                buy_links.nth(4).scroll_into_view_if_needed()
                page.wait_for_timeout(1000)
                buy_links.nth(4).click()
            else:
                print(f"Not enough BUY ONLINE links, clicking last one")
                buy_links.last.click()
            
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            close_zoho_if_present(page)
            page.screenshot(path=get_screenshot_path("1_navigate.png"), full_page=True)
            
            # Step 2: Principal Details
            current_step = "Step 2: Principal Details"
            print(f"{current_step}")
            page.get_by_role("textbox", name="Your name").fill("test tes")
            page.get_by_role("textbox", name="Email").fill("faith.njeri@oldmutual.com")
            page.get_by_role("spinbutton", name="Phone number").fill("0742587248")
            page.wait_for_timeout(1000)
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("2_principal.png"), full_page=True)
            
            # Step 3: Family Setup
            current_step = "Step 3: Family Setup"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_role("textbox", name="What is your age?").fill("45")
            page.get_by_test_id("spouseIncluded").locator("#input").check()
            page.get_by_test_id("childrenIncluded").locator("#input").check()
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("3_family.png"), full_page=True)
            
            # Step 4: Family Ages
            current_step = "Step 4: Family Ages"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_role("textbox", name="Spouse / Partner Age").fill("40")
            page.get_by_role("textbox", name="Child").fill("2")
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("4_ages.png"), full_page=True)
            
            # Step 5: Cover Options
            current_step = "Step 5: Cover Options"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.locator(".display-value").first.click()
            page.get_by_role("menu").get_by_text("250,000").click()
            page.wait_for_timeout(500)
            page.locator("div:nth-child(3) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page.get_by_role("menu").get_by_text("50,000").click()
            page.wait_for_timeout(500)
            page.locator(".outer-circle").first.click()
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("5_cover.png"), full_page=True)
            
            # Step 6: Not Referred
            current_step = "Step 6: Not Referred"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            
            # Select "No" for not referred
            page.locator(".outer-circle").nth(1).click()
            page.wait_for_timeout(500)
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("6_not_referred.png"), full_page=True)
            
            # Step 7: Quote Review
            current_step = "Step 7: Quote Review"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("7_quote.png"), full_page=True)
            
            # Step 8: Select Add-ons
            current_step = "Step 8: Select Add-ons"
            print(f"{current_step}")
            page.wait_for_timeout(2000)
            
            # Check if Select buttons exist, if not skip this step
            select_buttons = page.get_by_role("button", name="Select")
            if select_buttons.count() > 0:
                if select_buttons.count() > 2:
                    select_buttons.nth(2).click()
                    page.wait_for_timeout(500)
                if select_buttons.count() > 1:
                    select_buttons.nth(1).click()
                    page.wait_for_timeout(500)
            
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("8_addons.png"), full_page=True)
            
            # Step 9: Confirm Selection
            current_step = "Step 9: Confirm Selection"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("9_confirm.png"), full_page=True)
            
            # Step 10: Principal Member Details
            current_step = "Step 10: Principal Member Details"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_role("textbox", name="Date of Birth").fill("12/12/2000")
            page.locator(".display-value").first.click()
            page.get_by_role("menu").get_by_text("Female").click()
            page.wait_for_timeout(500)
            page.locator("div:nth-child(4) > omk-select > .anchor-wrapper > #materialField > .display-value").click()
            page.get_by_role("menu").get_by_text("Married").click()
            page.wait_for_timeout(500)
            page.get_by_role("textbox", name="ID/Passport Number").fill("786372728")
            page.get_by_role("textbox", name="Social Health Authority (SHA").fill("9732987892")
            page.get_by_role("textbox", name="KRA Pin Number").fill("A123456789k")
            page.get_by_role("textbox", name="Country").fill("kenya")
            page.get_by_role("textbox", name="Postal Address").fill("00100")
            page.get_by_role("textbox", name="Postal Code").fill("10292")
            page.get_by_role("textbox", name="City/County/Town").fill("nairobi")
            page.locator("#upload-nationalId input#file-upload").first.set_input_files("../download.jpeg")
            page.wait_for_timeout(1000)
            page.locator("#upload-kraPin input#file-upload").first.set_input_files("../download.jpeg")
            page.wait_for_timeout(1000)
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("10_principal.png"), full_page=True)
            
            # Step 11: Spouse Details
            current_step = "Step 11: Spouse Details"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_role("textbox", name="Full Name").fill("test test")
            page.get_by_role("textbox", name="Date of Birth").fill("12/12/2000")
            page.get_by_role("textbox", name="ID/Passport Number").fill("3868633")
            page.get_by_role("textbox", name="Social Health Authority (SHA").fill("3798738978")
            page.get_by_role("textbox", name="KRA Pin Number").fill("A123456789h")
            page.get_by_role("spinbutton", name="Phone Number").fill("0742587248")
            page.get_by_role("textbox", name="Email Address").fill("wangarinjeri77@gmail.com")
            page.get_by_role("textbox", name="Country").fill("kenya")
            page.get_by_role("textbox", name="Postal Address").fill("00100")
            page.get_by_role("textbox", name="Postal Code").fill("29882")
            page.get_by_role("textbox", name="City/County/Town").fill("test")
            page.locator("#upload-nationalId input#file-upload").first.set_input_files("../download.jpeg")
            page.wait_for_timeout(1000)
            page.locator("#upload-kraPin input#file-upload").first.set_input_files("../download.jpeg")
            page.wait_for_timeout(1000)
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("11_spouse.png"), full_page=True)
            
            # Step 12: Child Details
            current_step = "Step 12: Child Details"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_role("textbox", name="Full Name").fill("babay tasha")
            page.get_by_role("textbox", name="Date of Birth").fill("12/12/2025")
            page.get_by_role("textbox", name="Social Health Authority (SHA").fill("7663637")
            page.get_by_role("textbox", name="Birth Certificate Number").fill("6767673663")
            page.locator("#upload-birthCertificate-0 input#file-upload").first.set_input_files("../download.jpeg")
            page.wait_for_timeout(1000)
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("12_child.png"), full_page=True)
            
            # Step 13: Review Details
            current_step = "Step 13: Review Details"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("13_review.png"), full_page=True)
            
            # Step 14: Terms & Conditions
            current_step = "Step 14: Terms & Conditions"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_test_id("consentForNewProductsAndServices").locator("#input").check()
            page.get_by_test_id("consentForProductsAndServicesRelatedWithMyPolicy").locator("#input").check()
            page.get_by_test_id("termsAndConditions").locator("#input").check()
            page.locator("#ke-childDataProcessingConsent-0 > .sc-omk-radio.hydrated > .outer-circle > .inner-circle").click()
            page.locator(".outer-circle").first.click()
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("14_terms.png"), full_page=True)
            
            # Step 15: Next of Kin
            current_step = "Step 15: Next of Kin"
            print(f"{current_step}")
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Next of Kin").click()
            page.wait_for_timeout(500)
            page.get_by_role("textbox", name="First name").fill("test ")
            page.get_by_role("textbox", name="Last name").fill("test")
            page.get_by_role("textbox", name="National ID Number").fill("376367367")
            page.get_by_role("textbox", name="Phone Number").fill("0742587248")
            page.get_by_role("textbox", name="Email").fill("faith.njeri@oldmutual.com")
            page.get_by_role("textbox", name="Relationship").fill("sister")
            page.get_by_role("textbox", name="Full Postal Address").fill("78378")
            close_zoho_if_present(page)
            page.get_by_role("button", name="Continue").click(force=True)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=get_screenshot_path("15_nextofkin.png"), full_page=True)
            
            # Step 16: Payment
            current_step = "Step 16: Payment Processing"
            print(f"{current_step}")
            page.wait_for_timeout(2000)
            page.screenshot(path=get_screenshot_path("16_payment.png"), full_page=True)
            
            # Success
            duration = (datetime.now() - start_time).total_seconds()
            success_message = (
                f"*Afya Imara County Test Passed!*\n"
                f"*Duration:* {duration:.1f} seconds\n\n"
                f"All 16 steps completed successfully!"
            )
            print(success_message)
            send_slack_notification(success_message)
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            error_traceback = traceback.format_exc()
            error_screenshot = get_screenshot_path("error.png")
            page.screenshot(path=error_screenshot, full_page=True)
            
            error_message = (
                f"*Afya Imara County Test Failed!*\n"
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
    run_afya_imara_county()
