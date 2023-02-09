from fastapi import FastAPI, HTTPException, Body
from datetime import time, datetime, date, timedelta
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import urllib
from fastapi.middleware.cors import CORSMiddleware

load_dotenv('.env')

user = os.getenv('user')
password = urllib.parse.quote(str(os.getenv('password')))
client = MongoClient(f"mongodb://{user}:{password}@mongo.exceed19.online:8443/?authMechanism=DEFAULT")

db = client["exceed13"] #use database name
collection = db['gate-a'] # db.collection_name

class Door(BaseModel):
    state: bool
    house_name: str
    delay: int
    pin: str


data = [{
    "state": False,
    "house_name": "house1",
    "delay": 1,
    "pin": "123"
}]

app = FastAPI()
collection.delete_many({})
a = collection.insert_many(data)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
