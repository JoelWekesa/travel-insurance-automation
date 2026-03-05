from playwright.sync_api import sync_playwright
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    # Using a real browser User-Agent to bypass Cloudflare / 403 Forbidden
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
        }
    )
    page = context.new_page()
    print("Navigating...")
    # remove the webdriver property from navigator
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    response = page.goto("https://oldmutual.co.ke/app/public/lengo-digital-savings")
    print(f"Status Code: {response.status}")
    print("Waiting 10s...")
    page.wait_for_timeout(10000)
    
    # Save screenshot just to be sure we bypassed 403
    page.screenshot(path="screenshots/landing_page_bypassed.png", full_page=True)
    
    # Extract buttons
    print("\n--- Visible Buttons ---")
    buttons = page.locator("button, a").element_handles()
    count = 0
    for btn in buttons:
        if btn.is_visible():
            text = btn.inner_text().strip()
            if text:
                print(f"[{text}]")
                count += 1
    
    print(f"Found {count} visible buttons/links with text.")
    print("Screenshot saved to landing_page_bypassed.png.")
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
