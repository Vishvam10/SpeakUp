import os
from dotenv import load_dotenv

import globals.state as g

load_dotenv()


def set_mongodb_client() -> None:
    from pymongo import MongoClient

    try:
        client = MongoClient(host="localhost", port=27017)
        g.db_client = client
        g.db_name = "speakup"

    except Exception as e:
        print("Error occurred while connecting to DB : ", e)


def set_audio_classifier() -> None:
    from transformers import pipeline

    try:
        g.audio_classifer = pipeline(
            "audio-classification",
            model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
            device=0,
        )

    except Exception as e:
        print("Error occurred while connecting to DB : ", e)


def set_s3_storage() -> None:
    from storage.s3 import S3Storage

    try:
        bucket_name = os.getenv("S3_BUCKET_NAME", "")

        g.s3_storage = S3Storage(bucket_name=bucket_name)
        g.s3_storage.connect()

    except Exception as e:
        print("Error occurred while connecting to S3: ", e)
        raise
