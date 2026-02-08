import os
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright, expect
import requests
import time

# -----------------------------
# Slack Notification Function
# -----------------------------
def send_slack_notification(status: str, screenshot_path: str | None, step: str):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("[Slack] No webhook URL configured")
        return
    message = {"text": f"Afya Imara Test Alert\nStatus: {status}\nStep: {step}"}
    if screenshot_path:
        message["attachments"] = [{"image_url": screenshot_path, "text": step}]
    try:
        response = requests.post(webhook_url, json=message)
        if response.status_code != 200:
            print(f"[Slack] Failed to send: {response.text}")
    except Exception as e:
        print(f"[Slack] Slack Exception: {e}")

# -----------------------------
# Screenshot Function
# -----------------------------
def save_screenshot(page, step_name: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{timestamp}_{step_name}.png"
    page.screenshot(path=filename, full_page=True)
    print(f"[Screenshot] Saved: {filename}")
    return filename

# -----------------------------
# Click helper with tooltip handling
# -----------------------------
def safe_click(page, selector: str | None = None, role_name: str | None = None):
    """Try to click element safely, closing tooltips if blocking."""
    try:
        if selector:
            page.locator(selector).click(timeout=10000)
        elif role_name:
            page.get_by_role("button", name=role_name).click(timeout=10000)
    except:
        # Attempt to close tooltips or popups
        tooltips = page.locator("[role='tooltip']")
        if tooltips.count() > 0:
            for i in range(tooltips.count()):
                try:
                    tooltips.nth(i).evaluate("el => el.style.display = 'none'")
                except:
                    pass
        time.sleep(0.5)
        # Retry click
        if selector:
            page.locator(selector).click(timeout=10000)
        elif role_name:
            page.get_by_role("button", name=role_name).click(timeout=10000)

# -----------------------------
# Main Afya Imara Flow
# -----------------------------
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Step 1: Open page
        page.goto("https://www.oldmutual.co.ke/app/public/afya-imara?product=1")
        save_screenshot(page, "01_open_page")
        send_slack_notification("Passed", None, "Open Page")

        # Step 2: Personal Info
        page.get_by_role("textbox", name="Your name").fill("Faith Tester")
        page.get_by_role("textbox", name="Email").fill("wangarinjeri77@gmail.com")
        page.get_by_role("spinbutton", name="Phone number").fill("0742587248")
        safe_click(page, role_name="Continue")
        save_screenshot(page, "02_personal_info")
        send_slack_notification("Passed", None, "Personal Info")

        # Step 3: Age & spouse
        page.get_by_role("textbox", name="What is your age?").fill("26")
        page.get_by_test_id("spouseIncluded").locator("#input").check()
        safe_click(page, role_name="Continue")
        page.get_by_role("textbox", name="Spouse / Partner Age").fill("25")
        safe_click(page, role_name="Continue")
        save_screenshot(page, "03_age_spouse")
        send_slack_notification("Passed", None, "Age & Spouse Info")

        # Step 4: Limits & Plans
        page.get_by_test_id("afyaImaraInpatientLimit").locator("#label").click()
        page.locator("omk-select-option:nth-child(6) > md-select-option > .primary-text-wrapper").first.click()
        page.get_by_test_id("afyaImaraOutpatientLimit").locator("#label").click()
        page.locator("div:nth-child(3) > omk-select > omk-select-option:nth-child(6) > md-select-option > #item > md-item").click()
        page.locator("#rescue-plus").check()
        safe_click(page, role_name="Continue")
        save_screenshot(page, "04_limits_plan")
        send_slack_notification("Passed", None, "Limits & Plan Selection")

        # Step 5: Traveller Info & Documents
        # fill full name, DOB, ID, SHA, KRA
        # upload files
        # Continue
        # ... follow same Travel.py pattern
        save_screenshot(page, "05_traveller_docs")
        send_slack_notification("Passed", None, "Traveller Info & Documents")

        # Step 6: Consent & Payment
        page.get_by_test_id("consentForNewProductsAndServices").locator("#input").check()
        page.get_by_test_id("termsAndConditions").locator("#input").check()
        safe_click(page, role_name="Continue")
        safe_click(page, role_name="Process Payment")
        save_screenshot(page, "06_payment")
        send_slack_notification("Passed", None, "Payment Processed")

    except Exception as e:
        screenshot = save_screenshot(page, "error")
        send_slack_notification("Failed", screenshot, "Error Encountered")
        print(f"[Error] {e}")

    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
