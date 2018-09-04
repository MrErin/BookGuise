import json
import sqlite3


class Books():
    """Creates a class for the collection of data for an individual user's books imported from LibraryThing.
    Field List:
        * book_id (LibraryThing's internal ID of the given book)
        * book_title
        * book_author_lf (Author's name in "Last, First" format)
        * book_author_fl
        * book_author_code (LibraryThing's internal author identifier)
        * book_ISBN
        * book_ISBN_cleaned (not sure if there's any difference between this field and the previous one but LT provides both so I'm keeping both and will sort it out with SQL)
        * book_publication_date (appears to be just the year)
        * book_language_original
        * book_cover_URL
        * book_tags (list of user-generated keywords for the book)
        * book_collections (list of user-generated keywords for the book)
    """

    def __init__(self, json_dict, lt_id):
        """Collects the individual book data from Library Thing's JSON export

        Args:
            json_dict (dictionary): Expects a JSON object
            lt_id (integer): Key for the JSON object. In the LT import, this is LT's internal book ID.

        Structure: (curly braces indicate generic explanations)
            self.{SQLite field name} = json_dict[{Key for the JSON object to be deserialized}][{key for the target value for this field}]
            self.book_id = json_dict[lt_id]["book_id]
        """
        self.book_id = json_dict[lt_id]["book_id"]
        self.book_title = json_dict[lt_id]["title"]
        self.book_author_lf = json_dict[lt_id]["author_lf"]
        self.book_author_fl = json_dict[lt_id]["author_fl"]
        self.book_author_code = json_dict[lt_id]["author_code"]
        self.book_ISBN = json_dict[lt_id]["ISBN"]
        self.book_ISBN_cleaned = json_dict[lt_id]["ISBN_cleaned"]
        self.book_publication_date = json_dict[
            lt_id]["publicationdate"]
        self.book_language_original = json_dict[
            lt_id]["language_original"]
        self.book_cover_URL = json_dict[lt_id]["cover"]
        if ("tags" in json_dict[lt_id]):
            self.user_tags = json_dict[lt_id]["tags"]
        if ("collections" in json_dict[lt_id]):
            self.user_collections = json_dict[lt_id]["collections"]

    def __repr__(self):
        """prints the book's title as a representation of the entire object
        """
        print(self.book_title)


class LT_User():
    """Creates a class for the collection of a user's data from LibraryThing
    """

    def __init__(self, lt_user, json_dict):
        """Collects the user data for a LibraryThing import

        This serves as a wrapper of sorts for the book object. It adds the username to the individual book records.

        Args:
            lt_user (string): the user's LibraryThing username
            json_dict (JSON): book data from the LT JSON export
        """
        self.userDict = json_dict[lt_user]
        self.lt_userId = lt_user

    def __repr__(self):
        """returns the user name when this object is accessed
        """
        return(self.lt_userId)

    def save_books_to_database(self):
        """Saves the records to the indicated SQLite database
        """

        con = sqlite3.connect(
            "Python_Only/LibraryThing/LibraryThingImports.db")
        with con:
            cur = con.cursor()
            con.row_factory = sqlite3.Row

            for book in self.userDict:
                self.book = Books(self.userDict, book)
                cur.execute("INSERT INTO LT_Books"
                            "("
                            "lt_user_id,"
                            "lt_book_id,"
                            "book_title,"
                            "book_author_lf,"
                            "book_author_fl,"
                            "book_author_code,"
                            "book_ISBN,"
                            "book_ISBN_cleaned,"
                            "book_publication_date,"
                            "book_language_original,"
                            "book_cover_URL"
                            ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            (
                                self.lt_userId,
                                self.book.book_id,
                                self.book.book_title,
                                self.book.book_author_lf,
                                self.book.book_author_fl,
                                self.book.book_author_code,
                                self.book.book_ISBN,
                                self.book.book_ISBN_cleaned,
                                self.book.book_publication_date,
                                self.book.book_language_original,
                                self.book.book_cover_URL
                            ))

    def save_tags_to_database(self):
        """Saves user tags for a specific book to the database on the LT_Books_User_Tags table
        """

        con = sqlite3.connect(
            "Python_Only/LibraryThing/LibraryThingImports.db")
        with con:
            cur = con.cursor()
            con.row_factory = sqlite3.Row

            for book in self.userDict:
                self.book = Books(self.userDict, book)
                if(hasattr(self.book, 'user_tags')):
                    for tag in self.book.user_tags:
                        cur.execute("INSERT INTO LT_Books_User_Tags"
                                    "("
                                    "lt_user_id,"
                                    "lt_book_id,"
                                    "user_tag"
                                    ") VALUES (?,?,?)",
                                    (
                                        self.lt_userId,
                                        self.book.book_id,
                                        tag
                                    ))

    def save_collections_to_database(self):
        """Saves user collections for a specific book to the database on the LT_Books_User_Collections table
        """

        con = sqlite3.connect(
            "Python_Only/LibraryThing/LibraryThingImports.db")
        with con:
            cur = con.cursor()
            con.row_factory = sqlite3.Row

            for book in self.userDict:
                self.book = Books(self.userDict, book)
                if(hasattr(self.book, 'user_collections')):
                    # checks for the possibility of an empty list instead of a collections object in the JSON
                    if not not self.book.user_collections:
                        for collection_id, collection_name in self.book.user_collections.items():
                            cur.execute("INSERT INTO LT_Books_User_Collections"
                                        "("
                                        "lt_user_id,"
                                        "lt_book_id,"
                                        "user_collection_id,"
                                        "user_collection_name"
                                        ") VALUES (?,?,?,?)",
                                        (
                                            self.lt_userId,
                                            self.book.book_id,
                                            collection_id,
                                            collection_name
                                        ))


files = dict()

files["Adolf_Ledesma"] = [
    'Python_Only/LibraryThing/Adolf_Ledesma_10k.json',
    'Python_Only/LibraryThing/Adolf_Ledesma_20k.json',
    'Python_Only/LibraryThing/Adolf_Ledesma_20k2.json'
]
files["e-zReader"] = [
    'Python_Only/LibraryThing/e-zReader_20k.json',
    'Python_Only/LibraryThing/e-zReader_20k2.json',
    'Python_Only/LibraryThing/e-zReader_20k3.json'
]

files["purpleprincess1311"] = [
    'Python_Only/LibraryThing/purpleprincess_100.json',
]

for user in files:
    print("The user is:", user)
    for file in files[user]:
        print("The filename is: ", file)
        with open(file) as current_file:
            data = json.load(current_file)
        user_books = LT_User(user, data)
        user_books.save_books_to_database()
        user_books.save_tags_to_database()
        user_books.save_collections_to_database()
