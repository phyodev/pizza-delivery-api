from pydantic import BaseModel, Field
from typing import Optional

class SignUpModel(BaseModel):
    # id: Optional[int] = None
    username:str = Field(..., example="JohnDoe")
    email:str = Field(..., example="johndoe@gmail.com")
    password:str = Field(..., example="P@ssword001")
    is_staff:Optional[bool] = Field(..., example=False)
    is_active:Optional[bool] = Field(..., example=True)

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'JohnDoe',
                'email': 'johndoe@gmail.com',
                'password': 'P@ssword001',
                'is_staff': False,
                'is_active': True
            }
        }

# class Settings(BaseModel):
#     authjwt_secret_key:str='cc1682ef712d2dc4ea9ae5def7be5b36c40423161f068468aa9beab6a760047b'

class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    # id: Optional[int] = None
    quantity:int = Field(..., example=2)
    # order_status: Optional[str] = 'PENDING'
    pizza_size: Optional[str] = Field(..., example="SMALL")
    # user_id: Optional[int] = None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'quantity': 2,
                'pizza_size': 'SMALL'
            }
        }

class OrderStatusModel(BaseModel):
    order_status: Optional[str] = 'PENDING'

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'order_status': 'PENDING'
            }
        }