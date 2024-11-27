from fastapi import APIRouter

from api.asset.api import AssetAPIRouter
from api.user.api import UserAPIRouter
from api.analyze.api import AnalyzeAPIRouter
from api.auth.api import AuthAPIRouter

MainRouter = APIRouter()

MainRouter.include_router(AssetAPIRouter)
MainRouter.include_router(UserAPIRouter)
MainRouter.include_router(AnalyzeAPIRouter)
MainRouter.include_router(AuthAPIRouter)