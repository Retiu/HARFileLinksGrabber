"""
Extract all URLs from a HAR (HTTP Archive) file and save them to a text file.
Usage: python extract_har_links.py
"""

import json
import re
from pathlib import Path

HAR_FILE = r"!!CHANGE FILE NAME!!!.har"
OUTPUT_FILE = r"HARFileLinksGrabber_output.txt"

def extract_urls_from_har(har_path):
    urls = set()

    with open(har_path, "r", encoding="utf-8", errors="replace") as f:
        data = json.load(f)

    entries = data.get("log", {}).get("entries", [])
    for entry in entries:
        # Request URL
        req_url = entry.get("request", {}).get("url", "")
        if req_url:
            urls.add(req_url)

        # Response redirect URL
        redirect = entry.get("response", {}).get("redirectURL", "")
        if redirect:
            urls.add(redirect)

        # Scan response body text for any URLs
        content = entry.get("response", {}).get("content", {})
        body_text = content.get("text", "")
        if body_text:
            found = re.findall(r'https?://[^\s\'"<>)\\]+', body_text)
            urls.update(found)

    return sorted(urls)

def main():
    print(f"Reading: {HAR_FILE}")
    urls = extract_urls_from_har(HAR_FILE)
    print(f"Found {len(urls)} unique URLs")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# URLs extracted from HAR file\n")
        f.write(f"# Total: {len(urls)}\n\n")
        for url in urls:
            f.write(url + "\n")

    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
