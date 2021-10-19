# HabrSearchScrapping
More precise [Habr](https://habr.com/) search for articles by given query. Allows to filter search results by publication date, rating and tags. 

## Install
This project uses [poetry](https://python-poetry.org/docs/) for managing dependencies. Setup project with following command:
```sh
poetry install
```
If poetry is not located by shell but written in $PATH, try use poetry.bat instead (ocurred in `cygwin64` terminal).

### For development
To set up development environment additionally run:
```sh
make install
```

## Usage
Access virtualenv via Poetry by running `poetry shell`. The main executable is `Source/main.py`:
```sh
python ./Source/main.py
```
Script supports following CLI options:
```
-h, --help
    show this help message and exit
-q QUERY, --query QUERY
    obligatory parameter;
    what to search in https://habr.com;
-a ARTICLESAMOUNT, --amount ARTICLESAMOUNT
    obligatory parameter;
    how much articles to process;
-o FILE, --output FILE
    obligatory parameter;
    path to output file;
-r RATINGRANGE, --rating RATINGRANGE
    range of the article rating start and end are divided
    with ':', one of borders may not exist;
-d DATERANGE, --date DATERANGE
    date borders of the article publishing separated with
    ':', one of borders may not exist, format is
    `$YEAR-$MONTH-$DAY`;
-t TAGS, --tags TAGS
    one of tags listed with `;` between must be presented
    in article
```
