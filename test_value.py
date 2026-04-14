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
    
    # Page 1
    page.get_by_role('textbox', name='First Name').fill('tester')
    page.get_by_role('textbox', name='Surname').fill('tester')
    page.get_by_role('textbox', name='Phone Number').fill('0712345678')
    page.get_by_role('textbox', name='Email').fill('kareynjeir@gmail.com')
    page.get_by_role('button', name='Continue').click(force=True)
    page.wait_for_timeout(500)
    page.get_by_role('button', name='Continue').click(force=True)
    page.wait_for_timeout(5000)

    # Page 2 (Plan Select)
    page.get_by_role("button", name="SELECT").nth(0).click(force=True)
    page.wait_for_timeout(2000)
    # We must also fill the required amounts, otherwise Page 2 validation fails!
    # Ah! In the loop, I did this correctly! Let's replicate.
    freq = page.locator("omk-select").filter(has_text="Desired Frequency")
    if freq.is_visible():
        freq.locator("#label").click(force=True)
        page.wait_for_timeout(500)
        freq.locator("omk-select-option").nth(1).evaluate("el => el.click()") 
        page.wait_for_timeout(300)
    if page.get_by_role("spinbutton", name="Desired Contribution").is_visible():
        page.get_by_role("spinbutton", name="Desired Contribution").fill("30000")
        
    page.get_by_role('button', name='Continue').click(force=True)
    page.wait_for_timeout(3000)
    
    # Page 3 (Personal Details)
    print("Modifying dropdown value via JS...")
    dropdown = page.locator('omk-select').first
    
    # The first one is Title*. Let's set it to "Mr" using JS value property
    dropdown.evaluate("el => { el.value = 'Mr'; el.dispatchEvent(new Event('change')); el.dispatchEvent(new Event('input')); }")
    page.wait_for_timeout(2000)
    
    page.screenshot(path='screenshots/dropdown_js_value.png', full_page=True)
    print("Saved to dropdown_js_value.png")
    
    # Let's extract what text it currently shows on the label to see if it updated
    txt = dropdown.evaluate("el => el.shadowRoot ? el.shadowRoot.querySelector('#label').innerText : el.innerText")
    print(f"Dropdown displays: {txt}")
    
    browser.close()

with sync_playwright() as p:
    run(p)
