from fastapi import FastAPI
from assets import PLACESKINS, ACCESSORIES, TALES
from utils import add_table, add_item, update_item, fetch_all

import json
import random

app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "World"}

@app.get("/get_current_user_info/")
def get_current_user_info():
    rows = fetch_all('user_info')
    user_info = {row[0]: row[1] for row in rows}
    return user_info
    

    
@app.put("/set_current_user_info")
def set_current_user_info(user_info):
    update_item(table_name='user_info', new_item=user_info)
    return "DONE"
    
        

@app.get("/get_random_scooter_log/")
def get_random_scooter_log():
    with open("./scooter_log.json", "r") as f:
        data = json.load(f)
    inst = random.choice(data)
    return inst

@app.get("/generate_tale")
def get_tale():
    return {'tale': random.choice(TALES)}