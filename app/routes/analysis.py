from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io

router = APIRouter()

async def preprocess_excel(file: UploadFile) -> pd.DataFrame:
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed")
    
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read Excel file:{str(e)}")
    
    expected_columns = ["CampaignID", "Date", "AdSet", "Audience", "Spend", "Impressions", "Clicks", "Conversions"]
    if not all(col in df.columns for col in expected_columns):
        raise HTTPException(status_code=422, detail=f"Missing columns. Expected: {expected_columns}")
    
    df.fillna(0, inplace=True)
    df = df.astype({"Spend": float, "Impressions":float, "Clicks": float, "Conversions": float})
    
    avg_sale_value = 500
    
    df['CTR'] = df['Clicks'] / df['Impressions']
    df['CPC'] = df['Spend'] / df['Clicks']
    df['ROAS'] = (df['Conversions'] * avg_sale_value) / df['Spend']
    df["ConversionRate"] = df["Conversions"] / df["Clicks"]
    
    df[["CTR", "CPC", "ROAS", "ConversionRate"]] = df[["CTR", "CPC", "ROAS", "ConversionRate"]].round(2)
    return df

@router.post("/")
async def analyze_campaign_excel(file: UploadFile = File(...)):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed")
    
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read Excel file:{str(e)}")
    
    expected_columns = ["CampaignID", "Date", "AdSet", "Audience", "Spend", "Impressions", "Clicks", "Conversions"]
    if not all(col in df.columns for col in expected_columns):
        raise HTTPException(status_code=422, detail=f"Missing columns. Expected: {expected_columns}")
    
    df.fillna(0, inplace=True)
    df = df.astype({"Spend": float, "Impressions":float, "Clicks": float, "Conversions": float})
    
    avg_sale_value = 500
    
    df['CTR'] = df['Clicks'] / df['Impressions']
    df['CPC'] = df['Spend'] / df['Clicks']
    df['ROAS'] = (df['Conversions'] * avg_sale_value) / df['Spend']
    df["ConversionRate"] = df["Conversions"] / df["Clicks"]
    
    df[["CTR", "CPC", "ROAS", "ConversionRate"]] = df[["CTR", "CPC", "ROAS", "ConversionRate"]].round(2)
    
    return {
        "campaigns": df.shape[0],
        "aggregated_metrics": {
            "Total Spend": df["Spend"].sum(),
            "Total Impressions": df["Impressions"].sum(),
            "Total Clicks": df["Clicks"].sum(),
            "Total Conversions": df["Conversions"].sum(),
            "Average CTR": round(df["CTR"].mean(), 2),
            "Average CPC": round(df["CPC"].mean(), 2),
            "Average ROAS": round(df["ROAS"].mean(), 2),
            "Average Conversion Rate": round(df["ConversionRate"].mean(), 2)
        },
        "campaign_data": df.to_dict(orient="records")
    }