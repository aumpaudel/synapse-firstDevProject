from fastapi import FastAPI 
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float 
    is_available: bool = True

app = FastAPI()
items_db = []

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/about")
def about():
    return {"message": "This is about page"}

@app.get("/user/{id}")
def user(id: int):
    return {"user_id": id}

@app.get("/search")
def search(q: str, page:int = 1, limit: int = 10):
    return {"query": q, "page": page, "limit": limit}

@app.post("/submit")
def create_item(item: Item):
    items_db.append(item)
    return {"received": item}

@app.get("/items")
def get_items():
    return {"items": items_db, "count": len(items_db)} 

@app.delete("/items")
def delete_all_items():
    items_db.clear()  
    return {"message": "All items deleted", "items_remaining": len(items_db)}