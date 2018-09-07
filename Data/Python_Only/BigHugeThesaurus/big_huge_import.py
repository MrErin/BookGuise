# This import needs to accept input of a set of keywords and loop through them, for each one turning back a list of synonyms. This list needs to be accumulated and then used as search terms for the books in the database.
# Since I want the result set to be unique, it should be a set.

import json
import requests


with open('Data/DataFiles/config.json', 'r') as config_file:
    config = json.load(config_file)

keywords = ["love", "circuses", "lovely"]
dev_key = config['Big_Huge_Thesaurus_key']
all_words = set()

for current_word in keywords:
    # TODO: handle spaces and special characters per keyword here.
    # TODO: Also, how does the API handle plurals?
    # TODO: set up the import so it's sending the unique list to one set that can then be compared against the database

    bht_request = "http://words.bighugelabs.com/api/2/{0}/{1}/json".format(
        dev_key, current_word)
    print(bht_request)
    response = requests.get(bht_request)
    if response.status_code == 404:
        print(f'{current_word} generated 404')
    else:
        data = response.json()
# bht_request = 'Data/Python_Only/BigHugeThesaurus/sample.json'

        adjective_synonyms = set()
        noun_synonyms = set()
        verb_synonyms = set()

        # with open(bht_request) as request:
        #     data = json.load(request)

        if "adjective" in data:
            for synonym in data["adjective"]["syn"]:
                adjective_synonyms.add(synonym)
        if "noun" in data:
            for synonym in data["noun"]["syn"]:
                noun_synonyms.add(synonym)
        if "verb" in data:
            for synonym in data["verb"]["syn"]:
                verb_synonyms.add(synonym)
        all_words = adjective_synonyms | verb_synonyms | noun_synonyms
        print("Adjectives: ", adjective_synonyms)
        print("Nouns: ", noun_synonyms)
        print("Verbs: ", verb_synonyms)
        print("Everything: ", all_words)
