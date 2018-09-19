import xml.etree.ElementTree as ET
import json
import requests
import traceback


def build_gr_request(book_title):
    """Builds the API fetch request to get data from the Goodreads API based on a user-entered book title"""

    with open('Data/DataFiles/config.json', 'r') as config_file:
        config = json.load(config_file)

    dev_key = config['Goodreads_key']

    title_format = book_title.replace(' ', '+')
    goodreads_request = "https://www.goodreads.com/book/title.xml?&key={0}&title={1}".format(
        dev_key, title_format)
    response = requests.get(goodreads_request)
    root = ET.fromstring(response.content)
    book_root = root.find("book")
    print(goodreads_request)
    return book_root


def fave_book(book_title):
    """Attempts to create a new fave book"""

    book_root = build_gr_request(book_title)
    fave_book = dict()
    fave_book["gr_id"] = ""
    fave_book["isbn"] = ""
    fave_book["isbn13"] = ""
    fave_book["work_id"] = ""
    fave_book["title"] = ""
    fave_book["author"] = ""
    fave_book["cover"] = ""
    fave_book["gr_link"] = ""
    fave_book["similar_titles"] = list()
    try:
        fave_book["gr_id"] = book_root.find("id").text
        if not book_root.find("isbn") is None:
            fave_book["isbn"] = book_root.find("isbn").text
        if not book_root.find("isbn13") is None:
            fave_book["isbn13"] = book_root.find("isbn13").text
        fave_book["work_id"] = book_root.find("work").find("id").text
        fave_book["title"] = book_root.find("title").text
        for author in book_root.find("authors").iter("author"):
            if author.find("role").text is None:
                fave_book["author"] = author.find("name").text.strip()
        fave_book["cover"] = book_root.find("image_url").text
        fave_book["gr_link"] = book_root.find("url").text.strip()
        fave_book["description"] = book_root.find(
            "description").text.strip().replace('<br /><br />', ' ').replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
        if not book_root.find("similar_books") is None:
            for book in book_root.find("similar_books"):
                fave_book["similar_titles"].append(book.find("title").text)
            # fave_book["similar_titles"] = fave_book["similar_titles"][-2:]
        else:
            fave_book["similar_titles"].append("No similar titles")

        if __name__ == '__main__':
            print('Goodreads ID: ', fave_book["gr_id"])
            print('ISBN: ', fave_book["isbn"])
            print('ISBN-13: ', fave_book["isbn13"])
            print('Goodreads Work ID: ', fave_book["work_id"])
            print('Title: ', fave_book["title"])
            print('Author: ', fave_book["author"])
            print('Cover: ', fave_book["cover"])
            print('Goodreads Link: ', fave_book["gr_link"])
            print('Description: ', fave_book["description"])
            print('Similar Titles: ', fave_book["similar_titles"])
        else:
            return fave_book

    except AttributeError:
        unicorn_message = f"Congratulations! You found a unicorn! The book \"{book_title}\" isn't in the system."
        if __name__ == '__main__':
            print(unicorn_message)
        else:
            return(unicorn_message)
    except:
        traceback.print_exc()


if __name__ == "__main__":
    fave_book('Hound of the Baskervilles')
    print("-------------------------")
    # Tests not having an ISBN (because there are so many different editions of this one)
    fave_book('The Sun Also Rises')
    print("-------------------------")
    # Goodreads API automatically sends general requests to the first novel in the series. Yay!
    fave_book('Dresden Files')
    print("-------------------------")
    # Tests a book that doesn't exist
    fave_book("my flubishness")
