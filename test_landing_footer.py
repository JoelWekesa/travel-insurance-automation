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
    
    # Force hide the sticky footer and chatbot
    page.evaluate('''() => {
        // Find sticky footers and hide them
        const footers = document.querySelectorAll('.pb-\\\\[150px\\\\], .sticky, .fixed, omk-action-bar, [style*="position: fixed"], [style*="position: sticky"]');
        footers.forEach(f => f.style.display = 'none');
        const zsiq = document.getElementById('zsiq_float');
        if(zsiq) zsiq.style.display = 'none';
        
        // Also just scroll everything into view
        window.scrollTo(0, document.body.scrollHeight);
    }''')
    
    page.wait_for_timeout(2000)
    
    page.screenshot(path='screenshots/landing_no_footer.png', full_page=True)
    
    print('Saved to landing_no_footer.png')
    browser.close()

with sync_playwright() as p:
    run(p)
