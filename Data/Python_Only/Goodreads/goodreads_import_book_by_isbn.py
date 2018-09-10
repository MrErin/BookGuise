import xml.etree.ElementTree as ET
import json
import requests
import sqlite3

database = "Data/DataFiles/DataImports.db"
with open('Data/DataFiles/config.json', 'r') as config_file:
    config = json.load(config_file)

# print(config['NYT_key'])

# https://www.goodreads.com/book/isbn/0441172717?key= + devkey

current_isbn = '0441172717'
dev_key = config['Goodreads_key']
goodreads_request = "https://www.goodreads.com/book/isbn/{0}?key={1}".format(
    current_isbn, dev_key)

# print(goodreads_request)

response = requests.get(goodreads_request)
root = ET.fromstring(response.content)

# tree = ET.parse('Data/Python_Only/Goodreads/sample.xml')
# root = tree.getroot()


class GoodReads_Book_Tags():
    """collects data from GoodReads on individual books based on their ISBN
    """

    def __init__(self, isbn):
        """Collect data from XML"""

        book_tags = root.find("book")
        shelf_tag = book_tags.find("popular_shelves")
        con = sqlite3.connect(database)

        for shelf in shelf_tag.iter("shelf"):
            self.gr_id = book_tags.find("id").text.strip()
            self.isbn = book_tags.find("isbn").text.strip()
            self.isbn13 = book_tags.find("isbn13").text.strip()
            self.shelf_name = shelf.attrib["name"]
            self.shelf_count = shelf.attrib["count"]

            with con:
                cur = con.cursor()
                con.row_factory = sqlite3.Row

                cur.execute("INSERT INTO GR_Popular_Shelves"
                            "("
                            "gr_id,"
                            "isbn,"
                            "isbn13,"
                            "gr_shelf_name,"
                            "gr_shelf_count"
                            ") VALUES (?,?,?,?,?)", (
                                self.gr_id,
                                self.isbn,
                                self.isbn13,
                                self.shelf_name,
                                self.shelf_count
                            ))

    def __repr__(self):
        print(
            f'Goodreads ID: {self.gr_id}, ISBN: {self.isbn}, ISBN13: {self.isbn13}, Shelf Name: {self.shelf_name}, Shelf Count: {self.shelf_count}')

    def save_popular_shelves_to_database(self):
        """saves the popular shelf data to the database"""


GoodReads_Book_Tags(current_isbn)
