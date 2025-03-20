from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage for simplicity
items = {}

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return item

@app.get("/items/", response_model=List[Item])
async def get_items():
    return list(items.values())

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return item

@app.patch("/items/{item_id}", response_model=Item)
async def partial_update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    existing_item = items[item_id]
    if item.name:
        existing_item.name = item.name
    if item.description:
        existing_item.description = item.description
    if item.price:
        existing_item.price = item.price
    if item.tax:
        existing_item.tax = item.tax
    items[item_id] = existing_item
    return existing_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": "Item deleted successfully"}
