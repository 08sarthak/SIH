from fastapi import APIRouter, Depends, UploadFile,File
import app.controllers.market as controller
import app.controllers.chatbot as controller2
import app.models.model_types as model_type
from app.utils import utils
from typing import List

router = APIRouter()

@router.post("/market-trends")
async def display_market_trends():
    try:
        # response = await auth.sign_up_user(
        #     email=sign_up_request.email,
        #     password=sign_up_request.password,
        # )
        trends = await controller.display_market_trends()
        print("TREND:",trends)
        #respponse = utils.prettify_response(trends)
        return {
            "status": "success",
            "message": "Here are the required market trends",
            "data": trends
        }
    except Exception as e:
        return {
            "status": False,
            "message": f"An error occurred: {e}",
            "data": None
        }

@router.post("/price-recoomendation")
async def price_recommend(crop_data:model_type.CropData):
    try:
        # response = await auth.sign_up_user(
        #     email=sign_up_request.email,
        #     password=sign_up_request.password,
        # )
        price = await controller2.recommend_price(crop_data)
        print("PRICE:",price)
        #respponse = utils.prettify_response(trends)
        return {
            "status": "success",
            "message": "Here are the required market trends",
            "data": price
        }
    except Exception as e:
        return {
            "status": False,
            "message": f"An error occurred: {e}",
            "data": None
        }
        
