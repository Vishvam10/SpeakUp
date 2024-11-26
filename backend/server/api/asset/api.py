from fastapi import APIRouter, HTTPException, UploadFile, Depends

from api.tags import APITags

from database.adapter import MongoDBAdapter
from database.manager import get_adapter

AssetAPIRouter = APIRouter(prefix="/asset", tags=[APITags.ASSET])


def get_asset_mongodb_adapter() -> MongoDBAdapter:
    return get_adapter("asset")


@AssetAPIRouter.post("/{user_id}")
async def create_asset(
    user_id: str,
    file: UploadFile,
    db: MongoDBAdapter = Depends(get_asset_mongodb_adapter),
):
    asset_id = db.create(user_id, file)
    if asset_id:
        return {"asset_id": asset_id, "message": "Asset uploaded successfully"}
    raise HTTPException(status_code=500, detail="Failed to upload asset")


@AssetAPIRouter.get("/{user_id}/{asset_id}")
async def get_asset(
    user_id: str,
    asset_id: str,
    db: MongoDBAdapter = Depends(get_asset_mongodb_adapter),
):
    asset = db.get(user_id, asset_id)
    if asset:
        return asset
    raise HTTPException(status_code=404, detail="Asset not found")


@AssetAPIRouter.get("/{user_id}")
async def get_assets(
    user_id: str, db: MongoDBAdapter = Depends(get_asset_mongodb_adapter)
):
    assets = db.get_all(user_id)
    if assets:
        return assets
    raise HTTPException(status_code=404, detail="No assets found for this user")


@AssetAPIRouter.put("/{user_id}/{asset_id}")
async def update_asset(
    user_id: str,
    asset_id: str,
    file: UploadFile,
    db: MongoDBAdapter = Depends(get_asset_mongodb_adapter),
):
    updated = db.update(user_id, asset_id, file)
    if updated:
        return {"message": "Asset updated successfully"}
    raise HTTPException(status_code=404, detail="Asset not found")


@AssetAPIRouter.delete("/{user_id}/{asset_id}")
async def delete_asset(
    user_id: str,
    asset_id: str,
    db: MongoDBAdapter = Depends(get_asset_mongodb_adapter),
):
    deleted = db.delete(user_id, asset_id)
    if deleted:
        return {"message": "Asset deleted successfully"}
    raise HTTPException(status_code=404, detail="Asset not found")
