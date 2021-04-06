from pymongo import MongoClient

connection = MongoClient('')

root_db = connection['RGB']
blacklists = root_db['Blacklists']
main = root_db['Data']
