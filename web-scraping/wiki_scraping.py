"""IS 310: Compare Minecraft Wiki articles about animal mobs."""

import csv
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://minecraft.wiki"
CATEGORY_URL = BASE_URL + "/w/Category:Animal_mobs"
ROBOTS_URL = BASE_URL + "/robots.txt"
OUTPUT_FILE = Path(__file__).resolve().parent / "minecraft_animal_mobs.csv"
MAX_MOBS = 10
REQUEST_DELAY = 5

USER_AGENT = "is310-course-scraper/1.0 (student project; arp14@illinois.edu)"
HEADERS = {"User-Agent": USER_AGENT}


def check_robots():
    """Read the site's scraping rules before accessing wiki pages."""
    try:
        response = requests.get(ROBOTS_URL, headers=HEADERS, timeout=20)
    except requests.RequestException as error:
        print(f"Could not check robots.txt: {error}")
        return None

    if response.status_code != 200:
        print(f"Could not check robots.txt. HTTP status: {response.status_code}")
        return None

    rules = RobotFileParser()
    rules.parse(response.text.splitlines())
    return rules


def get_page(url, robots):
    """Fetch a permitted HTML page with a delay between requests."""
    if not robots.can_fetch(USER_AGENT, url):
        print(f"Robots.txt disallows this page: {url}")
        return None

    time.sleep(REQUEST_DELAY)
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
    except requests.RequestException as error:
        print(f"Could not reach {url}: {error}")
        return None

    if response.status_code != 200:
        print(f"Skipping {url}. HTTP status: {response.status_code}")
        return None

    if "text/html" not in response.headers.get("Content-Type", "").lower():
        print(f"Skipping {url}. Response was not an HTML page.")
        return None

    return BeautifulSoup(response.text, "html.parser")


def get_mob_links(category_page):
    """Get up to 10 animal mob links listed on the wiki category page."""
    section = category_page.find(id="mw-pages")
    if section is None:
        print("Could not find the page list on the category page.")
        return []

    mobs = []
    seen_urls = set()
    for link in section.select("li a[href]"):
        name = link.get_text(" ", strip=True)
        url = urljoin(BASE_URL, link["href"])
        path = urlparse(url).path

        if not name or name in ("Animal", "Chicken Jockey"):
            continue
        if not url.startswith(BASE_URL + "/w/") or ":" in path[len("/w/"):]:
            continue
        if url in seen_urls:
            continue

        seen_urls.add(url)
        mobs.append({"mob_name": name, "page_url": url})
        if len(mobs) >= MAX_MOBS:
            break

    return mobs


def analyze_mob(mob, robots):
    """Measure article length and internal wiki links."""
    soup = get_page(mob["page_url"], robots)
    if soup is None:
        return None

    content = soup.select_one("#mw-content-text .mw-parser-output")
    if content is None:
        print(f"Skipping {mob['mob_name']}. Article content was not found.")
        return None

    text = content.get_text(" ", strip=True)
    if not text:
        print(f"Skipping {mob['mob_name']}. Article text was empty.")
        return None

    internal_links = []
    for link in content.find_all("a", href=True):
        href = link["href"]
        absolute_url = urljoin(BASE_URL, href)
        if (
            absolute_url.startswith(BASE_URL + "/w/")
            and "#" not in href
            and "?" not in href
        ):
            internal_links.append(absolute_url)

    return {
        "mob_name": mob["mob_name"],
        "word_count": len(text.split()),
        "character_count": len(text),
        "internal_link_count": len(internal_links),
        "unique_internal_link_count": len(set(internal_links)),
        "page_url": mob["page_url"],
        "category_url": CATEGORY_URL,
    }


def save_csv(records):
    if not records:
        print("No articles were collected, so no CSV was created.")
        return

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved {len(records)} rows to {OUTPUT_FILE.name}")


def main():
    print("Checking Minecraft Wiki robots.txt...")
    robots = check_robots()
    if robots is None:
        return

    print("Getting Minecraft animal mobs...")
    category_page = get_page(CATEGORY_URL, robots)
    if category_page is None:
        return

    mobs = get_mob_links(category_page)
    print(f"Found {len(mobs)} mob pages to read.")

    results = []
    for mob in mobs:
        print(f"Reading {mob['mob_name']}...")
        record = analyze_mob(mob, robots)
        if record is not None:
            results.append(record)

    if results:
        print("\nResults sorted by word count:")
        for record in sorted(results, key=lambda row: row["word_count"], reverse=True):
            print(f"{record['mob_name']}: {record['word_count']} words, "
                  f"{record['internal_link_count']} internal links")

    save_csv(results)


if __name__ == "__main__":
    main()
