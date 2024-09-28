from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from database import Session, engine
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from dependencies import create_access_token, create_refresh_token, check_access_token_validation, check_refresh_token_validation

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session = Session(bind=engine)

@auth_router.get('/')
async def hello(access_token: check_access_token_validation=Depends()):
    return {"message": "Hello World"}

@auth_router.post('/signup', response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with the email already exists'
            )
    
    db_username = session.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with the username already exists'
            )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)

    session.commit()
    
    return new_user

@auth_router.post('/login', status_code=200)
async def login(user: LoginModel):
    db_user = session.query(User).filter(User.username==user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        # access_token = Authorize.create_access_token(subject=db_user.username)
        # refresh_token = Authorize.create_refresh_token(subject=db_user.username)
        access_token = create_access_token(data={'sub': db_user.username})
        refresh_token = create_refresh_token(data={'sub': db_user.username})

        response = {
            'access': access_token,
            'refresh': refresh_token
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Username or Password')

@auth_router.post('/refresh', status_code=200)
async def refresh_token(refresh_token: check_refresh_token_validation=Depends()):
    return {
        'access': refresh_token
    }