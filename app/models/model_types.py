from fastapi import UploadFile
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, constr, Field
from typing import *


class Language(BaseModel):
    language: str

class Query(BaseModel):
    query: str
    
class SignUpRequest(BaseModel):
    email: str
    username: str
    password: constr(min_length=8)
    phonenumber: str = Field(..., pattern=r'^\+91\d{10}$')

class LoginRequest(BaseModel):
    email: str
    password: str

# class Profile(BaseModel):
#     fullname: str
#     password: constr(min_length=8)
#     phonenumber: str = Field(..., pattern=r'^\+91\d{10}$')
#     address: str
#     email: str
#     city: str
#     pincode:str = Field(..., pattern=r'^\d{6}$')
    
class ProfileData(BaseModel):
    def __init__(self, occupation, address, state, city, pincode, profile_image, description):
        self.occupation = occupation
        self.address = address
        self.state = state
        self.city = city
        self.pincode = pincode
        self.profile_image = profile_image
        self.description = description

class CropData(BaseModel):
    cropname: str
    quantity: int
    qualitygrade: str