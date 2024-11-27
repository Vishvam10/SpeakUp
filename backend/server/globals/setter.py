import globals.state as g

from pymongo import MongoClient
from transformers import pipeline


def set_mongodb_client() -> None:
    try:
        client = MongoClient(host="localhost", port=27017)
        g.db_client = client
        g.db_name = "speakup"

    except Exception as e:
        print("Error occurred while connecting to DB : ", e)


def set_audio_classifier() -> None:
    try:
        g.audio_classifer = pipeline(
            "audio-classification",
            model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
            device=0,
        )

    except Exception as e:
        print("Error occurred while connecting to DB : ", e)
