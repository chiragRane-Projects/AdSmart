# app/routes/clustering.py

from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import io 
import base64

from routes.analysis import preprocess_excel

router = APIRouter()

@router.post("/")
async def cluster_campaign(file: UploadFile = File(...)):
    df = await preprocess_excel(file)  # ✅ await this properly

    features = ['CTR', 'ROAS', 'ConversionRate', 'Spend']
    df_clean = df[features].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    df_result = df.copy()
    df_result = df_result.iloc[df_clean.index].copy()
    df_result['Cluster'] = clusters

    plt.figure(figsize=(8, 5))
    scatter = plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap='Set1')
    plt.title("Campaign Clusters")
    plt.xlabel(features[0])
    plt.ylabel(features[1])
    plt.colorbar(scatter)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    return {
        "clusters": df_result.to_dict(orient="records"),
        "plot": img_base64
    }
