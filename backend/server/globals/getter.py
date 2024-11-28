import globals.state as g

from pymongo import MongoClient
from storage.s3 import S3Storage


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


def get_global_audio_classifier() -> str:
    if g.audio_classifer is None:
        print(
            "Audio classifier is not initialized : ",
            g.audio_classifer,
        )
        raise ValueError("Global audio classifier is not initialized")

    return g.audio_classifer


def get_global_image_classifier() -> str:
    if g.image_classifier is None:
        print(
            "Image classifier is not initialized : ",
            g.image_classifier,
        )
        raise ValueError("Global image classifier is not initialized")

    return g.image_classifier


def get_global_s3_storage() -> S3Storage:
    if g.s3_storage is None:
        print(
            "S3 storage is not initialized : ",
            g.s3_storage,
        )
        raise ValueError("Global S3 storage is not initialized")

    return g.s3_storage
