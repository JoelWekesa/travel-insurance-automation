from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    )
    page = context.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    page.goto('https://oldmutual.co.ke/app/public/lengo-digital-savings')
    page.wait_for_timeout(8000)
    
    page.screenshot(path='screenshots/landing_top.png')
    page.screenshot(path='screenshots/landing_full.png', full_page=True)
    
    # Let's extract all text content from the body to see what text exists
    text = page.locator("body").inner_text()
    print("PAGE TEXT:")
    print("="*40)
    print(text[:1000])  # Just print the first 1000 chars to see what's physically there
    print("="*40)
    
    browser.close()

with sync_playwright() as p:
    run(p)
