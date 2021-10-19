import sys
sys.path.append("./Modules")

import os
import math
from argparse import ArgumentParser
from re import sub
import datetime
from dateutil.parser import parse as parseDate
from bs4 import BeautifulSoup

import Modules.Compare as Compare
import Modules.Log as Log
import Modules.Display as Display
import Modules.Page as Page
import Modules.Habr.HabrURL as HabrURL
import Modules.Habr.HabrSearch as HabrSearch
import Modules.Habr.HabrSearchPost as HabrSearchPost
import Modules.Habr.HabrPost as HabrPost
import Modules.Habr.HabrArticle as HabrArticle

# CLI interface
parser = ArgumentParser()
parser.add_argument("-q", "--query", dest="query", help="what to search in https://habr.com;", default="")
parser.add_argument("-a", "--amount", dest="articlesAmount", help="how much articles to process;", type=int, default=5)
parser.add_argument("-o", "--output", dest="output", help="path to output file;", metavar="FILE", default="")
parser.add_argument("-r", "--rating", dest="ratingRange", help="range of the article rating start and end are divided with ':', one of borders may not exist;", default=":")
parser.add_argument("-d", "--date", dest="dateRange", help="date borders of the article publishing separated with ':', one of borders may not exist, format is `$YEAR-$MONTH-$DAY`;", default=":")
parser.add_argument("-t", "--tags", dest="tags", help="one of tags listed with `;` between must be presented in article", default="")
args = parser.parse_args()

# Verifying `query` argument
if not args.query:
    Log.out("Nothing to search\n  Query string is empty", "WARNING")
    exit()
query = sub('\s+', ' ', args.query)

# Verifying `output` argument
if not args.output:
    Log.out("No output file specified", "ERROR")
    exit()

outputDir = os.sep.join(os.path.normpath(args.output).split(os.sep)[0:-1])

# Verifying and initializing `ratingRange` filter
rating = args.ratingRange.split(":")
rating[0] = int(rating[0]) if rating[0] != "" else -math.inf
rating[1] = int(rating[1]) if rating[1] != "" else math.inf

# Verifying and initializing `dateRange` filter
dates = args.dateRange.split(":")
dates[0] = parseDate(dates[0]).timestamp() if dates[0] != "" else None
dates[1] = parseDate(dates[1]).timestamp() if dates[1] != "" else None

# Initializing `tags` filter
tags = list(filter(lambda tag: len(tag) > 0, args.tags.split(";")))

Log.out("Finding articles with query: \"" + query + "\"", "INFO")

articles = []
resultsPageURL = HabrURL.getSearchPageURL(query)

# Converting HTML from Habr search to objects
parsedArticlesAmount = 0
while parsedArticlesAmount < args.articlesAmount and resultsPageURL:
    Log.out("Loading search with URL: " + resultsPageURL, "INFO")
    html = Page.load(resultsPageURL)
    if not html:
        exit();

    dom = BeautifulSoup(html.read(), 'html.parser')
    resultsPageURL = HabrSearch.getNextPageURL(dom)
    habrPostDoms = HabrSearch.getPosts(dom)[:(args.articlesAmount - len(articles))]

    for postDomIndex in range(len(habrPostDoms)):
        postDom = habrPostDoms[postDomIndex]
        try:
            article = HabrArticle.fromDom(postDom)
            articles.append(article)
        except:
            Log.out("Cannot parse article\n  Failed article is #" + str(postDomIndex + 1) + "on the page", "WARNING")
    
    parsedArticlesAmount += len(habrPostDoms)
    print("  Parsed " + str(parsedArticlesAmount) + "/" + str(args.articlesAmount))

# Removing articles with undesired rating
if args.ratingRange != ':':
    articles = filter(lambda article: Compare.isInRange(article['rating'], rating[0], rating[1]), articles)
# Removing articles with undesired publishing dates
if args.dateRange != ':':
    articles = filter(lambda article: Compare.isInRange(article['date'], dates[0], dates[1]), articles)
# Removing articles without required tags
if args.tags != '':
    articles = filter(lambda article: Compare.includesOneOfPartially(article['tags'], tags), articles)

# Converting date and time to ISO string
articles = list(map(lambda article: { **article, 'date': datetime.datetime.utcfromtimestamp(article['date']).isoformat() if article['date'] != None else '-' }, articles))

# Saving data into csv output file
Log.out("Saving results to \"" + args.output + "\", as CSV", "INFO")
Display.toCSV(articles, args.output)

# Downloading chosen articles
Log.out("\nDownloading articles texts to '" + outputDir + "'", "INFO")
for article in articles:
    Log.out("Downloading \"" + article['title'] + "\"", "INFO")
    html = Page.load(article['url'])
    if not html:
        print("  Failed to download text of the article above \"" + article['title'] + "\"")
        continue
    
    dom = BeautifulSoup(html.read(), 'html.parser')
    articleHtml = str(HabrPost.getText(dom))

    file = open(outputDir + os.sep + sub('[<>:"/\\\?\*]', '', article['title']) + '.html', 'w', encoding="utf-8")
    file.write(Page.wrap(articleHtml, "utf-8"))
    file.close()
