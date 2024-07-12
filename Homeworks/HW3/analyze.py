
from pymongo import MongoClient
import json

client = MongoClient()
db = client['zomato']
collection = db['restaurants']

# вывод первой записи в коллекции
all_docs = collection.find()
first_doc = all_docs[0]


# вывод объекта json
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

# коунтер

count = collection.count_documents({})
print(f"число записей в бзд = {count}")

query = {'has_online_delivery':1}
print(f'Количество ресторанов с online-доставкой: {collection.count_documents(query)}')
#
# projections = {"properties.lightcond":1, "properties.weather":1, '_id': 0}
# project_docs = collection.find(query, projections)
# for doc in project_docs:
#     print(doc)
#
query = {'has_table_booking':1}
print(f'Количество ресторанов, в которых возможно резервация стола: {collection.count_documents(query)}')

query = {'average_cost_for_two':{'$lt': 1000}}
print(f'Количество ресторанов со средним чеком на двоих меньше 1000: {collection.count_documents(query)}')

query = {'average_cost_for_two':{'$gte': 5000}}
print(f'Количество ресторанов со средним чеком на двоих больше 5000: {collection.count_documents(query)}')
# query = {'properties.weather':{'$regex': 'rain', '$options': 'i'}}
# print(f'Количество документов аварий во время дождя: {collection.count_documents(query)}')
#
query = {'user_rating.rating_text':{'$in': ['Very Good', 'Excellent']}}
print(f'Количество ресторанов с рейтингом очень хорошо и отлично: {collection.count_documents(query)}')

query = {'user_rating.aggregate_rating':{'$gte': '4.8'}}
print(f'Количество ресторанов с рейтингом выше 4.8: {collection.count_documents(query)}')

query = {'cuisines':{'$in': ['Asian']}}
print(f'Количество ресторанов с азиатской едой: {collection.count_documents(query)}')

query = {'location.city':{'$in': ['New Delhi']}}
print(f'Количество ресторанов в Нью Дели: {collection.count_documents(query)}')