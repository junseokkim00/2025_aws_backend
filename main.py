from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from assets import PLACESKINS, ACCESSORIES, TALES
from utils import add_table, add_item, update_item, fetch_all, fetch_condition
import json
import random

import sqlite3

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"Hello": "World"}

@app.get("/get_current_user_info/")
def get_current_user_info():
    rows = fetch_all('user_info')
    user_info = {row[0]: row[1] for row in rows}
    print(user_info)
    return user_info
    
@app.post("/set_current_user_info/")
def set_current_user_info(user_info: dict):
    update_item(table_name="user_info", new_item=user_info)
    connection = sqlite3.connect("./my_db", timeout=20, isolation_level=None)
    rows = connection.execute("SELECT * FROM user_info")
    result = {}
    for row in rows:
        row_name, row_id = row[0], row[1]
        print(row_name, row_id)
        result[row_name] = row_id
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

@app.get("/gacha/")
def get_random_prize():
    value = random.choice(ACCESSORIES)
    print(value)
    return value

@app.get("/get_accessories/{acc_type}")
def get_accessories(acc_type):
    rows = fetch_condition(table_name="inventory", type=acc_type)
    result = []
    for row in rows:
        inst = {
            'id': row[0],
            'name': row[1],
            'type': row[2]
        }
        result.append(inst)
    return result


    

@app.post("/set_inventory_info")
def put_data(inst: dict):
    add_item(table_name="inventory", new_item=inst)
    connection = sqlite3.connect("./my_db", timeout=20, isolation_level=None)
    rows = connection.execute("SELECT * FROM inventory")
    result = []
    for row in rows:
        row_id, row_name, row_type = row[0], row[1], row[2]
        result.append({
            "id": row_id,
            "name": row_name,
            "type": row_type
        })
    print(result)
    return result