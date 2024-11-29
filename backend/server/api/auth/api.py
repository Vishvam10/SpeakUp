from fastapi import Depends, HTTPException, APIRouter, status

from database.adapter import MongoDBAdapter
from database.manager import get_adapter

from api.tags import APITags
from api.auth.model import UserLogin

from utils.auth import create_access_token, verify_password

AuthAPIRouter = APIRouter(prefix="/auth", tags=[APITags.AUTH])


def get_user_mongo_adapter() -> MongoDBAdapter:
    return get_adapter("user")


@AuthAPIRouter.post("/login")
async def login(
    user: UserLogin, db: MongoDBAdapter = Depends(get_user_mongo_adapter)
):
    user_data = db.find_one({"email": user.email})

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(user_id=user_data["user_id"])
    return {"token": f"Bearer {access_token}", "user_id" : user_data["user_id"]}
