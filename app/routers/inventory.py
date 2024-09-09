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
cred = credentials.Certificate("C:\Users\Khwaish\Downloads\kisaandvaar-firebase-adminsdk-t83e9-f6d6bf9844.json")
initialize_app(cred)

auth = auth()

router = APIRouter()

@router.post("/create-inventory-item")
def create_inventory_item(name, category, quantity, storage, description, price):
    try:
        doc_ref = db.collections("inventory").document()
        # doc_ref = db.collection("inventory").document()
        doc_ref.set({
            "name": name,
            "category": category,
            "quantity": {
                "value": quantity,
                "unit": "kg"  # kg, gm, pound, etc options
            },
            "storage": storage,
            "description": description,
            "price": {
                "value": price,
                "unit": "kg"  # kg, gm, pound, etc options
            }
        })
        print("Inventory item created:", doc_ref)
        
        return {"status": "success", "message": "Inventory item created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example usage:
# create_inventory_item("Apples", "fruits", 10, "self", "Fresh, red apples", 20)
