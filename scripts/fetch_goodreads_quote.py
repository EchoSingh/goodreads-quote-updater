import os
import re
import requests
from bs4 import BeautifulSoup

URL = os.getenv("PROFILE_URL", "https://www.goodreads.com/user/show/191174534-aditya-singh")

headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(URL, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# Find the latest quote block
quote_block = soup.select_one("div.quoteDetails")
if not quote_block:
    raise RuntimeError("Quote not found.")

# Get the quote text
text_div = quote_block.find("div", class_="quoteText")
text = text_div.get_text(separator=" ").split("Delete")[0].strip()

# Extract quote and author
parts = text.split("”")
if len(parts) >= 2:
    quote = parts[0].strip() + "”"
    author_raw = parts[1]
    author = re.sub(r"[―–—]\s*", "", author_raw).strip()
else:
    quote = text
    author = ""

# Get author image URL if available
img_tag = quote_block.find("img")
author_img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

# Format in Markdown + HTML (JetBrains Mono using inline style)
quote_md = f"""
<div style="font-family: 'JetBrains Mono', monospace; font-size: 14px;">

> {quote}
> — *{author}*

</div>
"""

if author_img_url:
    quote_md += f'<img src="{author_img_url}" alt="{author}" width="100"/>'

# Replace content in README.md
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start = "<!-- QUOTE_START -->"
end = "<!-- QUOTE_END -->"

new_content = (
    content[: content.index(start) + len(start)]
    + "\n\n"
    + quote_md.strip()
    + "\n\n"
    + content[content.index(end):]
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
