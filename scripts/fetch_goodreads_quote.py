import os
import re
import requests
from bs4 import BeautifulSoup

# Configuration
URL = os.getenv("PROFILE_URL", "https://www.goodreads.com/user/show/191174534-aditya-singh")
HEADERS = {"User-Agent": "Mozilla/5.0"}
README_PATH = "README.md"
START_MARKER = "<!-- QUOTE_START -->"
END_MARKER = "<!-- QUOTE_END -->"

try:
    # Fetch Goodreads profile
    res = requests.get(URL, headers=HEADERS)
    res.raise_for_status()  # Raise exception for HTTP errors
    soup = BeautifulSoup(res.text, "html.parser")

    # Locate the quote container
    quote_block = soup.select_one("div.quoteDetails")
    if not quote_block:
        raise RuntimeError("Quote container not found on the page")

    # Extract quote text
    text_div = quote_block.find("div", class_="quoteText")
    if not text_div:
        raise RuntimeError("Quote text element not found")
    
    # Clean and split quote text
    full_text = text_div.get_text(separator=" ", strip=True)
    quote_text = ""
    author = "Unknown"

    # Improved quote/author extraction using regex
    match = re.search(r'^(“.*?”|".*?")(.*?)$', full_text)
    if match:
        quote_text = match.group(1).strip()
        author_part = match.group(2).strip()
        # Extract author name by removing attribution prefixes
        author = re.sub(r'^[―–—\s]+', '', author_part).split('\n')[0].strip()
    else:
        # Fallback if regex fails
        quote_text = full_text.split('Delete')[0].strip()

    # Get author image (if available)
    img_tag = quote_block.find("img")
    author_img_url = img_tag['src'] if img_tag else None

    # Format output with circular author image
    html_content = f"""
<div style="font-family: 'JetBrains Mono', monospace; font-size: 14px;">

> {quote_text}
> <p style="text-align: right; margin-top: 10px; font-style: italic;">— {author}</p>

</div>
"""

    # Add circular image if available
    if author_img_url:
        html_content += f"""
<div style="display: flex; justify-content: center; margin-top: 20px;">
    <img 
        src="{author_img_url}" 
        alt="{author}" 
        width="120" 
        height="120"
        style="
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #e1e4e8;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        "
    >
</div>
"""

    # Update README.md
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate markers and replace content
    start_idx = content.index(START_MARKER) + len(START_MARKER)
    end_idx = content.index(END_MARKER)
    
    new_content = (
        content[:start_idx] +
        "\n\n" + html_content.strip() + "\n\n" +
        content[end_idx:]
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README updated successfully!")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
