# Table Scraper
This is a command-line web scraper app which extracts data from any table in any Wikipedia page (with a table)

## Motivation
Have you ever wanted to quickly run some statistics or visuals on a [Wikipedia](wikipedia.com) table? 

I have. So I wanted a way to begin thinking about a good way to do this. 

So far, this is what I've come up with, and it only involves the most primitive understanding of web-scraping, i.e. that there is such a thing as inspecting the html of a webpage as well as a command line interface!

## Instalation and Usage of `Table Scraper`

### Installation:
(You need `python` on your PATH to run this code, and you need `git` also in order to clone this repo.)
1. Clone the repo
```bash
git clone https://github.com/yoniabrams/Table_Scraper
cd Table_Scraper
```

2. Create virtual environment (recommended!!)
```bash
# on MacOS and Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install requirements (just a few, don't worry)
```bash
pip install -r requirements.txt
```

### Usage
If you type the following into your command-line you will see the "help" for the command-line application, describing the required and optional parameters to pass to the function in the command-line

```bash
python table_scraper.py -h
```
This is what you'll see:
```
usage: table_scraper.py [-h] [--table-id TABLE_ID] [--table-class TABLE_CLASS] [--with-citation WITH_CITATION] [--citation-base-url CITATION_BASE_URL] [--data-filepath DATA_FILEPATH]
                        [--citation-filepath CITATION_FILEPATH]
                        url

Scrape table data from a wikipedia URL.

positional arguments:
  url                   URL of the webpage

options:
  -h, --help            show this help message and exit
  --table-id TABLE_ID   Table ID in HTML
  --table-class TABLE_CLASS
                        Table class in HTML
  --with-citation WITH_CITATION
                        True/False: Would you like to get citations for data?
  --citation-base-url CITATION_BASE_URL
                        The base URL for the citations
  --data-filepath DATA_FILEPATH
                        relative or absolute path for where to save the scraped data
  --citation-filepath CITATION_FILEPATH
                        relative or absolute path for where to save the scraped citations
```

### Required parameters:
1. URL of Wikipedia page
2. Either the table-id or the table-class attribute from the table element (I'll say more about this soon).

### Example usage:
1. Let's say you want to learn about the most densely populated cities in the EU, so you go to this webpage [here](https://en.wikipedia.org/wiki/List_of_European_Union_cities_proper_by_population_density).
2. `Right click' on the upper-leftmost box of the table you're interested in
3. Click 'inspect'.
4. You'll see the table element from the "backend" (actually, "frontend" but whatever) of the webpage, and find the element which is called `table`:
    - E.g. `<table class=sortable ... ...>`
5. Type the following in your command-line (tweak according to your specifications and the available variables):
```bash
 python table_scraper.py https://en.wikipedia.org/wiki/List_of_European_Union_cities_proper_by_population_density --table-class sortable --with-citation True --citation-base-url https://en.wikipedia.org/wiki/List_of_European_Union_cities_proper_by_population_density

```
### Example output:
The two files, `data.csv` and `citations.csv` from the above code will look something like this:

**data.csv**
```

"Rank", "City", "Population", "Area (km2)", "Area (sq. miles)", "Density (/km2)", "Density (/sq. mile)", "Country"
0, 1, Levallois-Perret, "66,082", 2.41, 0.93, "27,420", "71,056", France
1, 2, Emperador, 692,0.03, 0.01, "23,067", "69,200" ,Spain
...
```
**citations.csv**
```
row,column,data,source
0, 26, "Population", "1,212,352[1]", https://en.wikipedia.org/wiki/List_of_European_Union_cities_proper_by_population_density#cite_note-1
1, 26, "Area (km2)", 162.4[2], https://en.wikipedia.org/wiki/List_of_European_Union_cities_proper_by_population_density#cite_note-2
...
```

### Disclaimer
There is more to be done here to make this scraper more robust.

### Thank you for stopping by!
