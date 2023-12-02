import argparse
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_page_soup(url):
    """ return a BeautifulSoup object from an url """

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def get_table_columns(soup: BeautifulSoup, table_id=None, table_class=None):
    """ return the columns from the desired table from the wikipedia-page BeautifulSoup html parser"""

    if table_id:  # if using an "id" attribute to reference the table
        table = soup.find('table', id=table_id)
    elif table_class:  # if using a "class_" attribute to reference the table
        table = soup.find('table', class_=table_class)
    else:
        return "No table reference method provided"

    headers = []
    for column in table.find_all('th'):
        title = column.text
        headers.append(title)
    return table, headers


def _get_citation_data(data_box, citation_base_url=None):
    """ from a wikipedia BeautifulSoup element, extract the citation provided """
    relative_url = data_box.find('sup').find('a').get('href')
    if citation_base_url:
        source = citation_base_url + relative_url
    else:
        source = relative_url
    return source


def populate_dataframe(table, headers, with_citation=False, citation_base_url=None, first_column_is_index=True):
    """
    traverse a wikipedia table through all <tr>s and <td>s i.e. rows and columns
    :param table: a BeautifulSoup table element
    :param headers: (list) a list of the column names in the table
    :param with_citation: (bool) if True, return a list of citations for each element where one is provided
    :param citation_base_url: (str) if provided, append the citation hrefs to the base url of the wiki page
    :param first_column_is_index: (bool) if True, reference the first column of each row instead of numeric idx
    :return: data (data from table) and citations (if desired)
    """
    data_from_table = pd.DataFrame(columns=headers)

    if with_citation:
        citations_from_table = []

    for row_idx, j in enumerate(table.find_all('tr')[1:]):
        row_data = j.find_all('td')  # find all the columns of the row

        row = []  # we will elicit the text from each col/row i.e. table element
        for col_idx, box in enumerate(row_data):
            unclean_text = box.text.strip()
            if with_citation and box.find('sup'):
                source = _get_citation_data(box, citation_base_url)
                citations_from_table.append({
                    'row': row[0] if first_column_is_index else row_idx + 1,
                    'column': headers[col_idx],
                    'data': unclean_text,
                    'source': source
                })

            row.append(unclean_text)

        length = len(data_from_table)
        data_from_table.loc[length] = row

    if not with_citation:
        return data_from_table

    return data_from_table, citations_from_table


def scrape_table(
        wiki_url,
        table_id=None,
        table_class=None,
        with_citation=False,
        citation_base_url=None,
        data_path='data.csv',
        citation_path='citation.csv'):
    """
    scrape data from a table in a wikipedia page
    :param wiki_url: (str) url of wiki page
    :param table_id: (str) id attribute of table element
    :param table_class:  (str) class attribute of table element
    :param with_citation: (bool) True if client wants citations from the table
    :param citation_base_url: (str) base url of the wiki page to reference the citations
    :param data_path: (str) filepath to where to save the data csv
    :param citation_path: (str) filepath to where to save the citation csv
    :return: None
    """
    wiki_soup = get_page_soup(wiki_url)

    wiki_table, column_names = get_table_columns(wiki_soup, table_id=table_id, table_class=TABLE_CLASS)

    data, citations = populate_dataframe(
        wiki_table,
        column_names,
        with_citation=with_citation,
        citation_base_url=citation_base_url
    )

    if data_path is None:
        data_path = 'data.csv'  # switch to a default value
    if citation_path is None:
        citation_path = 'citations.csv'

    data.to_csv(data_path)
    citations_df = pd.DataFrame(citations)
    citations_df.to_csv(citation_path)


if __name__ == '__main__':
    # configure argparse
    parser = argparse.ArgumentParser(description='Scrape table data from a wikipedia URL.')
    parser.add_argument('url', type=str, help='URL of the webpage')
    parser.add_argument('--table-id', type=str, help='Table ID in HTML')
    parser.add_argument('--table-class', type=str, help='Table class in HTML')
    parser.add_argument('--with-citation', type=bool, help='True/False: Would you like to get citations for data?')
    parser.add_argument('--citation-base-url', type=str, help='The base URL for the citations')
    parser.add_argument(
        '--data-filepath', type=str, help='relative or absolute path for where to save the scraped data'
    )
    parser.add_argument(
        '--citation-filepath', type=str, help='relative or absolute path for where to save the scraped citations'
    )

    # parse the commandline arguments
    args = parser.parse_args()
    URL = args.url
    TABLE_ID = args.table_id
    TABLE_CLASS = args.table_class
    WITH_CITATION = args.with_citation
    CITATION_BASE_URL = args.citation_base_url
    DATA_PATH = args.data_filepath
    CITATION_PATH = args.citation_filepath

    # scrape the table!
    scrape_table(
        wiki_url=URL,
        table_id=TABLE_ID,
        table_class=TABLE_CLASS,
        with_citation=WITH_CITATION,
        citation_base_url=CITATION_BASE_URL,
        data_path=DATA_PATH,
        citation_path=CITATION_PATH)
