## Quote of the Day

<!-- QUOTE_START -->

<table><tr>
<td width="30%" align="center">
  <img src="https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/authors/1679568617i/30691._UX200_CR0,36,200,200_.jpg" alt="Adolf Hitler" width="150" style="border-radius:50%">
</td>
<td width="70%" valign="center">
  <p style="font-size: 16px; font-style: italic;">“Do not compare yourself to others. If you do so, you are insulting yourself.”</p>
  <p align="right" style="font-weight: bold;">― Adolf Hitler</p>
</td>
</tr></table>

<!-- QUOTE_END -->

# Goodreads Quote Updater

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white)

A Python script that automatically updates your GitHub profile README with your latest quote from Goodreads.

## Features

- Automatically fetches your featured quote from Goodreads
- Extracts quote text, author information, and author image
- Beautifully formats the quote in your README
- Scheduled daily updates via GitHub Actions
- Comprehensive error handling and logging
- Lightweight with minimal dependencies

## Setup

### Prerequisites
- Goodreads account with profile quotes
- GitHub account

### Installation

1. **Fork or clone this repository**
   ```bash
   git clone https://github.com/EchoSingh/goodreads-quote-updater.git
   cd goodreads-quote-updater
   ```

## Usage

### GitHub Actions Setup

1. Update the workflow file (`.github/workflows/update-readme.yml`) by Replacing `YOUR_USER_ID` with your actual Goodreads user ID
   ```yaml
   name: Update Goodreads Quote
   
   on:
     schedule:
       - cron: '0 6 * * *'  # Runs daily at 06:00 UTC
     workflow_dispatch:  # Allows manual triggering
   
   jobs:
     update-quote:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout repository
           uses: actions/checkout@v3
           
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.x'
             
         - name: Install dependencies
           run: pip install requests beautifulsoup4
           
         - name: Update quote
           env:
             PROFILE_URL: "https://www.goodreads.com/user/show/YOUR_USER_ID"
           run: python scripts/fetch_goodreads_quote.py
           
         - name: Commit changes
           run: |
             git config --global user.name "github-actions[bot]"
             git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
             git add README.md
             git commit -m "Update daily quote" || echo "No changes to commit"
             git push
   ```

## README Integration

Add these markers to your README.md where you want the quote to appear:
```markdown
<!-- QUOTE_START -->
<!-- QUOTE_END -->
```

The script will automatically update the content between these markers.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
