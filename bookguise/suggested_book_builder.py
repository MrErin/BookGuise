import xml.etree.ElementTree as ET
import json
import requests
import traceback
import random

# ! need to put a period before "keyword exclusion list" when ready to use this in the app again.
from .style_choices import style_colors as colors
from .style_choices import style_images as masks
from .keyword_exclusion_list import exclusion_keywords as exclusions
from .keyword_map import keyword_map as keymap


class Suggested_Book():
    """accepts a book title and builds a mysterious description from it."""

    def __init__(self, book_title):
        with open('Data/DataFiles/config.json', 'r') as config_file:
            config = json.load(config_file)

        gr_dev_key = config['Goodreads_key']

        title_format = book_title.replace(' ', '+')
        goodreads_request = "https://www.goodreads.com/book/title.xml?&key={0}&title={1}".format(
            gr_dev_key, title_format)
        print(goodreads_request)

        try:
            self.lt_haiku_summaries = list()
            self.keywords = set()
            self.custom_excludes = set()
            self.bg_color = random.choice(colors)
            self.bg_mask = random.choice(masks)
            self.lt_id = ''
            self.series_title = ''
            self.author = ''
            gr_response = requests.get(goodreads_request)
            gr_root = ET.fromstring(gr_response.content)
            gr_book_root = gr_root.find("book")

            self.gr_id = gr_book_root.find("id").text
            if not gr_book_root.find("isbn") is None:
                self.isbn = gr_book_root.find("isbn").text.strip()
            if not gr_book_root.find("isbn13") is None:
                self.isbn13 = gr_book_root.find("isbn13").text.strip()
            self.title = gr_book_root.find("title").text
            self.publication_year = gr_book_root.find(
                "work").find("original_publication_year").text
            self.gr_link = gr_book_root.find("link").text
            for author in gr_book_root.find("authors").iter("author"):
                if author.find("role").text is None:
                    self.author = author.find("name").text.strip()
            if not gr_book_root.find("series_works").find("series_work") is None:
                self.series_title = gr_book_root.find("series_works").find(
                    "series_work").find("series").find("title").text.strip()
            self.build_custom_excludes()
            if not gr_book_root.find("popular_shelves") is None:
                for shelf in gr_book_root.find("popular_shelves").iter("shelf"):
                    if shelf.attrib["name"] not in exclusions and shelf.attrib["name"] not in self.custom_excludes and int(shelf.attrib["count"]) > 1 and not "series" in shelf.attrib["name"]:
                        try:
                            shelf.attrib["name"].encode('ascii')
                            if shelf.attrib["name"] in keymap.keys():

                                new_keyword = keymap[shelf.attrib["name"]]
                                self.keywords.add(new_keyword)
                            else:
                                self.keywords.add(shelf.attrib["name"])

                        except UnicodeEncodeError:
                            pass
                        except UnicodeDecodeError:
                            pass

            if not self.isbn is None:

                lt_dev_key = config['LibraryThing_key']
                librarything_request = 'https://www.librarything.com/services/rest/1.1/?method=librarything.ck.getwork&isbn={0}&apikey={1}'.format(
                    self.isbn, lt_dev_key)

                print(librarything_request)

                lt_response = requests.get(librarything_request)
                lt_root = ET.fromstring(lt_response.content)

                # !!Prepare for some magic:
                # https://stackoverflow.com/questions/37586536/lxml-doc-find-returning-none

                # According to the "Your target element is in the default namespace" answer in the SO link above, this is what I've done:
                # Create a new dictionary that has an arbitrary key for naming the document and as its value, the "ltml xmlns" value from the xml document
                namespace = {'xml_document': 'http://www.librarything.com/'}

                # set the new root to be a find for my newly created namespace
                lt_book_root = lt_root.find(
                    './/xml_document:fieldList', namespace)
                self.lt_id = lt_root.find(
                    './/xml_document:item', namespace).attrib["id"]

                for field in lt_book_root:
                    if field.attrib["type"] == "57":
                        fact_root = field.findall(
                            ".//{http://www.librarything.com/}fact")
                        for fact in fact_root:
                            self.lt_haiku_summaries.append(
                                fact.text[9:-4].strip().replace('<br>', '/').replace('<p>', '/').replace('</p>', '/'))

        except:
            print('The goodreads request was: ', goodreads_request)
            print('The librarything request was: ', librarything_request)
            traceback.print_exc()

    def build_custom_excludes(self):
        self.custom_excludes.add(self.series_title.lower().replace(' ', '-'))
        if not self.author is None:
            self.author_full = self.author.lower().split(" ")
            print("Self_author_full:", self.author_full)

            try:
                self.custom_excludes.add(
                    f"{self.author_full[0]}")
                if len(self.author_full) == 2:
                    self.custom_excludes.add(
                        f"{self.author_full[0]}-{self.author_full[1]}")
                    self.custom_excludes.add(
                        f"{self.author_full[1]}-{self.author_full[0]}")
                    self.custom_excludes.add(
                        f"{self.author_full[1]}")
                if "." in self.author_full[0]:
                    strip_fn = self.author_full[0].replace('.', '')
                    dash_fn = self.author_full[0].replace('.', '-')[:-1]
                    self.custom_excludes.add(strip_fn)
                    self.custom_excludes.add(dash_fn)
                    self.custom_excludes.add(
                        f"{strip_fn}-{self.author_full[1]}")
                    self.custom_excludes.add(
                        f"{dash_fn}-{self.author_full[1]}")
                    self.custom_excludes.add(
                        f"{self.author_full[1]}-{strip_fn}")
                    self.custom_excludes.add(
                        f"{self.author_full[1]}-{dash_fn}")
                if "." in self.author_full[1]:
                    strip_ln = self.author_full[1].replace('.', '')
                    dash_ln = self.author_full[1].replace('.', '-')[:-1]
                    self.custom_excludes.add(strip_ln)
                    self.custom_excludes.add(dash_ln)
                    self.custom_excludes.add(
                        f"{strip_ln}-{self.author_full[1]}")
                    self.custom_excludes.add(
                        f"{dash_ln}-{self.author_full[1]}")
                    self.custom_excludes.add(
                        f"{self.author_full[1]}-{strip_ln}")
                    self.custom_excludes.add(
                        f"{self.author_full[1]}-{dash_ln}")
                if len(self.author_full) > 2:
                    if "." in self.author_full[2]:
                        strip_on = self.author_full[2].replace('.', '')
                        dash_on = self.author_full[2].replace('.', '-')[:-1]
                        self.custom_excludes.add(strip_on)
                        self.custom_excludes.add(dash_on)
                        self.custom_excludes.add(
                            f"{strip_on}-{self.author_full[1]}")
                        self.custom_excludes.add(
                            f"{dash_on}-{self.author_full[1]}")
                        self.custom_excludes.add(
                            f"{self.author_full[1]}-{strip_on}")
                        self.custom_excludes.add(
                            f"{self.author_full[1]}-{dash_on}")
                    strip_n1 = self.author_full[0].replace('.', '')
                    strip_n2 = self.author_full[1].replace('.', '')
                    strip_n3 = self.author_full[2].replace('.', '')
                    dash_n1 = self.author_full[0].replace('.', '-')
                    dash_n2 = self.author_full[1].replace('.', '-')
                    dash_n3 = self.author_full[2].replace('.', '-')
                    self.custom_excludes.add(
                        f"{self.author_full[0]}-{self.author_full[1]}-{self.author_full[2]}")
                    self.custom_excludes.add(self.author_full[2])
                    self.custom_excludes.add(
                        f"{self.author_full[0]}-{self.author_full[2]}")
                    self.custom_excludes.add(
                        f"{self.author_full[2]}-{self.author_full[0]}")
                    self.custom_excludes.add(
                        f"{strip_n1}-{strip_n2}-{strip_n3}")
                    self.custom_excludes.add(
                        f"{strip_n3}-{strip_n1}-{strip_n2}")
                    self.custom_excludes.add(f"{dash_n1}-{dash_n2}-{dash_n3}")
                    self.custom_excludes.add(f"{dash_n1}-{dash_n2}{dash_n3}")
                    self.custom_excludes.add(f"{dash_n3}-{dash_n1}-{dash_n2}")

                if self.series_title.lower().startswith("a "):
                    check_title = self.series_title[2:].lower().replace(
                        ' ', '-')
                    self.custom_excludes.add(check_title)
                if self.series_title.lower().startswith("an "):
                    check_title = self.series_title[3:].lower().replace(
                        ' ', '-')
                    self.custom_excludes.add(check_title)
                if self.series_title.lower().startswith("the "):
                    check_title = self.series_title[4:].lower().replace(
                        ' ', '-')
                    self.custom_excludes.add(check_title)
            except IndexError:
                print("index error; oops")
                traceback.print_exc()

            except:
                print("other exception")
                traceback.print_exc()

    # def __str__(self):
    #     print('Goodreads ID: ', self.gr_id)
    #     print('ISBN: ', self.isbn)
    #     print('ISBN13: ', self.isbn13)
    #     print('Title: ', self.title)
    #     print('Series Title: ', self.series_title)
    #     print('Publication Year: ', self.publication_year)
    #     print('Goodreads Link: ', self.gr_link)
    #     print('Author: ', self.author)
    #     print('Custom Keyword Exclusions: ', self.custom_excludes)
    #     print('Keywords: ', self.keywords)
    #     print('LibraryThing ID: ', self.lt_id)
    #     print('LibraryThing Haikus: ', self.lt_haiku_summaries)


if __name__ == '__main__':
    Suggested_Book('greyhaven').__str__()
