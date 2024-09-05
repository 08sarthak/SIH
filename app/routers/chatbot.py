from fastapi import APIRouter, Depends, UploadFile,File
import app.controllers.chatbot as controller
import app.models.model_types as model_type
from app.utils import utils
from typing import List

router = APIRouter()

@router.post("/chatbot")
async def chatbot(query:model_type.Query):
    try:
        # response = await auth.sign_up_user(
        #     email=sign_up_request.email,
        #     password=sign_up_request.password,
        # )
        reply = await controller.chatbot(query)
        print("TREND:",reply)
        #respponse = utils.prettify_response(trends)
        return {
            "status": "success",
            "message": "Here are the required market trends",
            "data": reply
        }
    except Exception as e:
        return {
            "status": False,
            "message": f"An error occurred: {e}",
            "data": None
        }