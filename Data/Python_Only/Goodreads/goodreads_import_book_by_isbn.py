import xml.etree.ElementTree as ET
import json
import requests


# with open('Data/DataFiles/config.json', 'r') as file:
#     config = json.load(file)

# print(config['NYT_key'])

# https://www.goodreads.com/book/isbn/0441172717?key= + devkey

# current_isbn = '0441172717'
# dev_key = config['Goodreads_key']
# goodreads_request = "https://www.goodreads.com/book/isbn/{0}?key={1}".format(
#     current_isbn, dev_key)

# print(goodreads_request)

# response = requests.get(goodreads_request)
# root = ET.fromstring(response.content)

tree = ET.parse('Data/Python_Only/Goodreads/sample.xml')
root = tree.getroot()


class GoodReads_Book_Tags():
    """collects data from GoodReads on individual books based on their ISBN
    """

    def __init__(self, isbn):
        """Collect data from XML"""

        # self.book_cover_URL = json_dict[lt_id]["cover"]
        # if ("tags" in json_dict[lt_id]):
        #     self.user_tags = json_dict[lt_id]["tags"]
        self.gr_id = ''
        self.isbn = ''
        self.isbn13 = ''
        self.shelf_name = ''
        self.shelf_count = ''

    def __repr__(self):
        print(
            f'{self.gr_id}, {self.isbn}, {self.isbn13}, {self.shelf_name}, {self.shelf_count}')

    def test():
        for child in root:
            print(child.tag, child.attrib)

    # def save_popular_shelves_to_database(self):
    #     """saves the popular shelf data to the database"""


# print(GoodReads_Book(current_isbn))
GoodReads_Book_Tags.test()
