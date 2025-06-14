import os
import requests
from bs4 import BeautifulSoup

URL = os.getenv("PROFILE_URL")

headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(URL, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# Find quote block (latest shared quote)
quote_block = soup.select_one("div.quoteDetails")
if not quote_block:
    raise RuntimeError("Quote not found on page.")

# Quote text
text_div = quote_block.find("div", class_="quoteText")
text = text_div.get_text(separator=" ").split("Delete")[0].strip()

# Clean and split into quote and author
parts = text.split("”")
if len(parts) >= 2:
    quote = parts[0].strip() + "”"
    author = parts[1].replace("—", "").strip()
else:
    quote = text
    author = ""

# Author image
img_tag = quote_block.find("img")
author_img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

# Markdown formatting
quote_md = f'> {quote}\n> — *{author}*\n\n'
if author_img_url:
    quote_md += f'<img src="{author_img_url}" alt="{author}" width="100"/>'

# Update README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start = "<!-- QUOTE_START -->"
end = "<!-- QUOTE_END -->"
new_content = (
    content[: content.index(start) + len(start)]
    + "\n\n"
    + quote_md
    + "\n"
    + content[content.index(end) :]
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
