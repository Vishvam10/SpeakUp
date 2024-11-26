import globals.state as g

from pymongo import MongoClient


def set_mongodb_client() -> None:
    try:
        client = MongoClient(host="localhost", port=27017)
        g.db_client = client
        g.db_name = "speakup"

    except Exception as e:
        print("Error occurred while connecting to DB : ", e)
