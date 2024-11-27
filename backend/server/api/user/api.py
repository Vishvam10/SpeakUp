from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, status

from api.tags import APITags
from api.user.pydantic_model import UserCreate, UserUpdate, UserResponse

from database.adapter import MongoDBAdapter
from database.manager import get_adapter

from utils.hash import hash_password, generate_uuid, verify_password

UserAPIRouter = APIRouter(prefix="/user", tags=[APITags.USER])


def get_user_mongo_adapter() -> MongoDBAdapter:
    return get_adapter("user")


@UserAPIRouter.get("/all")
async def get_all_users(db: MongoDBAdapter = Depends(get_user_mongo_adapter)):
    users = db.find_all(filter={}, query={})
    if not users:
        return []
    return users


@UserAPIRouter.post("/")
async def create_user(
    user: UserCreate, db: MongoDBAdapter = Depends(get_user_mongo_adapter)
):
    if not user.email or "@" not in user.email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    if len(user.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long",
        )

    existing_user = db.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    hashed_password = hash_password(user.password)
    user_data = user.model_dump()

    now = datetime.now(timezone.utc)

    user_data["user_id"] = generate_uuid()
    user_data["password"] = hashed_password
    user_data["created_at"] = now
    user_data["updated_at"] = now
    user_data["deleted_at"] = None

    db.create(user_data)

    return {"status": status.HTTP_201_CREATED, "user_id": user_data["user_id"]}


@UserAPIRouter.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str, db: MongoDBAdapter = Depends(get_user_mongo_adapter)
):
    user = db.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    return user


@UserAPIRouter.put("/{user_id}")
async def update_user(
    user_id: str,
    user: UserUpdate,
    db: MongoDBAdapter = Depends(get_user_mongo_adapter),
):
    existing_user = db.find_one({"user_id": user_id})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    if user.password:
        if not user.old_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is required to update the password",
            )

        if (user.old_password != user.password) and (
            not verify_password(existing_user["password"], user.old_password)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password does not match",
            )

        user.password = hash_password(user.password)

    updated_user = db.update(
        filter={"user_id": user_id}, data=user.model_dump(exclude_unset=True)
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    return {
        "status": status.HTTP_200_OK,
        "message": "User updated successfully",
    }


@UserAPIRouter.delete("/{user_id}")
async def delete_user(
    user_id: str, db: MongoDBAdapter = Depends(get_user_mongo_adapter)
):
    deleted = db.delete({"user_id": user_id})
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "status": status.HTTP_200_OK,
        "message": "User deleted successfully",
    }
