from fastapi import UploadFile, File
import app.models.model_types as modelType
from app.helpers import ai_helpers
from app.utils import utils
import json
from typing import *
import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException

# Initialize the Firebase Admin SDK with the downloaded service account key
cred = credentials.Certificate("D:/DdriveCodes/SIH/app/helpers/kisaandvaar-firebase-adminsdk-t83e9-f6d6bf9844.json")
firebase_admin.initialize_app(cred)


# async def sign_up_user(sign_up_request: modelType.SignUpRequest):
#     try:
#         # Create a new user
#         user = auth.create_user(
#             email=sign_up_request.email,
#             password=sign_up_request.password,
#         )
#         print('Successfully created new user:', user.uid)
#         return user
#     except Exception as e:
#         print(f"Error creating user: {e}")
#         return None

async def sign_up_user(sign_up_request: modelType.SignUpRequest):
    try:
        # Create a new user
        user = auth.create_user(
            email=sign_up_request.email,
            password=sign_up_request.password,
            display_name=sign_up_request.username,
            phone_number=sign_up_request.phonenumber
        )
        print('Successfully created new user:', user)
        return user
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def login(login_request: modelType.LoginRequest):
    try:
        user = await auth.get_user_by_email(
            email=login_request.email
            )

        return user
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")

# Example usage
#new_user = sign_up_user("user@example.com", "strongpassword123")
