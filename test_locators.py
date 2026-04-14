from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://oldmutual.co.ke/app/public/lengo-digital-savings")
    page.wait_for_timeout(5000)
    
    print("Testing locators:")
    
    try:
        page.get_by_test_id("firstName").click(timeout=3000)
        print("[SUCCESS] get_by_test_id('firstName') worked!")
    except Exception as e:
        print(f"[FAIL] get_by_test_id failed")
        
    try:
        page.locator('omk-text-field[name="firstName"]').click(timeout=3000)
        print("[SUCCESS] locator('omk-text-field[name=\"firstName\"]') worked!")
    except Exception as e:
        print(f"[FAIL] locator failed")

    try:
        page.get_by_role("textbox", name="First Name").click(timeout=3000)
        print("[SUCCESS] get_by_role worked!")
    except Exception as e:
        print(f"[FAIL] get_by_role failed")

    browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        run(p)
