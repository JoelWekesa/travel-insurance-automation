from playwright.sync_api import sync_playwright
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    print("Navigating...")
    page.goto("https://oldmutual.co.ke/app/public/lengo-digital-savings")
    print("Waiting 10s...")
    page.wait_for_timeout(10000)
    
    html = page.content()
    with open("lengo_dom.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("DOM saved to lengo_dom.html.")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
