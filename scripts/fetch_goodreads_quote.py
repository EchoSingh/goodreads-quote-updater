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
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # Locate the quote container
    quote_block = soup.select_one("div.quoteDetails")
    if not quote_block:
        raise RuntimeError("❌ Quote container not found on the page")

    # Extract quote text
    text_div = quote_block.find("div", class_="quoteText")
    if not text_div:
        raise RuntimeError("❌ Quote text element not found")
    
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

    # GitHub-compatible formatting without CSS
    # ========================================
    # 1. Use standard markdown for the quote
    # 2. For circular image: Use a service that provides circular images
    #    or create the circle effect using GitHub's avatar rendering
    # ========================================
    
    markdown_content = f"> {quote_text}\n\n"
    markdown_content += f"<p align=\"right\"><em>― {author}</em></p>\n\n"

    # Add author image with GitHub's avatar rendering
    if author_img_url:
        # GitHub automatically renders square images as circles when using ?size= parameter
        # We'll use the image URL directly with size parameters
        circle_img_url = f"{author_img_url.split('?')[0]}?size=200"
        
        markdown_content += f"<div align=\"center\">\n\n"
        markdown_content += f"[![]({circle_img_url})]"
        markdown_content += f"(https://www.goodreads.com/user/show/191174534-aditya-singh)\n\n"
        markdown_content += "</div>"

    # Update README.md
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate markers and replace content
    start_idx = content.index(START_MARKER) + len(START_MARKER)
    end_idx = content.index(END_MARKER)
    
    new_content = (
        content[:start_idx] +
        "\n\n" + markdown_content.strip() + "\n\n" +
        content[end_idx:]
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ README updated successfully!")
    print(f"ℹ️ Quote: {quote_text[:50]}...")
    print(f"ℹ️ Author: {author}")
    print(f"ℹ️ Image URL: {circle_img_url if author_img_url else 'None'}")

except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
