from fastapi import APIRouter

from api.tags import APITags

AnalyzeAPIRouter = APIRouter(prefix="/analyze", tags=[APITags.ANALYSIS])

@AnalyzeAPIRouter.post("/analyze")
async def analyze_video(): 
    ...
