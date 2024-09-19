from firebase_admin import credentials, initialize_app, auth, db
from fastapi import UploadFile, File
import app.models.model_types as modelType
from app.helpers import ai_helpers
from app.utils import utils
import json
from typing import *
import os
import firebase_admin
from fastapi import APIRouter, HTTPException

# Initialize the Firebase Admin SDK with the downloaded service account key
# cred = credentials.Certificate("D:/DdriveCodes/SIH/app/helpers/kisaandvaar-firebase-adminsdk-t83e9-f6d6bf9844.json")
# initialize_app(cred)

#auth = auth()

router = APIRouter()

@router.post("/create-inventory-item")
def create_inventory_item(name, category, quantity, storage, description, price, item_id=None, rating=0.0, item_status="in stock"):
    try:
        storage_collection = db.collection(storage)  # Use storage as collection name

        # Generate a unique ID if item_id is not provided
        if not item_id:
            item_id = storage_collection.document().id

        doc_ref = storage_collection.document(item_id)
        doc_ref.set({
            "name": name,
            "category": category,
            "quantity": {
                "value": quantity,
                "unit": "kg"  # kg, gm, pound, etc options
            },
            "storage": storage,  # self_stored or externally_stored
            "description": description,
            "price": {
                "value": price,
                "unit": "kg"  # kg, gm, pound, etc options
            },
            "ratings": [],  # an empty list for ratings
            "average_rating": 0.0,  # Initialize average rating to zero
            "item_status": item_status,  # item status field (in stock, sold, etc)
        })
        print("Inventory item created:", doc_ref)

        return {"status": "success", "message": "Inventory item created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to retrieve all items from the inventory based on storage type.
@router.get("/inventory/<storage>")
def get_items1(storage):
    try:
        storage_collection = db.collection(storage)  # Use storage type as collection name
        docs = storage_collection.get()
        items = []
        for doc in docs:
            items.append(doc.to_dict())
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to retrieve all items from the inventory.
@router.get("/inventory")
def get_items():
    try:
        self_stored_collection = db.collection("self_stored")
        self_stored_docs = self_stored_collection.get()

        externally_stored_collection = db.collection("externally_stored")
        externally_stored_docs = externally_stored_collection.get()

        all_items = []
        all_items.extend(doc.to_dict() for doc in self_stored_docs)
        all_items.extend(doc.to_dict() for doc in externally_stored_docs)

        return all_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example usage:
# create_inventory_item("Apples", "fruits", 10, "self", "Fresh, red apples", 20)
@router.delete("/inventory/<storage>/<item_id>")
def delete_item(storage, item_id):
    try:
        storage_collection = db.collection(storage)
        doc_ref = storage_collection.document(item_id)
        doc_ref.delete()
        return {"status": "success", "message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/inventory/<storage>/<item_id>")
def update_item(storage, item_id, name: Optional[str] = None, category: Optional[str] = None, quantity: Optional[int] = None, description: Optional[str] = None, price: Optional[float] = None):
    try:
        storage_collection = db.collection(storage)
        doc_ref = storage_collection.document(item_id)

        data = {}
        if name is not None:
            data["name"] = name
        if category is not None:
            data["category"] = category
        if quantity is not None:
            data["quantity"] = quantity
            if quantity == 0:
                data["item_status"] = "out of stock"
        if description is not None:
            data["description"] = description
        if price is not None:
            data["price"] = price

        doc_ref.update(data)
        return {"status": "success", "message": "Item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))