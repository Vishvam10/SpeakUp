from typing import List, Optional, Dict
from datetime import datetime, timezone

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from globals.getter import get_global_mongodb_client, get_global_mongodb_db_name


class MongoDBAdapter:
    def __init__(self, collection_name: str):
        try:
            client = get_global_mongodb_client()
            db_name = get_global_mongodb_db_name()
            db = client.get_database(db_name)
            self.collection: Collection = db[collection_name]
        except PyMongoError as e:
            print(f"Error initializing MongoDB client : {e}")
            raise

    @staticmethod
    def str_id(id: ObjectId) -> str:
        try:
            return str(id)
        except Exception as e:
            print(f"Error converting ObjectId to string : {e}")
            raise

    def insert_one(self, data: dict) -> str:
        try:
            document_data = {**data}
            result = self.collection.insert_one(document_data)
            return result
        except PyMongoError as e:
            print(f"Error creating document : {e}")
            raise

    def insert_many(self, data: list) -> str:
        try:
            result = self.collection.insert_many(data)
            return result
        except PyMongoError as e:
            print(f"Error creating document : {e}")
            raise

    def _remove_id_field(self, document: dict) -> dict:
        if "_id" in document:
            del document["_id"]
        return document

    def find_one(self, filter: Dict = {}, query: Dict = {}) -> Optional[dict]:
        try:
            query["_id"] = 0

            document = self.collection.find_one(filter, query)
            if document:
                return self._remove_id_field(document)
            return None
        except PyMongoError as e:
            print(f"Error finding document : {e}")
            raise

    def find_all(self, filter: Dict = {}, query: Dict = {}) -> List[dict]:
        try:
            query["_id"] = 0
            result = list(self.collection.find(filter, query))
            return [self._remove_id_field(doc) for doc in result]
        except PyMongoError as e:
            print(f"Error finding documents : {e}")
            raise

    def update(self, filter: Dict = {}, data: Dict = {}) -> Optional[dict]:
        try:
            now = datetime.now(timezone.utc)
            update_data = {"$set": {**data, "updated_at": now}}
            result = self.collection.update_one(filter, update_data)
            return result
        except PyMongoError as e:
            print(f"Error updating document : {e}")
            raise

    def delete(self, filter: Dict = {}) -> bool:
        try:
            result = self.collection.delete_one(filter)
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting document : {e}")
            raise
