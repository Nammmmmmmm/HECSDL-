import os
import cv2
import numpy as np
import tensorflow as tf
import pyodbc
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from image_processing import resize_with_padding
import matplotlib.pyplot as plt

# --- Cấu hình SQL Server ---
server = r'LAPTOP-8L0VDRJ8\KIET'
database = 'HCSDL'
username = 'sa'
password = '123456'
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# --- Load model MobileNetV2 ---
model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# --- Thư mục chứa ảnh gốc ---
IMAGE_FOLDER = 'dataset/'

# --- Hàm trích vector đặc trưng ---
def extract_features(img):
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    features = model.predict(img)[0]
    return features

# --- Hàm tính cosine similarity ---
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# --- Hàm tìm 3 ảnh giống nhất ---
def find_top3_similar(new_image_path):
    raw_img = resize_with_padding(new_image_path)
    features_new = extract_features(raw_img)

    cursor.execute("SELECT filename, feature_vector FROM Images")
    results = cursor.fetchall()

    similarities = []
    for filename, vector_str in results:
        vector_db = np.array(list(map(float, vector_str.split(','))))
        sim = cosine_similarity(features_new, vector_db)
        similarities.append((filename, sim))

    top3 = sorted(similarities, key=lambda x: x[1], reverse=True)[:3]
    return top3

# --- Hiển thị ảnh tương tự ---
def show_top3_images(top3):
    fig, axes = plt.subplots(1, 3, figsize=(12, 5))
    for i, (filename, score) in enumerate(top3):
        path = os.path.join(IMAGE_FOLDER, filename)
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        axes[i].imshow(img)
        axes[i].set_title(f"{filename}\nSimilarity: {score:.4f}")
        axes[i].axis('off')
    plt.tight_layout()
    plt.show()

# --- Hàm xử lý khi kéo-thả ảnh ---
def handle_drop(event):
    filepath = event.data.strip('{').strip('}')
    if os.path.isfile(filepath):
        print(f"Đã nhận ảnh: {filepath}")
        top3 = find_top3_similar(filepath)
        for f, s in top3:
            print(f"{f} - similarity: {s:.4f}")
        show_top3_images(top3)

# --- Giao diện ---
root = TkinterDnD.Tk()
root.title("Kéo-thả ảnh để tìm tương tự")
root.geometry("400x200")

label = tk.Label(root, text="Kéo và thả ảnh vào đây", font=("Arial", 16), bg="lightgray")
label.pack(expand=True, fill="both", padx=10, pady=10)

label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', handle_drop)

root.mainloop()
