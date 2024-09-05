from fastapi import APIRouter, HTTPException, Depends
import app.models.model_types as modelType
from fastapi.security import HTTPBearer

router = APIRouter()

oauth2_scheme = HTTPBearer()

@router.post("/select-language")
async def selected_language(language:modelType.Language):
    try:
        # response = await auth.sign_up_user(
        #     email=sign_up_request.email,
        #     password=sign_up_request.password,
        # )
        return {
            "status": "success",
            "message": "Language has been succesfully set accoding to user",
            "data": language
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sign-up")
async def sign_up(sign_up_request: modelType.SignUpRequest):
    try:
        # response = await auth.sign_up_user(
        #     email=sign_up_request.email,
        #     password=sign_up_request.password,
        # )
        return {
            "status": "success",
            "message": "User signed up successfully. Please check your email to confirm your account.",
            "data": "response"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login_user(login_request: modelType.LoginRequest):
    # auth_result = auth.authenticate_user(login_request.email, login_request.password)
    # login_id = auth.extract_sub_from_token(auth_result['AccessToken'])
    return {
        "status": True,
        "message": "Login successful",
        "access_token": "auth_result",
        "login_id": "login_id" 
    }


@router.post("/set-profile")
async def login_user(profile: modelType.Profile):
    # auth_result = auth.authenticate_user(login_request.email, login_request.password)
    # login_id = auth.extract_sub_from_token(auth_result['AccessToken'])
    return {
        "status": True,
        "message": "Profile Set",
        "data": profile 
    }