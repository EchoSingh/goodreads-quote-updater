import json
import random
from datetime import datetime

# Load quotes
with open("quotes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

# Pick a random quote
quote = random.choice(quotes)
quote_text = quote["quote"]
author = quote["author"]

# Format it nicely
quote_block = f"> “{quote_text}”\n>\n> — *{author}*\n"

# Read README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Replace content between markers
start_tag = "<!-- QUOTE_START -->"
end_tag = "<!-- QUOTE_END -->"

start_idx = content.find(start_tag) + len(start_tag)
end_idx = content.find(end_tag)

new_content = content[:start_idx] + "\n" + quote_block + "\n" + content[end_idx:]

# Write back
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
