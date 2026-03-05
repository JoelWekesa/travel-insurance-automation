import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

try:
    response = requests.get("https://oldmutual.co.ke/app/public/lengo-digital-savings", headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        html = response.text
        # Simple extraction
        import re
        text_snippets = re.findall(r'>([^<]+)<', html)
        clean_snippets = [s.strip() for s in text_snippets if s.strip()]
        
        print("\nVisible text segments on landing page:")
        for snippet in clean_snippets:
            if len(snippet) > 3: 
                print(snippet)
    else:
        print(response.text[:500])
except Exception as e:
    print(f"Error: {e}")
