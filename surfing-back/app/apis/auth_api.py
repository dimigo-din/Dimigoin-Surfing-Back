# surfing-back/app/apis/auth_api.py

from typing import Dict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas import base_schema, auth_schema
from app.utils import jwt, dimi_api
from app.cruds import auth_crud
from app.models.user_model import UserInterface
from app.models.refresh_token_model import RefreshTokenInterface
from app.database import get_db
from app import setting

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    )

@router.post("/login", responses={
    200: {"model": auth_schema.TokenResponse},
    400: {"model": base_schema.GeneralErrorResponse}
})
def login(
    user_login_data: auth_schema.LoginRequest,
    db: Session = Depends(get_db),
):
    login_result = dimi_api.login(user_login_data.username, user_login_data.password)
    if isinstance(login_result, str):
        return JSONResponse(status_code=400, content=base_schema.GeneralErrorResponse(error=login_result).to_json_str())
    user_id = login_result.user_id
    user_email = login_result.email
    user: UserInterface | None = auth_crud.get_user_by_id(db, user_id)
    if user is None:
        auth_crud.create_user(db, user_id, user_email)
        user_role = "STUDENT"
    else:
        user_role = user.role
        
    new_access_token = jwt.surfingJWT.encode_token(user_id, user_role)
    new_refresh_token = auth_crud.create_refresh_token(db, user_id)

    return auth_schema.TokenResponse(
        access_token=new_access_token,
        expire_in=setting.JWT_EXPIRE,
        refresh_token=new_refresh_token
    )

@router.get("/refresh", responses={
    200: {"model": auth_schema.AccessTokenResponse},
    404: {"model": auth_schema.UserNotFound}
})
def refresh(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    refresh_token_result = auth_crud.get_user_info_by_refresh_token(db, refresh_token)
    
    if refresh_token_result == None:
        return JSONResponse(status_code=404, content=auth_schema.UserNotFound(error="User Not Found").to_json_str())
    new_access_token = jwt.surfingJWT.encode_token(refresh_token_result.user_id, refresh_token_result.role)
    return auth_schema.AccessTokenResponse(
        access_token=new_access_token,
        expire_in=setting.JWT_EXPIRE
    )

@router.get("/logout", responses={
    200: {"model": base_schema.GeneralSuccessResponse},
    404: {"model": auth_schema.UserNotFound}
})
def logout(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    refresh_token_result: bool = auth_crud.delete_refresh_token(db, refresh_token)
    if not refresh_token_result:
        return JSONResponse(status_code=404, content=auth_schema.UserNotFound(error="User Not Found").to_json_str())
    return base_schema.GeneralSuccessResponse(message="Logout Success")

    
    
