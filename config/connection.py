
# from mongoengine import connect
from dotenv import load_dotenv
import os
import pymongo
load_dotenv()
mongodb = os.getenv("mongodb")
myclient = pymongo.MongoClient(mongodb)
mydb = myclient["mydatabase"]