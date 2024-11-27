from typing import Dict
from typing_extensions import Literal

from database.adapter import MongoDBAdapter


collections = Literal["user", "asset", "report", "analysis"]
adapters: Dict[collections, MongoDBAdapter] = {}


def get_adapter(collection_name: collections) -> MongoDBAdapter:
    if collection_name not in adapters:
        adapters[collection_name] = MongoDBAdapter(collection_name)

    return adapters[collection_name]
