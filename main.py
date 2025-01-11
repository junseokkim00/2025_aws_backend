from fastapi import FastAPI
from assets import PLACESKINS, ACCESSORIES, TALES
from utils import add_table, add_item, update_item, fetch_all
import json
import random

import sqlite3

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
    connection = sqlite3.connect("./my_db")
    rows = connection.execute("SELECT * FROM user_info")
    result = {}
    for row in rows:
        row_name, row_id = row[0], row[1]
        result[row_name] = result[row_id]
    return result

@app.get("/get_random_scooter_log/")
def get_random_scooter_log():
    with open("./scooter_log.json", "r") as f:
        data = json.load(f)
    inst = random.choice(data)
    return inst

@app.get("/generate_tale")
def get_tale():
    return {'tale': random.choice(TALES)}

@app.get("/gacha")
def get_random_prize():
    value = random.choice(ACCESSORIES)
    return value

@app.put("/set_inventory_info")
def put_data(inst):
    add_item(table_name="inventory", new_item=inst)
    connection = sqlite3.connect("./my_db")
    rows = connection.execute("SELECT * FROM inventory")
    result = []
    for row in rows:
        row_id, row_name, row_type = row[0], row[1], row[2]
        result.append({
            "id": row_id,
            "name": row_name,
            "type": row_type
        })
    return result