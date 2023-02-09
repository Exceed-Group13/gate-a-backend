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

class Setting(BaseModel):
    house_name: str
    delay: int

class Pin(BaseModel):
    house_name: str
    old_pin: str
    new_pin:str
    
class HomeDetail(BaseModel):
    state: bool
    house_name: str
    
class PinDetail(BaseModel):
    pin: str
    house_name: str

data = [{
    "state": False,
    "house_name": "house1",
    "delay": 1,
    "pin": "123"
}]

app = FastAPI()
# collection.delete_many({})
# a = collection.insert_many(data)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.put("/setting") 
def setting(detail: Setting):
    """set delay for door to close"""
    sett = collection.find_one_and_update({"house_name": detail.house_name},{'$set': {'delay': detail.delay}}) 
    return {"delay": detail.delay}

@app.get("/setting")
def show_setting():
    """show detail on setting page"""
    sett = collection.find_one({}, {'_id':0})
    return {"house_name": sett['house_name'], "delay": sett['delay']}

@app.put("/resetpin")
def reset_pin(detail: Pin):
    """reset password"""
    pwd = collection.find_one({"house_name": detail.house_name})
    if detail.old_pin == pwd['pin']:
        collection.find_one_and_update({"house_name": detail.house_name},{'$set': {'pin': detail.new_pin}})
        return {"respond": "success"}
    else:
        return {"respond": "unsuccess"}     
    
@app.get("/home")
def show_status():
    """Check the status of the door."""
    door = collection.find({}, {'_id':0})
    tmp = list()
    for d in door:
        tmp.append(d)
    return {'result': tmp}

@app.put("/home")
def control_door(detail: HomeDetail):
    """Close and open the door."""
    collection.find_one_and_update({'house_name': detail.house_name}, 
        {'$set': {'state': detail.state}})
    return {'response': "Door change state successfully"}

@app.put("/regis")
def set_pin(detail: PinDetail):
    """Set the pin for the firt time."""
    ori_db = collection.find_one({}, {'_id':0})
    collection.find_one_and_update({"house_name": ori_db['house_name']}, {'$set': {'pin': detail.pin, 'house_name': detail.house_name}})
    return {'response': "Pin set successfully"}
