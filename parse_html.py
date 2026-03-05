import re

html = open("lengo_dom_headed.html", "r", encoding="utf-8").read()

# Very basic extraction of text inside tags
# We know the user says there are 3 options on the landing page
text_snippets = re.findall(r'>([^<]+)<', html)
clean_snippets = [s.strip() for s in text_snippets if s.strip()]

print("Visible text segments:")
for snippet in clean_snippets:
    if len(snippet) > 3: # filter out short noise
        print(snippet)
        
# Let's also look for any form inputs
inputs = re.findall(r'<input[^>]+>', html)
print("\nInputs found:", len(inputs))
for inp in inputs[:10]:
    print(inp)
    
buttons = re.findall(r'<button[^>]*>(.*?)</button>', html, re.IGNORECASE)
print("\nButtons found:", len(buttons))
for btn in buttons[:10]:
    print(btn)
