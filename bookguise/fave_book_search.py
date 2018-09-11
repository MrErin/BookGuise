import xml.etree.ElementTree as ET
import json
import requests
import traceback


def find_fave(title_input):
    """Builds an API fetch request from a book title entered by a user into the search bar"""

    with open('Data/DataFiles/config.json', 'r') as config_file:
        config = json.load(config_file)

    dev_key = config['Goodreads_key']

    # TODO: figure out what other substitutions to make such as apostrophes and other special characters
    title_format = title_input.replace(' ', '+')
    goodreads_request = "https://www.goodreads.com/book/title.xml?&key={0}&title={1}".format(
        dev_key, title_format)

    try:
        response = requests.get(goodreads_request)
        root = ET.fromstring(response.content)
        book_root = root.find("book")

        fave_book = dict()
        fave_book["gr_id"] = book_root.find("id").text
        if not book_root.find("isbn") is None:
            fave_book["isbn"] = book_root.find("isbn").text
        if not book_root.find("isbn13") is None:
            fave_book["isbn13"] = book_root.find("isbn13").text
        fave_book["work_id"] = book_root.find("work").find("id").text
        fave_book["title"] = book_root.find("title").text

        if __name__ == '__main__':
            print(goodreads_request)
            print(fave_book)
        else:
            return fave_book

    except:
        print('The request was: ', goodreads_request)

        traceback.print_exc()


if __name__ == "__main__":
    find_fave('Hound of the Baskervilles')
    find_fave('The Sun Also Rises')
    # Goodreads API automatically sends general requests to the first novel in the series. Yay!
    find_fave('Dresden Files')
