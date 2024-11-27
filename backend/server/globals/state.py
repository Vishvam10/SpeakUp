from pymongo import MongoClient
from transformers import pipeline

db_client: MongoClient = None
db_name: str = ""

audio_classifer : pipeline = None
