from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    )
    page = context.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    responses = []
    page.on("response", lambda response: responses.append(response) if "api" in response.url or "graphql" in response.url or response.status >= 400 else None)
    
    page.goto('https://oldmutual.co.ke/app/public/lengo-digital-savings')
    page.wait_for_timeout(5000)
    
    # Run through the steps fast...
    # Step 1
    page.get_by_role("textbox", name="First Name").fill("tester")
    page.get_by_role("textbox", name="Surname").fill("tester")
    page.get_by_role("textbox", name="Phone Number").fill("0712345678")
    page.get_by_role("textbox", name="Email").fill("kareynjeri@gmail.com")
    page.get_by_role("button", name="Continue").click(force=True)
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Continue").click(force=True)
    page.wait_for_load_state("networkidle")
    
    # Step 2
    page.get_by_role("button", name="SELECT").nth(0).click(force=True)
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Continue").click(force=True)
    page.wait_for_timeout(3000)
    
    # Step 3
    # Use keyboard to fill required dropdowns
    reqs = ["Title*", "Gender*", "Nationality*", "Occupation*", "Source of funds*", "Income range*"]
    for lbl in reqs:
        try:
            loc = page.locator("omk-select").filter(has_text=lbl).first
            loc.evaluate("el => el.scrollIntoView({block: 'center'})")
            page.wait_for_timeout(200)
            loc.click(force=True)
            page.wait_for_timeout(500)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(200)
            page.keyboard.press("ArrowDown")
            page.wait_for_timeout(200)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
        except Exception as e:
            pass
            
    page.get_by_role("textbox", name="Date of birth").fill("12/12/2000")
    page.get_by_role("textbox", name="National ID/Passport number").fill("123123123")
    page.get_by_role("textbox", name="Full Postal Address").fill("Nairobi")
    page.get_by_role("textbox", name="KRA number").fill("A123123123K")
    page.get_by_role("button", name="Continue").click(force=True)
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Continue").click(force=True)
    page.wait_for_load_state("networkidle")
    
    # Step 4
    page.get_by_role("button", name="Add Beneficiary").click(force=True)
    page.wait_for_timeout(500)
    page.get_by_role("textbox", name="First name").fill("test")
    page.get_by_role("textbox", name="Last name").fill("test")
    
    loc = page.locator("omk-select").first
    loc.evaluate("el => el.scrollIntoView({block: 'center'})")
    page.wait_for_timeout(200)
    loc.click(force=True)
    page.wait_for_timeout(500)
    page.keyboard.press("ArrowDown")
    page.wait_for_timeout(200)
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)

    page.get_by_role("textbox", name="Mobile number").fill("0712345678")
    page.get_by_role("textbox", name="Email address").fill("kareynjeri@gmail.com")
    page.get_by_role("textbox", name="Full postal address").fill("test")
    page.get_by_role("slider").fill("100")
    
    page.get_by_role("button", name="Continue").click(force=True)
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Continue").click(force=True)
    page.wait_for_load_state("networkidle")
    
    # Step 5
    page.locator("#upload-nationalId input[type='file']").set_input_files("download.jpeg")
    page.wait_for_timeout(500)
    page.locator("#upload-kraPin input[type='file']").set_input_files("download.jpeg")
    page.wait_for_timeout(500)
    
    print("Clicking Continue on Step 5...")
    # Clear previous responses
    responses.clear()
    page.get_by_role("button", name="Continue").click(force=True)
    page.wait_for_timeout(5000)
    
    print("Recent network responses:")
    for r in responses:
        print(f"[{r.status}] {r.url}")
        try:
            print("Response:", r.text()[:200])
        except:
            pass
            
    browser.close()

with sync_playwright() as p:
    run(p)
