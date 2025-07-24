import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import json
import os
import base64
import io
import pandas as pd
from PIL import Image, ImageTk
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = os.getenv('API_ENDPOINT')  # e.g. "http://localhost:8000/api/metrics/"

CARD_BG = '#f5f5f5'
TEXT_COLOR = '#333'
TITLE_FONT = ('Helvetica', 16, 'bold')
VALUE_FONT = ('Helvetica', 14)


class AdSmartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 AdSmart - Campaign Analyzer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#ffffff')

        self.title_label = tk.Label(root, text='📈 AdSmart - Campaign Analyzer',
                                    font=('Helvetica', 20, 'bold'), bg='#ffffff', fg='#111')
        self.title_label.pack(pady=10)

        # Tabbed Interface
        self.tab_control = ttk.Notebook(root)
        self.metrics_tab = tk.Frame(self.tab_control, bg="#ffffff")
        self.clustering_tab = tk.Frame(self.tab_control, bg="#ffffff")

        self.tab_control.add(self.metrics_tab, text="📊 Metrics")
        self.tab_control.add(self.clustering_tab, text="📍 Clustering")
        self.tab_control.pack(expand=1, fill="both")

        # --- Metrics Tab ---
        self.metrics_upload_btn = tk.Button(self.metrics_tab, text="Upload Excel for Metrics",
                                            command=self.upload_metrics_file, font=('Helvetica', 12),
                                            bg='#008cff', fg='white')
        self.metrics_upload_btn.pack(pady=10)

        self.metrics_frame = tk.Frame(self.metrics_tab, bg="#ffffff")
        self.metrics_frame.pack(fill="both", expand=True)

        # --- Clustering Tab ---
        self.cluster_upload_btn = tk.Button(self.clustering_tab, text="Upload Excel for Clustering",
                                            command=self.upload_cluster_file, font=('Helvetica', 12),
                                            bg='#28a745', fg='white')
        self.cluster_upload_btn.pack(pady=10)

        self.cluster_table_frame = tk.Frame(self.clustering_tab, bg="#ffffff", relief="solid", bd=1)
        self.cluster_table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cluster_img_label = tk.Label(self.clustering_tab, bg="#ffffff")
        self.cluster_img_label.pack(pady=10)

    def upload_metrics_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                files = {
                    "file": (
                        os.path.basename(file_path),
                        f,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                }
                response = requests.post(API_ENDPOINT, files=files)

            if response.status_code != 200:
                messagebox.showerror("Upload Failed", f"Error: {response.json().get('detail', 'Unknown error')}")
                return

            metrics = response.json()["aggregated_metrics"]
            self.display_metrics(metrics)

            with open(file_path, "rb") as f2:
                files2 = {
                    "file": (
                        os.path.basename(file_path),
                        f2,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                }
                visual_res = requests.post("http://localhost:8000/api/visuals/", files=files2)
                if visual_res.status_code == 200:
                    self.display_charts(visual_res.json())

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def upload_cluster_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                res = requests.post("http://localhost:8000/api/clustering/", files=files)

            if res.status_code != 200:
                messagebox.showerror("Error", f"API Error {res.status_code}: {res.text}")
                return

            data = res.json()
            cluster_data = data["clusters"]
            plot_img_base64 = data["plot"]

            self.display_cluster_table(cluster_data)
            self.display_cluster_image(plot_img_base64)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_metrics(self, metrics):
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()

        row, col = 0, 0
        for key, value in metrics.items():
            card = tk.Frame(self.metrics_frame, bg=CARD_BG, bd=1, relief="groove")
            card.grid(row=row, column=col, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew")

            tk.Label(card, text=key, font=TITLE_FONT, fg=TEXT_COLOR, bg=CARD_BG).pack(pady=5)
            tk.Label(card, text=f"{round(value, 2)}", font=VALUE_FONT, fg="#008cff", bg=CARD_BG).pack()

            col += 1
            if col >= 3:
                row += 1
                col = 0

    def display_charts(self, base64_dict):
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()

        for title, b64img in base64_dict.items():
            decoded_img = base64.b64decode(b64img)
            img = Image.open(io.BytesIO(decoded_img)).resize((500, 300))
            photo = ImageTk.PhotoImage(img)

            frame = tk.Frame(self.metrics_frame, bg='#ffffff', bd=1, relief='solid')
            frame.pack(pady=15)

            tk.Label(frame, text=title.replace("_", " ").title(), font=TITLE_FONT, bg="#ffffff").pack()
            label = tk.Label(frame, image=photo, bg="#ffffff")
            label.image = photo
            label.pack()

    def display_cluster_table(self, data):
        df = pd.DataFrame(data)

        for widget in self.cluster_table_frame.winfo_children():
            widget.destroy()

        cols = list(df.columns)
        tree = ttk.Treeview(self.cluster_table_frame, columns=cols, show="headings")
        tree.pack(fill="both", expand=True)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    def display_cluster_image(self, img_base64):
        img_data = base64.b64decode(img_base64)
        image = Image.open(io.BytesIO(img_data)).resize((600, 400))
        img = ImageTk.PhotoImage(image)

        self.cluster_img_label.config(image=img)
        self.cluster_img_label.image = img


if __name__ == "__main__":
    root = tk.Tk()
    app = AdSmartApp(root)
    root.mainloop()
