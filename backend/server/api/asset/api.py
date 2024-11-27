import os

from fastapi import APIRouter, HTTPException, UploadFile, Depends, status
from pydantic import BaseModel

from api.tags import APITags
from api.asset.utils import generate_thumbnail_and_extract_audio

from database.adapter import MongoDBAdapter
from database.manager import get_adapter

from globals.getter import get_global_s3_storage

from utils.auth import get_current_user, generate_uuid

AssetAPIRouter = APIRouter(prefix="/asset", tags=[APITags.ASSET])


def get_asset_mongodb_adapter() -> MongoDBAdapter:
    return get_adapter("asset")


class AssetMetadata(BaseModel):
    analysis_params: dict
    metadata: dict


@AssetAPIRouter.post("/{user_id}")
async def create_asset(
    user_id: str,
    file: UploadFile,
    current_user: str = Depends(get_current_user),
    db: MongoDBAdapter = Depends(get_asset_mongodb_adapter),
):
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access"
        )

    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File not uploaded"
        )

    file_name, _ = os.path.splitext(file.filename)

    assets = db.find_all({"user_id": user_id})
    asset_present = False

    for asset in assets:
        s3_video_file_name = asset["s3_video_file_name"]
        if file.filename in s3_video_file_name:
            asset_present = True
            break

    if asset_present:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Asset already present",
        )

    try:
        s3_video_file_name = f"{user_id}/{file.filename}"
        s3_audio_file_name = f"{user_id}/{file_name}.mp3"

        s3_storage = get_global_s3_storage()

        (
            thumbnail_url,
            audio_buffer,
        ) = await generate_thumbnail_and_extract_audio(file.file)

        # Moving the cursor back to the beginning since during the audi
        # extraction part, the cursor would have moved to the end.

        file.file.seek(0)

        s3_storage.upload_fileobj(s3_video_file_name, file.file)
        s3_storage.upload_fileobj(s3_audio_file_name, audio_buffer)

        # Not storing the public URL since that would be
        # refreshed anyway, we will get that when requested)

        asset_data = {
            "asset_id": generate_uuid(),
            "user_id": user_id,
            "s3_video_file_name": s3_video_file_name,
            "s3_audio_file_name": s3_audio_file_name,
            "thumbnail": thumbnail_url,
        }

        db.insert_one(asset_data)

        return {
            "asset_id": asset_data["asset_id"],
            "message": "Asset uploaded successfully",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@AssetAPIRouter.get("/{user_id}/{asset_id}")
async def get_asset(
    user_id: str,
    asset_id: str,
    current_user: str = Depends(get_current_user),
    db: MongoDBAdapter = Depends(get_asset_mongodb_adapter),
):
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access"
        )

    asset = db.find_one({"user_id": user_id, "asset_id": asset_id})

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found"
        )

    s3_video_file_name = asset.get("s3_video_file_name")
    s3_audio_file_name = asset.get("s3_audio_file_name")

    s3_storage = get_global_s3_storage()

    audio_src_url = s3_storage.get_url(s3_audio_file_name)
    video_src_url = s3_storage.get_url(s3_video_file_name)

    asset["audio_src_url"] = audio_src_url
    asset["video_src_url"] = video_src_url

    return asset


@AssetAPIRouter.get("/{user_id}")
async def get_all_assets(
    user_id: str,
    current_user: str = Depends(get_current_user),
    db: MongoDBAdapter = Depends(get_asset_mongodb_adapter),
):
    try:
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access",
            )

        assets = db.find_all({"user_id": user_id})
        return assets if assets else []
    except Exception as e:
        print("Failed to get all assets : ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


@AssetAPIRouter.delete("/{user_id}")
async def delete_all_assets(
    user_id: str,
    current_user: str = Depends(get_current_user),
    db: MongoDBAdapter = Depends(get_asset_mongodb_adapter),
):
    try:
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access",
            )

        assets = db.find_all({"user_id": user_id})

        if not assets:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No assets found"
            )

        deleted = db.delete({"user_id": user_id})

        s3_storage = get_global_s3_storage()
        s3_storage.connect()

        for asset in assets:
            s3_video_file_name = asset["s3_video_file_name"]
            s3_audio_file_name = asset["s3_audio_file_name"]

            try:
                s3_storage.delete_object(s3_video_file_name)
                s3_storage.delete_object(s3_audio_file_name)
                print(
                    f"Deleted {s3_video_file_name} and {s3_audio_file_name} from S3."
                )
            except Exception as e:
                print(
                    f"Error deleting {s3_video_file_name} and {s3_audio_file_name} : {e}"
                )

        if deleted:
            return {"message": "Assets deleted successfully"}

    except Exception as e:
        print("Failed to delete assets : ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


@AssetAPIRouter.delete("/{user_id}/{asset_id}")
async def delete_asset(
    user_id: str,
    asset_id: str,
    current_user: str = Depends(get_current_user),
    db: MongoDBAdapter = Depends(get_asset_mongodb_adapter),
):
    try:
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access",
            )

        s3_storage = get_global_s3_storage()
        s3_storage.connect()

        asset = db.find_one({"user_id": user_id, "asset_id": asset_id})

        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found"
            )

        deleted = db.delete({"user_id": user_id, "asset_id": asset_id})

        # Delete associated files from S3
        s3_video_file_name = asset["s3_video_file_name"]
        s3_audio_file_name = asset["s3_audio_file_name"]

        try:
            s3_storage.delete_object(s3_video_file_name)
            s3_storage.delete_object(s3_audio_file_name)
            print(
                f"Deleted {s3_video_file_name} and {s3_audio_file_name} from S3."
            )
        except Exception as e:
            print(
                f"Error deleting {s3_video_file_name} and {s3_audio_file_name} : {e}"
            )

        if deleted:
            return {"message": "Asset deleted successfully"}

    except Exception as e:
        print("Failed to delete asset: ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )
