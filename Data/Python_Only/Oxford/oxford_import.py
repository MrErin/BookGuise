import requests
import json

database = "Data/DataFiles/DataImports.db"
with open('Data/DataFiles/config.json', 'r') as file:
    config = json.load(file)

app_id = config['Oxford_app_id']
app_key = config['Oxford_key']

language = 'en'
word_id = 'Ace'

url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + \
    language + '/' + word_id.lower() + '/synonyms'

r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})

print(json.dumps(r.json()))
