
DROP TABLE IF EXISTS
LT_Books;
DROP TABLE IF EXISTS
LT_Books_User_Tags;
DROP TABLE IF EXISTS
LT_Books_User_Collections;

CREATE TABLE 'LT_Books'
(
    'book_id'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    'lt_user_id' TEXT,
    'lt_book_id' INTEGER,
    'book_title' TEXT, 
    'book_author_lf' TEXT, 
    'book_author_fl' TEXT, 
    'book_author_code' TEXT, 
    'book_ISBN' TEXT, 
    'book_ISBN_cleaned' TEXT, 
    'book_publication_date' TEXT, 'book_language_original' TEXT, 
    'book_cover_URL' TEXT,
    'delete' INTEGER,
    'delete_reason' TEXT
    );

CREATE TABLE 'LT_Books_User_Tags'
(
    'tag_id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    'lt_user_id' TEXT,
    'lt_book_id' INTEGER,
    'user_tag' TEXT,
    'delete' INTEGER,
    'delete_reason' TEXT
);

CREATE TABLE 'LT_Books_User_Collections'
(
    'collection_id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    'lt_user_id' TEXT,
    'lt_book_id' INTEGER,
    'user_collection_id' TEXT,
    'user_collection_name' TEXT,
    'delete' INTEGER,
    'delete_reason' TEXT
);