from services import viz
from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io

router = APIRouter()

@router.post("/")
async def generate_visuals(file: UploadFile = File(...)):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only Excel files allowed.")

    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to read Excel file.")

    expected_columns = ["CampaignID", "Date", "AdSet", "Audience", "Spend", "Impressions", "Clicks", "Conversions"]
    if not all(col in df.columns for col in expected_columns):
        raise HTTPException(status_code=422, detail=f"Missing columns. Expected: {expected_columns}")
    
    try:
        plots = {
            "ctr_over_time": viz.ctr_over_time(df),
            "top_campaign_roas": viz.top_campaigns_by_roas(df),
            "conversion_rate_by_audience": viz.conversion_rate_by_audience(df)
        }
        return plots
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plot generation failed: {str(e)}")