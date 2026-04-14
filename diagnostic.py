import re
from playwright.sync_api import Playwright, sync_playwright
import os
from datetime import datetime, timedelta

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    print("Navigating to Travel Insurance...")
    page.goto("https://www.oldmutual.co.ke/app/public/travel-insurance")
    page.wait_for_load_state("networkidle")
    
    # Handle unexpected window dialogs (e.g., Double Insurance alert)
    def handle_dialog(dialog):
        print(f"Native Dialog appeared: '{dialog.message}'. Accepting...")
        dialog.accept()
    page.on("dialog", handle_dialog)
    
    print("Clicking Retail...")
    page.get_by_test_id("retail").get_by_role("button", name="Select Cover").click()
    page.wait_for_timeout(2000)
    
    for i in range(1, 4):
        print(f"\n--- Checking Page {i} ---")
        page.screenshot(path=f"screenshots/diag_page{i}_before.png", full_page=True)
        
        # Determine what's on the page
        if page.get_by_role("textbox", name="Fullname").is_visible():
            print("Page is Personal Info. Filling...")
            page.get_by_role("textbox", name="Fullname").fill("Test User")
            page.get_by_role("textbox", name="Phone").fill("0712345678")
            page.get_by_role("textbox", name="Email").fill("test@user.com")
            
            try:
                page.get_by_role("button", name="Close tooltip").click(timeout=1000)
            except:
                pass
                
        elif page.locator(".inner-circle").first.is_visible():
            print("Page is Travel Details (Get a quote). Filling...")
            page.locator(".inner-circle").first.click()
            page.wait_for_timeout(500)
            
            try:
                page.get_by_placeholder(re.compile("Traveller", re.IGNORECASE)).first.fill("01/01/1990")
            except:
                page.get_by_role("textbox", name=re.compile("Traveller", re.IGNORECASE)).first.fill("01/01/1990")
            page.wait_for_timeout(500)
            
            page.locator("omk-select").click()
            page.wait_for_timeout(500)
            page.locator("omk-select-option:nth-child(5) > md-select-option").click()
            page.wait_for_timeout(500)
            
            departure_date = (datetime.now() + timedelta(days=5)).strftime("%d/%m/%Y")
            return_date = (datetime.now() + timedelta(days=6)).strftime("%d/%m/%Y")
            
            page.get_by_role("textbox", name="Departure Date").fill(departure_date)
            page.wait_for_timeout(1000)
            
            # CHECK DOUBLE INSURANCE HERE
            page.screenshot(path=f"screenshots/diag_page{i}_double_ins.png", full_page=True)
            try:
                if page.get_by_role("radio", name="No").is_visible():
                    print("Found Double Insurance 'No' radio. Clicking...")
                    page.get_by_role("radio", name="No").click()
                    page.wait_for_timeout(500)
            except:
                pass
                
            page.get_by_role("textbox", name="Return Date").fill(return_date)
            page.wait_for_timeout(500)
            
        elif page.get_by_role("button", name="Proceed to buy").is_visible() or page.get_by_text("Choose a retail plan").is_visible() or page.get_by_text("Limits in USD").is_visible() or page.get_by_text("Premium Payable").is_visible():
            print("Page is Select a plan or Proceed. Clicking next...")
        else:
            print("Unknown page!")
            page.screenshot(path=f"screenshots/diag_page{i}_unknown.png", full_page=True)
            
        page.screenshot(path=f"screenshots/diag_page{i}_after.png", full_page=True)
        
        # Try to click Continue or Proceed
        try:
            btn = page.locator("button:has-text('Proceed to buy'), button:has-text('Continue'), button:has-text('Proceed')").last
            if btn.is_visible():
                print("Clicking Continue/Proceed...")
                btn.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(3000)
            else:
                # specifically for standard continue button
                btn_role = page.get_by_role("button", name="Continue", exact=True).last
                if btn_role.is_visible():
                    print("Clicking Continue via role...")
                    btn_role.click()
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(3000)
        except Exception as e:
            print("Could not click forward:", e)

    print("Done tracing!")
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
