from fastapi import UploadFile, File
import app.models.model_types as modelType
from app.helpers import ai_helpers
from app.utils import utils
import json
from typing import *
import os
import firebase_admin
from firebase_admin import credentials, auth

# Initialize the Firebase Admin SDK with the downloaded service account key
cred = credentials.Certificate("D:/DdriveCodes/SIH/app/helpers/kisaandvaar-firebase-adminsdk-t83e9-f6d6bf9844.json")
firebase_admin.initialize_app(cred)

async def sign_up_user(sign_up_request: modelType.SignUpRequest):
    try:
        # Create a new user
        user = auth.create_user(
            email=sign_up_request.email,
            password=sign_up_request.password,
        )
        print('Successfully created new user:', user.uid)
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

# Example usage
#new_user = sign_up_user("user@example.com", "strongpassword123")
