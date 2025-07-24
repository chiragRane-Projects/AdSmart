
# 🎯 AdSmart - AI-Powered Marketing Campaign Analyzer

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Tkinter](https://img.shields.io/badge/Tkinter-%23121011.svg?style=for-the-badge)]()
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=numpy)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-006699?style=for-the-badge&logo=matplotlib)](https://matplotlib.org/)
[![scikit-learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)
[![PyInstaller](https://img.shields.io/badge/Packaged%20With-PyInstaller-blue?style=for-the-badge)](https://www.pyinstaller.org/)

---

## 📌 Project Overview

**AdSmart** is a sleek, full GUI-based platform that helps marketers **analyze, cluster, and visualize** their campaign performance using AI. Upload your marketing KPIs in an Excel sheet, and instantly receive segmentation, insights, and visual feedback — no code needed.

> ✅ Built for real-world marketers, agencies, startups, and brands looking to unlock growth using ML.

---

## 🧠 Use Cases

- 📊 Segment marketing campaigns by performance using K-Means clustering.
- 🔍 Visualize CTR, ROAS, conversion rates, and more.
- ⚡ Instantly analyze campaign health from an Excel file.
- 🎯 Make data-backed decisions without needing a data team.

---

## 🧰 Tech Stack

| Layer          | Tools Used                                      |
|----------------|--------------------------------------------------|
| Frontend       | Python Tkinter GUI (Standalone EXE)             |
| Backend        | FastAPI + Uvicorn                               |
| Data Handling  | Pandas, NumPy, Scikit-Learn, Matplotlib         |
| Packaging      | PyInstaller for .exe build                      |

---

## 🚀 How to Use

1. 🧾 Prepare your Excel with columns like:
   ```
   CampaignName | CTR | ROAS | ConversionRate | AdSpend | Impressions ...
   ```

2. 💡 Launch the app by double-clicking the `.exe` or via CLI.

3. 📤 Upload Excel → View insights → Get campaign clusters instantly.

---

## 🛠 How to Run on Your Device

> 🐍 Requires Python 3.10–3.11 (Tkinter-friendly version)

### ⚙️ Step-by-step CLI Setup:

```bash
# Clone the repo
git clone https://github.com/chiragRane-Projects/adsmart-analyzer.git
cd adsmart-analyzer/backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate (Windows)

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn main:app --reload
```

Then in another terminal, run the Tkinter GUI:
```bash
cd frontend
python gui.py
```

---

## 🧪 Sample Input File

> ✅ [Download Sample Excel](./adsmart_clustering_ready.xlsx)

---

## 📂 Project Structure

```
adsmart-analyzer/
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── requirements.txt
├── gui.py
└── sample.xlsx
```

---

## 📦 EXE Setup

Run this inside your virtualenv:
```bash
pyinstaller --onefile --noconsole gui.py
```

Final EXE will be in `/dist` folder.

---

## 📣 Connect

Feel free to fork, open issues, and suggest features!

[🔗 LinkedIn](https://linkedin.com/in/chirag-yourhandle) | [🐙 GitHub](https://github.com/chiragRane-Projects)

---

## 📃 License

MIT © 2025 Chirag
