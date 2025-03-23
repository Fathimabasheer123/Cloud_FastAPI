from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List,Optional

app = FastAPI()

items=[]
class Item(BaseModel):
    id:int
    name: str
    description:Optional[str] =None
    price: float
    stock: int

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    item_id = len(items) 
    item.id = item_id 
    items.append(item)
    return {"message": "Item added successfully", "item": item}



@app.get("/items/", response_model=List[Item])
def get_items():
    return items

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
        raise HTTPException(status_code=404, detail="Item not found")
   


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id >=len(items) or item_id<0:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return item


@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    if item_id >=len(items) or item_id<0:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items.pop(item_id)
    return deleted_item
