import csv

def toCSV(articles, path):
    with open(path, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, delimiter=",", fieldnames=["source", "date", "title", "url"], extrasaction="ignore")
        writer.writeheader()
        for article in articles:
            writer.writerow(article)
