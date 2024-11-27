from pymongo import MongoClient
from transformers import pipeline

from storage.s3 import S3Storage

db_client: MongoClient = None
db_name: str = ""

audio_classifer : pipeline = None
s3_storage : S3Storage = None
