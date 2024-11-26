from fastapi import APIRouter, HTTPException, Depends

from api.tags import APITags
from api.user.pydantic_model import UserCreate, UserUpdate

from database.adapter import MongoDBAdapter
from database.manager import get_adapter

UserAPIRouter = APIRouter(prefix="/user", tags=[APITags.USER])


def get_user_mongo_adapter() -> MongoDBAdapter:
    return get_adapter("user")


@UserAPIRouter.post("/")
async def create_user(
    user: UserCreate, db: MongoDBAdapter = Depends(get_user_mongo_adapter)
):
    user_id = db.create(user.model_dump())
    return {"user_id": user_id, "message": "User created successfully"}


@UserAPIRouter.get("/{user_id}")
async def get_user(
    user_id: str, db: MongoDBAdapter = Depends(get_user_mongo_adapter)
):
    user = db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@UserAPIRouter.put("/{user_id}")
async def update_user(
    user_id: str,
    user: UserUpdate,
    db: MongoDBAdapter = Depends(get_user_mongo_adapter),
):
    updated_user = db.update(user_id, user.model_dump())
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}


@UserAPIRouter.delete("/{user_id}")
async def delete_user(
    user_id: str, db: MongoDBAdapter = Depends(get_user_mongo_adapter)
):
    deleted = db.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
