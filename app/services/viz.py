import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

plt.switch_backend('Agg')

def plot_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_bytes = buf.read()
    buf.close()
    return base64.b64encode(img_bytes).decode('utf-8')

def ctr_over_time(df: pd.DataFrame):
    df['Date'] = pd.to_datetime(df['Date'])
    df['CTR'] = df['Clicks'] / df['Impressions']
    df_grouped = df.groupby('Date')['CTR'].mean().reset_index()
    plt.figure(figsize=(8,4))
    plt.plot(df_grouped['Date'], df_grouped['CTR'], marker='o', color='teal')
    plt.title("CTR Over Time")
    plt.xlabel("Date")
    plt.ylabel("CTR")
    plt.grid(True)
    
    return plot_to_base64()

def top_campaigns_by_roas(df: pd.DataFrame):
    avg_sale_value = 500
    df["ROAS"] = (df["Conversions"] * avg_sale_value) / df["Spend"]

    top_df = df.sort_values("ROAS", ascending=False).head(5)

    plt.figure(figsize=(8, 4))
    plt.bar(top_df["CampaignID"], top_df["ROAS"], color='darkorange')
    plt.title("Top 5 Campaigns by ROAS")
    plt.xlabel("Campaign")
    plt.ylabel("ROAS")

    return plot_to_base64()


def conversion_rate_by_audience(df: pd.DataFrame):
    df["ConversionRate"] = df["Conversions"] / df["Clicks"]
    grouped = df.groupby("Audience")["ConversionRate"].mean().sort_values()

    plt.figure(figsize=(8, 4))
    grouped.plot(kind="barh", color="royalblue")
    plt.title("Conversion Rate by Audience")
    plt.xlabel("Conversion Rate")
    plt.ylabel("Audience")

    return plot_to_base64()