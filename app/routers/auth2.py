from firebase_admin import credentials, initialize_app, auth
from fastapi import UploadFile, File
import app.models.model_types as modelType
from app.helpers import ai_helpers
from app.utils import utils
import json
from typing import *
import os
import firebase_admin


# Initialize the Firebase Admin SDK with the downloaded service account key
cred = credentials.Certificate("C:\Users\Khwaish\Downloads\kisaandvaar-firebase-adminsdk-t83e9-f6d6bf9844.json")
initialize_app(cred)

auth = auth()

from fastapi import APIRouter, HTTPException

router = APIRouter()
@router.post("/login")
async def login(login_request: modelType.LoginRequest):
    try:
        user = await auth.get_user_by_email(
            email=login_request.email,
            password=login_request.password
            )

        # Generate a custom token if needed for API access control (optional)

        return user
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")

async def sign_up_user(sign_up_request: modelType.SignUpRequest):
    try:
        # Create a new user
        user = auth.create_user(
            email=sign_up_request.email,
            password=sign_up_request.password,
        )
        print('Successfully created new user:', user.uid)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example usage
#new_user = sign_up_user("user@example.com", "strongpassword123")