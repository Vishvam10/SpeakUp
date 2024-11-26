import globals.state as g

from pymongo import MongoClient


def get_global_mongodb_client() -> MongoClient:
    if g.db_client is None:
        print(
            "MongoDB client is not initialized : ",
            g.db_client,
        )
        raise ValueError("Global MongoDB Adapter Manager is not initialized")

    return g.db_client


def get_global_mongodb_db_name() -> str:
    if g.db_name is None:
        print(
            "MongoDB database name is not initialized : ",
            g.db_name,
        )
        raise ValueError("Global MongoDB Adapter Manager is not initialized")

    return g.db_name
