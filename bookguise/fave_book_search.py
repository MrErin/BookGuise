import xml.etree.ElementTree as ET
import json
import requests
import traceback


def find_fave(title_input):
    """Builds an API fetch request from a book title entered by a user into the search bar"""

    with open('Data/DataFiles/config.json', 'r') as config_file:
        config = json.load(config_file)

    dev_key = config['Goodreads_key']

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
        fave_book["similar_titles"] = list()
        if not book_root.find("similar_books") is None:
            for book in book_root.find("similar_books"):
                fave_book["similar_titles"].append(book.find("title").text)
            fave_book["similar_titles"] = fave_book["similar_titles"][-3:]
        else:
            fave_book["similar_titles"].append("No similar titles")

        if __name__ == '__main__':
            print(goodreads_request)
            print(fave_book)
        else:
            return fave_book
    except AttributeError:
        unicorn_message = f"Congratulations! You found a unicorn! The book \"{title_input}\" isn't in the system."
        print(unicorn_message)
        return(unicorn_message)
    except:
        print('The request was: ', goodreads_request)

        traceback.print_exc()


if __name__ == "__main__":
    # find_fave('Hound of the Baskervilles')
    # Tests not having an ISBN (because there are so many different editions of this one)
    # find_fave('The Sun Also Rises')
    # Goodreads API automatically sends general requests to the first novel in the series. Yay!
    # find_fave('Dresden Files')
    # Tests a book that doesn't exist
    find_fave("my flubishness")
