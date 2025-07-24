from fastapi import APIRouter, File, UploadFile, HTTPException
import pandas as pd
import io

router = APIRouter()

@router.post("/")
async def upload_campaign_excel(file: UploadFile = File(...)):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed")
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read excel file: {str(e)}")
    
    expected_columns = ["CampaignID", "Date", "AdSet", "Audience", "Spend", "Impressions", "Clicks", "Conversions"]
    
    if not all(col in df.columns for col in expected_columns):
        raise HTTPException(status_code=422, detail=f"Missing columns. Expected: {expected_columns}")
    
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "shape": df.head(5).to_dict(orient="records")
    }