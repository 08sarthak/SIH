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
# cred = credentials.Certificate("C:\Users\Khwaish\Downloads\kisaandvaar-firebase-adminsdk-t83e9-f6d6bf9844.json")
# initialize_app(cred)

auth = auth()

router = APIRouter()

"""
User Cart (in Database):
user_id (reference to the user document)
items (array of objects):
item_id (reference to the inventory item document)
quantity (number)
farm_id (reference to the seller's document) - Required to ensure items are bought from the same farm

API Endpoints:

Add to Cart:
POST /cart/add
Body: item_id (ID of the item to add), quantity (desired quantity)
View Cart:
GET /cart
Retrieve the user's cart items and total bill.
Update Cart Quantity:
PUT /cart/{item_id}
Body: quantity (updated desired quantity)
Remove from Cart:
DELETE /cart/{item_id}
Remove the specified item from the cart.
Empty Cart:
DELETE /cart/empty
Clear all items from the user's cart.

"""


# @router.post("/cart/add")
# async def add_to_cart(item_id: str, quantity: int):
#     """
#     Adds an item to the user's cart.
#     """
#     user_id = get_current_user_id()  # Replace with your authentication logic

#     # Check if item exists
#     inventory_ref = db.reference("inventory").child(item_id)
#     inventory_data = await inventory_ref.get()

#     if not inventory_data.exists():
#         raise HTTPException(status_code=404, detail="Item not found")

#     # Get farm ID from inventory data
#     farm_id = inventory_data.val()["farm"]

#     # Check if cart already has items from a different farm
#     cart_ref = db.reference("carts").child(user_id)
#     cart_snapshot = await cart_ref.get()

#     if cart_snapshot.exists():
#         cart_data = cart_snapshot.val()
#         if cart_data and cart_data["items"] and cart_data["items"][0]["farm_id"] != farm_id:
#             raise HTTPException(status_code=400, detail="Cart can only have items from the same farm")

#     # Update or create cart
#     cart_data = {"items": []} if not cart_snapshot.exists() else cart_snapshot.val()
#     cart_data["items"].append({"item_id": item_id, "quantity": quantity, "farm_id": farm_id})
#     await cart_ref.set(cart_data)

#     return {"message": "Item added to cart successfully"}

# @router.get("/cart")
# async def view_cart():
#     """
#     Retrieves the user's cart items and calculates the total bill.
#     """
#     user_id = get_current_user_id()  # Replace with your authentication logic
#     cart_ref = db.reference("carts").child(user_id)
#     cart_snapshot = await cart_ref.get()

#     cart_data = cart_snapshot.val() if cart_snapshot.exists() else {"items": []}
#     total_bill = 0

#     for item in cart_data.get("items", []):
#         inventory_ref = db.reference("inventory").child(item["item_id"])
#         inventory_data = await inventory_ref.get()
#         if inventory_data.exists():
#             item_price = inventory_data.val()["price"]["value"] * item["quantity"]
#             total_bill += item_price

#     return {"items": cart_data["items"], "total_bill": total_bill}

# @router.put("/cart/{item_id}")
# async def update_cart_quantity(item_id: str, quantity: int):
#     """
#     Updates the quantity of an item in the cart.
#     """
#     user_id = get_current_user_id()  # Replace with your authentication logic
#     cart_ref = db.reference("carts").child(user_id)

#     # Update cart item quantity
#     cart_snapshot = await cart_ref.get()
#     cart_data = cart_snapshot.val() if cart