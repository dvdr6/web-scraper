# 🌐 Offline Website Scraper CLI

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

A powerful, lightweight command-line tool written in Python to recursively crawl and download entire websites for offline viewing. It automatically mirrors the site structure and rewrites internal links to work locally without an internet connection.

## ✨ Features

- **Recursive Crawling**: Depth-controlled BFS algorithm to discover sub-pages.
- **Asset Management**: Automatically downloads HTML, CSS, JavaScript, Images, and Fonts.
- **Smart Rewriting**: Converts absolute and root-relative URLs into local relative paths.
- **Path Preservation**: Mirrors the original website's directory structure.
- **CSS Support**: Parses `@import` and `url()` references within stylesheets.
- **ZIP Export**: Optionally package the entire local mirror into a single ZIP file.
- **Polite Scraping**: Built-in delay to avoid overwhelming target servers.

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- `pip` package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/offline-scraper.git
   cd offline-scraper
   ```

2. Install dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```

### Usage

Basic usage to download a site:
```bash
python scraper.py https://example.com
```

Advanced usage with depth and ZIP export:
```bash
python scraper.py https://example.com --depth 5 --output my_mirror --zip
```

### Arguments

| Flag | Description | Default |
|------|-------------|---------|
| `url` | The starting URL to crawl | (Required) |
| `--depth N` | Maximum crawl depth | `3` |
| `--output DIR` | Name of the output folder | `website_dump` |
| `--zip` | Compress the output into a ZIP file | `False` |

## 📁 Output Structure

The tool generates a clean, mirrored directory structure:
```text
website_dump/
├── index.html
├── about/
│   └── index.html
├── css/
│   └── style.css
├── js/
│   └── app.js
└── images/
    └── logo.png
```

## 🛠️ Built With

- **Requests**: For robust HTTP networking.
- **BeautifulSoup4**: For precise HTML parsing and manipulation.
- **Urllib**: For smart URL normalization and joining.
- **Zipfile**: For efficient compression of mirrored assets.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Developed with ❤️ for the open-source community.*
