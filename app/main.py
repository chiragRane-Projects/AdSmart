from fastapi import FastAPI
from routes import upload, analysis, visuals, clustering


app = FastAPI(
    title="AdSmart - AI Marketing Analyzer",
    description="Upload ad campaign CSV and get insights",
    version="0.1.0"
)

app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(analysis.router, prefix="/api/analyze", tags=['Analysis'])
app.include_router(visuals.router, prefix="/api/visuals", tags=['Analytics'])
app.include_router(clustering.router, prefix="/api/clustering", tags=['Clustering'])