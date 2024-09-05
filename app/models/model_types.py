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
    fullname: str
    username: str
    password: constr(min_length=8)
    phonenumber: str = Field(..., pattern=r'^\+91\d{10}$')

class LoginRequest(BaseModel):
    email: str
    password: str

class Profile(BaseModel):
    fullname: str
    password: constr(min_length=8)
    phonenumber: str = Field(..., pattern=r'^\+91\d{10}$')
    address: str
    email: str
    city: str
    pincode:str = Field(..., pattern=r'^\d{6}$')

class CropData(BaseModel):
    cropname: str
    quantity: int
    qualitygrade: str