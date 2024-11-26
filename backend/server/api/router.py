from fastapi import APIRouter

from api.asset.api import AssetAPIRouter
from api.user.api import UserAPIRouter
from api.analyze.api import AnalyzeAPIRouter

MainRouter = APIRouter()

MainRouter.include_router(AssetAPIRouter)
MainRouter.include_router(UserAPIRouter)
MainRouter.include_router(AnalyzeAPIRouter)