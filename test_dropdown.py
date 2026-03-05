from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    )
    page = context.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    page.goto('https://oldmutual.co.ke/app/public/lengo-digital-savings')
    page.wait_for_timeout(5000)
    
    page.get_by_role('textbox', name='First Name').fill('tester')
    page.get_by_role('textbox', name='Surname').fill('tester')
    page.get_by_role('textbox', name='Phone Number').fill('0712345678')
    page.get_by_role('textbox', name='Email').fill('kareynjeir@gmail.com')
    
    page.get_by_role('button', name='Continue').click(force=True)
    page.wait_for_timeout(500)
    page.get_by_role('button', name='Continue').click(force=True)
    page.wait_for_timeout(5000)

    print('Focusing Title dropdown...')
    dropdown = page.locator('omk-select').first
    dropdown.click(force=True)
    page.wait_for_timeout(1000)
    
    # Send ArrowDown and Enter
    page.keyboard.press('ArrowDown')
    page.wait_for_timeout(500)
    page.keyboard.press('Enter')
    page.wait_for_timeout(1000)
    
    page.screenshot(path='screenshots/dropdown_keyboard.png', full_page=True)
    print('Saved to dropdown_keyboard.png')
    browser.close()

with sync_playwright() as p:
    run(p)
