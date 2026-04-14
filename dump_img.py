from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://oldmutual.co.ke/app/public/lengo-digital-savings")
    page.wait_for_timeout(10000)
    
    page.screenshot(path="screenshots/landing_page_dump.png", full_page=True)
    print("Screenshot saved to screenshots/landing_page_dump.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
