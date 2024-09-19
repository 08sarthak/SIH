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

"""
The marketplace should list items based on the category of the items, and also based on other filters 
like quanity, farmer/farm, location, price, ratings, etc in ascending order. It should not display out of stock items. 
It should retrive all the listings made by farmer accounts based on these conditions.
The endpoints to be used are:

/marketplace
/marketplace/query={query}
/marketplace/{item_category}
/marketplace/{item_category}/query={query}
/marketplace/{farm}/query={query}
/marketplace/{pincode}/query={query}
/marketplace/query={query}/sorted_by_ratings
/marketplace/query={query}/sorted_by_price
/marketplace/query={query}/sorted_by_quantity

args:
- item_category: str OR Other filters 
- query: str
return:
- list of items

TODO:
Implement being able to specify a location's radius:
eg. 100 km range from 201305 pincode
TODO:
Multiple filters applied at the same time is currently out of scope, implement later.

"""

def find_common_items(query_results1, query_results2):
    """
    Finds common items in two query results.
    """
    items1_set = set(query_results1)
    items2_set = set(query_results2)
    common_items_set = items1_set.intersection(items2_set)
    return common_items_set

@router.get("/marketplace")
async def get_all_marketplace_items():
  """
  Retrieves all in-stock listings from the database.
  """
  inventory_ref = db.reference("inventory")
  # Query documents where item_status is "in stock"
  query = inventory_ref.where("item_status", "==", "in stock")
  documents = query.get()

  items = []
  for doc in documents:
    # item_data = doc.to_dict()
    item_data = dict(doc)
    items.append(item_data)

  return items

@router.get("/marketplace/query={query}")
async def get_marketplace_items_by_query(query):
    """
    Retrieves marketplace items based on a search query.
    """
    inventory_ref = db.reference("inventory")
    # Query documents where the name or description contains the query
    query_results = inventory_ref.order_by_child("name").start_at(query).end_at(query + "\uf8ff").get()

    items = []
    for doc in query_results:
        #item_data = dict(doc)
        # item_data = doc.to_dict()
        if item_data["item_status"] == "in stock":  # Filter in-stock items
            items.append(item_data)

    return items

# @router.get("/marketplace/{item_category}/query={query}")
# async def get_marketplace_items_by_category_and_query(item_category: str, query: str):
#     """
#     Retrieves marketplace items based on a category and search query.
#     """
#     inventory_ref = db.reference("inventory")
    
#     # Query documents where the category matches and the name or description contains the query
#     query_results = inventory_ref.order_by_child("category").start_at(item_category).end_at(item_category + "\uf8ff")
#     query_results2 = inventory_ref.order_by_child("name").start_at(query).end_at(query + "\uf8ff")
    
#     items = []
#     for doc in query_results:
#         # item_data = doc.to_dict()
#         item_data = dict(doc)
#         if item_data["item_status"] == "in stock":  # Filter in-stock items
#             items.append(item_data)

#     return items

@router.get("/marketplace/{item_category}/query={query}")
async def get_marketplace_items_by_category_and_query(item_category, query):
    """
    Retrieves items based on category and a search query.
    """
    inventory_ref = db.reference("inventory")
    # Query documents by category and search query
    query_results = inventory_ref.order_by_child("category").start_at(item_category).end_at(item_category + "\uf8ff")
    query_results2 = inventory_ref.order_by_child("name").start_at(query).end_at(query + "\uf8ff")

    # Find common items
    common_items_Set = find_common_items(query_results, query_results2)
    
    items = []
    for doc in common_items_Set:
        # item_data = doc.to_dict()
        item_data = dict(doc)
        if item_data["item_status"] == "in stock":  # Filter in-stock items
            items.append(item_data)

    return items

