import csv
import json
import os
import re
import time
from getpass import getpass
from pathlib import Path

import requests

# This IMDb ID comes from the OMDb example link used for this assignment.
IMDB_ID = "tt3896198"  # Guardians of the Galaxy Vol. 2
WIKIPEDIA_TITLE = "Guardians of the Galaxy Vol. 2"

OMDB_URL = "https://www.omdbapi.com/"
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "is310-movie-api-project/1.0 (arp14@illinois.edu)"}
OUTPUT_FOLDER = Path(__file__).resolve().parent


def get_json(url, params, name):
    """Make a request, check for errors, and return the JSON response."""
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=20)
    except requests.RequestException as error:
        # Do not print request URLs, since the OMDb URL contains an API key.
        print(f"{name} request failed: {type(error).__name__}")
        return None

    print(f"{name} HTTP status: {response.status_code}")
    if response.status_code != 200:
        print(f"{name} returned an HTTP error. Skipping this lookup.")
        return None

    try:
        data = response.json()
    except ValueError:
        print(f"{name} did not return valid JSON.")
        return None

    
    print(f"\n{name} response:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print()
    return data


def get_omdb_movie(api_key):
    data = get_json(
        OMDB_URL,
        {"apikey": api_key, "i": IMDB_ID, "plot": "short", "r": "json"},
        "OMDb",
    )
    if data is None:
        return None
    if data.get("Response") != "True":
        print("OMDb error:", data.get("Error", "Movie not found"))
        return None

    # Keep only fields useful for this comparison, not the full API response.
    return {
        "imdb_id": data.get("imdbID"),
        "title": data.get("Title"),
        "year": data.get("Year"),
        "director": data.get("Director"),
        "genre": data.get("Genre"),
        "runtime": data.get("Runtime"),
        "imdb_rating": data.get("imdbRating"),
        "imdb_votes": data.get("imdbVotes"),
        "plot": data.get("Plot"),
    }


def year_in_text(text):
    match = re.search(r"\b(?:19|20)\d{2}\b", text or "")
    return match.group(0) if match else ""


def get_wikipedia_movie():
    data = get_json(
        WIKIPEDIA_API_URL,
        {
            "action": "query",
            "prop": "info|extracts",
            "titles": WIKIPEDIA_TITLE,
            "inprop": "url",
            "exintro": "1",
            "explaintext": "1",
            "exchars": "350",
            "format": "json",
            "formatversion": "2",
        },
        "Wikipedia MediaWiki",
    )
    if data is None:
        return None
    if "error" in data:
        print("MediaWiki API error:", data["error"].get("info", "Unknown error"))
        return None

    pages = data.get("query", {}).get("pages", [])
    if not pages or "missing" in pages[0]:
        print("Wikipedia article not found.")
        return None

    page = pages[0]
    intro = page.get("extract", "")
    return {
        "page_id": page.get("pageid"),
        "title": page.get("title"),
        "page_length_bytes": page.get("length"),
        "intro_preview": intro[:220],
        "year_in_intro": year_in_text(intro),
        "url": page.get("fullurl"),
    }


def cleaned_title(title):
    return re.sub(r"[^a-z0-9]", "", (title or "").lower())


def save_json(filename, data):
    with open(OUTPUT_FOLDER / filename, "w", encoding="utf-8") as file:
        json.dump([data], file, indent=2, ensure_ascii=False)
    print("Saved", filename)


def main():
    api_key = os.environ.get("OMDB_API_KEY", "").strip()
    if not api_key:
        try:
            api_key = getpass("Enter your OMDb API key (hidden): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("No API key entered. Stopping.")
            return
    if not api_key:
        print("An OMDb API key is required. Stopping.")
        return

    print("Looking up a movie using its IMDb ID...")
    omdb = get_omdb_movie(api_key)
    if omdb is None:
        print("No files changed because the OMDb lookup failed.")
        return

    print(f"Now looking up '{omdb['title']}' in Wikipedia's MediaWiki API...")
    time.sleep(1)
    wiki = get_wikipedia_movie()
    if wiki is None:
        print("No files changed because the Wikipedia lookup failed.")
        return

    comparison = {
        "imdb_id": omdb["imdb_id"],
        "omdb_title": omdb["title"],
        "wikipedia_title": wiki["title"],
        "title_match": cleaned_title(omdb["title"]) == cleaned_title(wiki["title"]),
        "omdb_year": omdb["year"],
        "wikipedia_year_from_intro": wiki["year_in_intro"],
        "year_match": omdb["year"] == wiki["year_in_intro"],
        "director_from_omdb": omdb["director"],
        "imdb_rating": omdb["imdb_rating"],
        "wikipedia_page_id": wiki["page_id"],
        "wikipedia_page_length_bytes": wiki["page_length_bytes"],
        "wikipedia_url": wiki["url"],
    }

    save_json("OMDb.json", omdb)
    save_json("WikipediaMediaWiki.json", wiki)
    with open(OUTPUT_FOLDER / "movie_comparison.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(comparison.keys()))
        writer.writeheader()
        writer.writerow(comparison)
    print("Saved movie_comparison.csv")
    print("\nComparison:")
    print(json.dumps(comparison, indent=2, ensure_ascii=False))
    print("\nFinished. Check the JSON and CSV files before pushing to GitHub.")


if __name__ == "__main__":
    main()
