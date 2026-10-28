# IS 310: Minecraft Wiki Web Scraping

## My question

How much information does Minecraft Wiki have about different animal mobs? I wanted to compare how detailed their pages are by looking at word count and how many other wiki pages they link to.

## Why I chose this wiki

I chose [Minecraft Wiki](https://minecraft.wiki) because it is a community-run wiki from our class's recommended list. Minecraft has a lot of different mobs, so I thought it would be interesting to see whether some get much more documentation than others. This might help researchers study how people organize and document information about games.

## What I scraped

My script starts with the [Animal mobs category](https://minecraft.wiki/w/Category:Animal_mobs). It gets links to the first 10 eligible animal mobs listed there and then visits each mob's article. For every article, it records the mob name, word count, character count, total internal links, unique internal links, the article URL and the category URL. It saves everything to `minecraft_animal_mobs.csv`.

The category page and individual article pages are two different levels of the wiki.

## Scraping rules

I checked the site's [robots.txt](https://minecraft.wiki/robots.txt). When I tested the Mobs category from my Mac, the robots.txt check allowed the test page and Python received HTTP 200. The script checks robots.txt again when it runs and does not request pages it disallows. It identifies me with a student User-Agent, waits five seconds between page requests and skips pages if they return an error. I also reviewed the [Minecraft Wiki rules](https://minecraft.wiki/w/Minecraft_Wiki:Wiki_rules). I only collect counts and URLs instead of republishing the article text or images.

## What these numbers mean

I think word count and internal links are useful for seeing which pages have more information, but they do not directly tell us which mobs are the most popular. A longer page might have more details because a mob has more complicated game mechanics or because editors spent more time working on it. The word counts might also include tables and other information inside the article. Since I am only looking at 10 animal mobs, I would not use these results to make claims about every Minecraft mob.

## How to run

1. Open the `web-scraping` folder in VS Code.
2. Activate the virtual environment with `source .venv/bin/activate` on a Mac, if needed.
3. Install packages with `python -m pip install -r requirements.txt`.
4. Run `python wiki_scraping.py`.
5. When the script finishes, check for `minecraft_animal_mobs.csv` in the same folder.

The script makes one request for robots.txt and up to 11 page requests. It pauses five seconds before each wiki page request. If a page is blocked or the site's page structure changes, it skips the page rather than writing an incorrect zero count.
