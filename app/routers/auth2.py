# from firebase_admin import credentials, initialize_app, auth
# from fastapi import UploadFile, File
# import firebase_admin._user_identifier
# import firebase_admin.auth
# import firebase_admin.instance_id
# import app.models.model_types as modelType
# from app.helpers import ai_helpers
# from app.utils import utils
# import json
# from typing import *
# import os
# import firebase_admin
# from fastapi import APIRouter, HTTPException

# # Initialize the Firebase Admin SDK with the downloaded service account key
# cred = credentials.Certificate("D:/DdriveCodes/SIH/app/helpers/kisaandvaar-firebase-adminsdk-t83e9-f6d6bf9844.json")
# initialize_app(cred)

# auth = auth()

# router = APIRouter()

# @router.post("/login")
# async def login(login_request: modelType.LoginRequest):
#     try:
#         user = await auth.get_user_by_email(
#             email=login_request.email,
#             password=login_request.password
#             )

#         return user
    
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Invalid email or password")
    
# @router.post("/sign-up")
# async def sign_up_user(sign_up_request: modelType.SignUpRequest):
#     try:
#         # Create a new user
#         user = auth.create_user(
#             email=sign_up_request.email,
#             password=sign_up_request.password,
#             firstname=sign_up_request.firstname,
#             lastname=sign_up_request.lastname,
#             username=sign_up_request.username,
#             password=sign_up_request.password,
#             phonenumber=sign_up_request.phonenumber
#         )
#         print('Successfully created new user:', user)
#         return user
    
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Example usage
# #new_user = sign_up_user("user@example.com", "strongpassword123")

# @router.post("/build-profile")
# async def build_new_profile(build_profile_request: modelType.ProfileData):
#     try:
#         # Create a new user profile
#         user_profile = auth.UserInfo(
#             occupation = build_profile_request.occupation,
#             address = build_profile_request.address,
#             state = build_profile_request.state,
#             city = build_profile_request.city,
#             pincode = build_profile_request.pincode,
#             profile_image = build_profile_request.profile_image,
#             description = build_profile_request.description
#         )
        
#         print('Successfully created new user profile:', user_profile)
#         user = auth.get_user

        
#         return user_profile
    
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))  
    
    
# def get_active_user_session_info():
#     """User authentication per session is possible from flutter side, TODO"""
#     # Validate user's occupation (ensure they are the owner or an admin)
#     # user = await User.get_current_user()
#     # if user.occupation not in ["owner", "admin"]:
#     #     raise HTTPException(status_code=403, detail="Only owners or admins can update service listings.")
#     # https://firebase.google.com/docs/auth/android/manage-users
    
    