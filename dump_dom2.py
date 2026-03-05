from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://oldmutual.co.ke/app/public/lengo-digital-savings")
    page.wait_for_timeout(5000)
    
    html = page.content()
    with open("lengo_dom_headed.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("DOM saved to lengo_dom_headed.html.")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
