from fastapi import APIRouter

from api.asset.api import AssetAPIRouter
from api.user.api import UserAPIRouter
from api.analysis.api import AnalysisAPIRouter
from api.auth.api import AuthAPIRouter

MainRouter = APIRouter()

MainRouter.include_router(AssetAPIRouter)
MainRouter.include_router(UserAPIRouter)
MainRouter.include_router(AnalysisAPIRouter)
MainRouter.include_router(AuthAPIRouter)