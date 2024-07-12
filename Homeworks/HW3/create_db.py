
import json
from pymongo import MongoClient

# подключение к серверу MangoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['zomato'] # выбор бзд

collection = db['restaurants']

with open('zomato.json', 'r') as file:
    data = json.load(file)

data_list = []
for dat in data:
    if dat.get('restaurants'):
        for restaurant in dat["restaurants"]:
            data_list.append(restaurant['restaurant'])

collection.insert_many(data_list)