@router.get("/marketplace/{farm}/query={query}")
async def get_marketplace_items_by_farm_and_query(farm, query):
    """
    Retrieves items based on farm and a search query.
    """
    inventory_ref = db.reference("inventory")
    # Query documents by farm and search query
    query_results = inventory_ref.order_by_child("farm").start_at(farm).end_at(farm + "\uf8ff")
    query_results2 = inventory_ref.order_by_child("name").start_at(query).end_at(query + "\uf8ff")

    # Find common items
    common_items_set = find_common_items(query_results, query_results2)

    items = []
    for doc in common_items_set:
        item_data = dict(doc)
        if item_data["item_status"] == "in stock":  # Filter in-stock items
            items.append(item_data)

    return items

@router.get("/marketplace/{item_category}")
async def get_marketplace_items_by_category(item_category):
    """
    Retrieves items based on category.
    """
    inventory_ref = db.reference("inventory")
    # Query documents by category
    query_results = inventory_ref.order_by_child("category").start_at(item_category).end_at(item_category + "\uf8ff")

    items = []
    for doc in query_results:
        item_data = dict(doc)
        if item_data["item_status"] == "in stock":  # Filter in-stock items
            items.append(item_data)

    return items

@router.get("/marketplace/query={query}/sort_by_price")
async def get_marketplace_items_by_query_and_sort_by_price(query):
    """
    Retrieves items based on a search query and sorts them by price.
    """
    inventory_ref = db.reference("inventory")

    # Query documents where name or description contains the query
    query_results = inventory_ref.order_by_child("name").start_at(query).end_at(query + "\uf8ff")
    query_results2 = inventory_ref.order_by_child("description").start_at(query).end_at(query + "\uf8ff")

    # Find common items
    common_items_set = find_common_items(query_results, query_results2)

    # Sort common items by price
    sorted_items = sorted(common_items_set, key=lambda item: item["price"]["value"])

    return sorted_items

@router.get("/marketplace/query={query}/sort_by_quantity")
async def get_marketplace_items_by_query_and_sort_by_quantity(query):
    """
    Retrieves items based on a search query and sorts them by quantity.
    """
    inventory_ref = db.reference("inventory")

    # Query documents where name or description contains the query
    query_results = inventory_ref.order_by_child("name").start_at(query).end_at(query + "\uf8ff")
    query_results2 = inventory_ref.order_by_child("description").start_at(query).end_at(query + "\uf8ff")

    # Find common items
    common_items_set = find_common_items(query_results, query_results2)

    # Sort common items by quantity
    sorted_items = sorted(common_items_set, key=lambda item: item["quantity"]["value"])

    return sorted_items

@router.get("/marketplace/query={query}/sorted_by_ratings")
async def get_marketplace_items_by_query_and_sort_by_ratings(query):
    """
    Retrieves items based on a search query and sorts them by average rating.
    """
    inventory_ref = db.reference("inventory")

    # Query documents where name or description contains the query
    query_results = inventory_ref.order_by_child("name").start_at(query).end_at(query + "\uf8ff")
    query_results2 = inventory_ref.order_by_child("description").start_at(query).end_at(query + "\uf8ff")

    # Find common items
    common_items_set = find_common_items(query_results, query_results2)

    # Sort common items by average rating
    sorted_items = sorted(common_items_set, key=lambda item: item["average_rating"], reverse=True)

    return sorted_items

@router.get("/marketplace/{pincode}/query={query}")
async def get_marketplace_items_by_pincode_and_query(pincode, query):
    """
    Retrieves items based on a pincode and a search query.
    """
    inventory_ref = db.reference("inventory")

    # Query documents by pincode and search query
    query_results = inventory_ref.order_by_child("pincode").start_at(pincode).end_at(pincode + "\uf8ff")
    query_results2 = inventory_ref.order_by_child("name").start_at(query).end_at(query + "\uf8ff")

    # Find common items
    common_items_set = find_common_items(query_results, query_results2)

    items = []
    for doc in common_items_set:
        item_data = dict(doc)
        if item_data["item_status"] == "in stock":  # Filter in-stock items
            items.append(item_data)

    return items