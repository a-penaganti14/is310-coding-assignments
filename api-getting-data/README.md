# IS 310: Getting Culture Across APIs

## What I did

I chose movies for this assignment because I love watching movies. I thought it would be interesting to see what kind of data different websites have about the same movie. I used *Guardians of the Galaxy Vol. 2* because this was the example in the OMDb link I started with. My main question was how OMDb and Wikipedia organize information about the same movie.

I used the OMDb API to get the title, release year, director, genre and rating. Then I used Wikipedia's MediaWiki Action API to look up the same movie. From Wikipedia, I got the article title, page ID, article length and part of the introduction. I compared the names and years to check whether both results were about the same movie. OMDb includes a colon in the movie title, while Wikipedia doesn't, so I ignored punctuation when checking the titles.

## Comparing the APIs

The main difference I noticed was what each API focuses on. OMDb gives you movie details in one JSON response, including ratings and the director. Wikipedia's API gives you information about a wiki article, like its page ID and size, and some text from the article. I thought OMDb was easier for getting movie facts, while Wikipedia was more useful for learning about the movie itself. Both return JSON, but they organize the information differently.

OMDb needed me to sign up for a free API key. Its free plan allows 1,000 requests a day. Wikipedia did not need an account or key for this request, but I included a User-Agent with my school email. Wikimedia's current API limit for an identified, unauthenticated script is 200 requests per minute. I only made a few requests, with a short pause between them. OMDb is run by Brian Fritz and supported through free and paid access. Wikipedia is run by the nonprofit Wikimedia Foundation and its articles are written and updated by contributors. If either site changes its rules or stops offering access, I would have to change how I get the data.

Neither source tells you everything about a movie. OMDb has selected ratings and movie facts, but those ratings change and they do not show what everyone thinks. Wikipedia has more background information, but the content depends on what people have written and edited. Some movies also have much longer articles than others. Looking at one movie is enough to test the APIs, but not enough to make claims about every movie.

## Files

- `getting_culture.py` makes the API requests and prints the responses.
- `OMDb.json` saves selected movie fields from OMDb.
- `WikipediaMediaWiki.json` saves selected fields from Wikipedia's API.
- `movie_comparison.csv` compares the title, year and other information from both sources.
- `requirements.txt` lists the Python library needed to run the script.

## How to run

1. Open the `api-getting-data` folder in VS Code.
2. Run `python3 -m pip install -r requirements.txt` in the terminal.
3. Run `python3 getting_culture.py`.
4. Paste your OMDb API key when the terminal asks. It will not appear on the screen or be saved in the project.
5. Check the two JSON files and the CSV before pushing them to GitHub.

The included data files are a saved example from November 9, 2026. Running the script updates them with fresh API results.

## Sources

- OMDb API: https://www.omdbapi.com/
- OMDb API key information: https://www.omdbapi.com/apikey.aspx
- Wikipedia MediaWiki Action API: https://en.wikipedia.org/w/api.php
- Wikimedia API limits: https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits
