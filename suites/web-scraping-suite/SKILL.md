---
name: web-scraping-suite
description: "Master unified web scraping & data extraction suite. Routes intelligently between Firecrawl (single-page/crawl/agent JSON), Apify (social media platforms), HasData (SERP/e-commerce), Skyvern (visual/behind-login), and Defuddle (clean markdown)."
use_when: "Extracting public web content or collecting data from an authorized source."
avoid_when: "Accessing private/login-gated data without authorization or violating site policy."
entry_inputs: "Target URLs, allowed scope, desired fields, rate limits, and output schema."
workflow: "Choose the least complex permitted method, collect bounded data, validate results."
verification: "Check source coverage, schema, errors, and compliance with access limits."
exit_output: "Structured output, source/provenance, and collection limitations."
category: "data-and-research"
tools:
  - firecrawl
  - apify
  - playwright
  - python
---

# Web Scraping Suite (Unified Master Skill)

A single command center for all web scraping, crawling, and data extraction needs.

## 1. Routing Decision Tree (Ponytail / YAGNI Principle)

Stop at the simplest tool that solves the problem:

```
[Need to scrape/extract web data]
   |
   +---> Is it a single doc / article / blog URL?
   |        └──> Use Firecrawl Scrape (`firecrawl-scrape`): returns clean markdown.
   |
   +---> Is it an entire documentation site or subdomain?
   |        └──> Use Firecrawl Crawl (`firecrawl-crawl`): recursive depth-limited crawl.
   |
   +---> Is it behind strict logins / complex multi-step forms / visual flows?
   |        └──> Use Skyvern or Playwright (`skyvern-browser-automation` / `playwright`).
   |
   +---> Is it a major social platform (Twitter/X, Instagram, TikTok, LinkedIn)?
   |        └──> Use Apify Actors (`apify-ultimate-scraper` / `agent-reach`): handles rotation & proxies.
   |
   +---> Do you need structured JSON matching a strict schema?
   |        └──> Use Firecrawl Agent (`firecrawl-agent`): autonomous schema-guided JSON extractor.
   |
   +---> Is it commercial SERP / Maps / Google Shopping / Amazon product data?
            └──> Use HasData (`hasdata-cli`): structured commerce API.
```

## 2. Integrated Grilling & GSD Phase Protocol

Before running heavy scraping:
- **Phase 1 (Spec/Grill):** Clarify exact fields needed, target URLs, rate limits, and output format (Markdown vs CSV vs JSON). Do not scrape entire websites when 1 page suffices.
- **Phase 2 (Plan & Probe):** Test 1 sample page first. Verify headers, anti-bot behavior, and rendered content before batch execution.
- **Phase 3 (Execute):** Run bounded extraction with strict page/item caps.
- **Phase 4 (Verify):** Verify schema completeness, missing nulls, and deduplication.

## 3. Quick Reference Recipes

### Recipe A: Single Page / Clean Markdown (Firecrawl)
```bash
# Extract single page to LLM-ready markdown
firecrawl scrape "https://example.com/docs"
```

### Recipe B: Batch Crawl Documentation
```bash
# Crawl docs subdirectory up to depth 3
firecrawl crawl "https://example.com/docs" --limit 50 --depth 3
```

### Recipe C: Social Platform Scraping (Apify)
```python
# When scraping Twitter/Instagram/LinkedIn, route to Apify Actors to avoid IP bans
# Load apify-ultimate-scraper workflow
```

### Recipe D: Raw Python Fallback (Minimalist Stdlib / BeautifulSoup)
```python
import urllib.request
from bs4 import BeautifulSoup

req = urllib.request.Request("https://example.com", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    soup = BeautifulSoup(resp.read(), "html.parser")
```
