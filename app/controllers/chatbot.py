from fastapi import UploadFile, File
import app.models.model_types as model_type
from app.helpers import ai_helpers
from app.utils import utils
import json
from typing import *


async def chatbot(query: model_type.Query):
    chat = query.query
    result = ai_helpers.chatbot(chat)
    return result

async def recommend_price(crop: model_type.CropData):
    result = ai_helpers.price_recommend(crop)
    return result