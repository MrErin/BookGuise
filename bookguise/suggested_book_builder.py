import xml.etree.ElementTree as ET
import json
import requests
import traceback
from keyword_exclusion_list import exclusion_keywords as exclusions


def build_suggested_book(book_title):
    """accepts a book title and builds a mysterious description from it."""

    with open('Data/DataFiles/config.json', 'r') as config_file:
        config = json.load(config_file)

    gr_dev_key = config['Goodreads_key']
    lt_dev_key = config['LibraryThing_key']

    title_format = book_title.replace(' ', '+')
    goodreads_request = "https://www.goodreads.com/book/title.xml?&key={0}&title={1}".format(
        gr_dev_key, title_format)
    librarything_request = ''

    try:
        response = requests.get(goodreads_request)
        root = ET.fromstring(response.content)
        book_root = root.find("book")

        suggested_book = dict()
        suggested_book["gr_id"] = book_root.find("id").text
        if not book_root.find("isbn") is None:
            suggested_book["isbn"] = book_root.find("isbn").text
        if not book_root.find("isbn13") is None:
            suggested_book["isbn13"] = book_root.find("isbn13").text
        suggested_book["title"] = book_root.find("title").text
        suggested_book["keywords"] = list()
        if not book_root.find("popular_shelves") is None:
            for shelf in book_root.find("popular_shelves").iter("shelf"):
                if shelf.attrib["name"] not in exclusions:
                    # print(shelf.attrib["name"], shelf.attrib["count"])

                    #! need to figure out how to add the keywords and counts as dictionary entries to the list
                    suggested_book["keywords"].append([shelf.attrib["name"]]=shelf.attrib["count"])

        # if __name__ == '__main__':
        #     print(goodreads_request)
        #     print(librarything_request)
        #     print(suggested_book)
        else:
            return suggested_book

    except:
        print('The goodreads request was: ', goodreads_request)
        print('The librarything request was: ', librarything_request)

        traceback.print_exc()


if __name__ == '__main__':
    build_suggested_book('Narnia')
