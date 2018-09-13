import xml.etree.ElementTree as ET
import json
import requests
import traceback
# need to put a period before "keyword exclusion list" when ready to use this in the app again.
from keyword_exclusion_list import exclusion_keywords as exclusions


class Suggested_Book():
    """accepts a book title and builds a mysterious description from it."""

    def __init__(self, book_title):
        with open('Data/DataFiles/config.json', 'r') as config_file:
            config = json.load(config_file)

        gr_dev_key = config['Goodreads_key']

        title_format = book_title.replace(' ', '+')
        goodreads_request = "https://www.goodreads.com/book/title.xml?&key={0}&title={1}".format(
            gr_dev_key, title_format)

        try:
            gr_response = requests.get(goodreads_request)
            gr_root = ET.fromstring(gr_response.content)
            gr_book_root = gr_root.find("book")

            self.gr_id = gr_book_root.find("id").text
            if not gr_book_root.find("isbn") is None:
                self.isbn = gr_book_root.find("isbn").text
            if not gr_book_root.find("isbn13") is None:
                self.isbn13 = gr_book_root.find("isbn13").text
            self.title = gr_book_root.find("title").text
            self.publication_year = gr_book_root.find(
                "publication_year").text
            self.gr_link = gr_book_root.find("link").text
            self.keywords = list()
            if not gr_book_root.find("popular_shelves") is None:
                for shelf in gr_book_root.find("popular_shelves").iter("shelf"):
                    if shelf.attrib["name"] not in exclusions:
                        try:
                            shelf.attrib["name"].encode('ascii')
                            # print(shelf.attrib["name"])
                            new_keyword = dict(
                                [(shelf.attrib["name"], int(shelf.attrib["count"]))])
                            self.keywords.append(new_keyword)
                        except UnicodeEncodeError:
                            pass

            lt_dev_key = config['LibraryThing_key']
            librarything_request = 'https://www.librarything.com/services/rest/1.1/?method=librarything.ck.getwork&isbn={0}&apikey={1}'.format(
                self.isbn, lt_dev_key)

            lt_response = requests.get(librarything_request)
            lt_root = ET.fromstring(lt_response.content)
            lt_book_root = lt_root.tag("ltml")
            self.lt_id = lt_root.attrib["version"]

            # self.lt_id = lt_book_root.find("item").attrib["id"]

        except:
            print('The goodreads request was: ', goodreads_request)
            print('The librarything request was: ', librarything_request)
            traceback.print_exc()

    def __repr__(self):
        # print('Goodreads ID: ', self.gr_id)
        # print('ISBN: ', self.isbn)
        # print('ISBN13: ', self.isbn13)
        # print('Title: ', self.title)
        # print('Publication Year: ', self.publication_year)
        # print('Goodreads Link: ', self.gr_link)
        # print('Keywords: ', self.keywords)
        print('LibraryThing ID: ', self.lt_id)


if __name__ == '__main__':
    print(Suggested_Book('Harry Potter'))
