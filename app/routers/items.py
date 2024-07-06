import os
import json
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.item import Item

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/items.json")

def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def write_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@router.get("/", response_model=List[Item])
async def read_items():
    return read_data()

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    items = read_data()
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/", response_model=Item)
async def create_item(item: Item):
    items = read_data()
    item_dict = item.dict()
    item_dict["id"] = len(items) + 1
    items.append(item_dict)
    write_data(items)
    return item_dict
