from typing import List, Optional
from datetime import datetime, timezone

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult

from globals.getter import get_global_mongodb_client, get_global_mongodb_db_name


class MongoDBAdapter:
    def __init__(self, collection_name: str):
        client = get_global_mongodb_client()
        db_name = get_global_mongodb_db_name()
        db = client.get_database(db_name)

        print("\n\nTF : ", db_name)

        self.collection: Collection = db[collection_name]

    @staticmethod
    def str_id(id: ObjectId) -> str:
        return str(id)

    def create(self, data: dict) -> str:
        now = datetime.now(timezone.utc)
        document_data = {
            **data,
            "created_at": now,
            "updated_at": now,
            "deleted_at": None,
        }
        result: InsertOneResult = self.collection.insert_one(document_data)
        return self.str_id(result.inserted_id)

    def get(self, document_id: str) -> Optional[dict]:
        document = self.collection.find_one({"_id": ObjectId(document_id)})
        if document:
            document["_id"] = self.str_id(document["_id"])
        return document

    def get_all(self) -> List[dict]:
        documents = self.collection.find()
        return [{"_id": self.str_id(doc["_id"]), **doc} for doc in documents]

    def update(self, document_id: str, data: dict) -> Optional[dict]:
        now = datetime.now(timezone.utc)
        update_data = {"$set": {**data, "updated_at": now}}
        result: UpdateResult = self.collection.update_one(
            {"_id": ObjectId(document_id)}, update_data
        )

        if result.matched_count > 0:
            return self.get(document_id)
        return None

    def delete(self, document_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count > 0
