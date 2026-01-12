from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, auth, schema
from .database import get_db, engine, Session as session
import pandas as pd

app = FastAPI(title="SIMPROSYS PROJECT")

models.Base.metadata.create_all(engine)

@app.get("/get_token")
def get_token():
    data = {"username" : "Deep",
            "password" : 123}
    
    token = auth.create_access_token(data=data)
    return {"token":token}

@app.post("/login")
def verify_token(token:str):
    return auth.validate_token(token)

@app.post("/create_product", response_model=schema.ProductOut)
def create_product(product:schema.ProductCreate, db:Session=Depends(get_db), token:str=Depends(auth.validate_token)):
    new_product = models.Product(
        title = product.title,
        description = product.description,
        price = product.price,
        status = product.status,
        category_id = product.category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@app.post("/create_category", response_model=schema.CategoryOut)
def create_category(category:schema.CategoryCreate, db:Session=Depends(get_db), token:str=Depends(auth.validate_token)):
    new_category = models.Category(
        name = category.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@app.get("/search/product/{product_id}")
def search_product(id: int, db:Session=Depends(get_db), token:str=Depends(auth.validate_token)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    return product

@app.put("/update/product/{product_id}", response_model=schema.ProductOut)
def update_item(id:int,product:schema.ProductCreate, db:Session=Depends(get_db), token:str=Depends(auth.validate_token)):
    db_item = db.query(models.Product).filter(models.Product.id == id).first()
    db_item.title = product.title
    db_item.description = product.description
    db_item.price = product.price
    db_item.status = product.status
    db_item.category_id = product.category_id
    db.commit()
    return db_item

@app.delete("/product/{product_id}")
def delete_item(id: int,db:Session=Depends(get_db), token:str=Depends(auth.validate_token)):
    db_item = db.query(models.Product).filter(models.Product.id == id).first()
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}

@app.get("/get_product_list")
def download_csv(db:Session=Depends(get_db), token:str=Depends(auth.validate_token)):

    try:
        df = pd.read_sql_table("product", engine)
        df.to_csv("ProductList.csv", index=False)
        return {"message":"CSV Downloaded"}
    except:
        return {"message" : "Error while creating CSV"}

def create_dummy_product(product_id : int, no_of_copies : int):
    
    db = session()
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    for _ in range(no_of_copies):
        dummy_product = models.Product(
        title = product.title,
        description = product.description,
        price = product.price,
        status = product.status,
        category_id = product.category_id
        )

        db.add(dummy_product)
        db.commit()

@app.post("/add_dummy_product/{product_id}")
def add_dummy(background_tasks:BackgroundTasks, product_id : int, no_of_copies : int, token:str=Depends(auth.validate_token)):
    try:
        background_tasks.add_task(create_dummy_product, product_id, no_of_copies)
        return {"message" : "Your request has been accepted and processing..."}
    except:
        raise HTTPException(status_code=400, detail="There is some issue in createing dummy products")

