import os
import cv2
import numpy as np
import tensorflow as tf
import pyodbc

# --- Cấu hình kết nối SQL Server ---
server = r'LAPTOP-8L0VDRJ8\KIET'
database = 'HCSDL'
username = 'sa'
password = '123456'
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# --- Tải mô hình MobileNetV2 ---
model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# --- Hàm resize ảnh: padding ảnh 244x400 -> 400x400 -> resize 244x244 ---
def resize_with_padding(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Không thể đọc ảnh: {image_path}")
    h, w, _ = img.shape

    delta_w = max(0, 400 - w)
    delta_h = max(0, 400 - h)
    top_padding = delta_h // 2
    bottom_padding = delta_h - top_padding
    left_padding = delta_w // 2
    right_padding = delta_w - left_padding

    padded_img = cv2.copyMakeBorder(img, top_padding, bottom_padding, left_padding, right_padding,
                                    cv2.BORDER_CONSTANT, value=(0, 0, 0))
    resized_img = cv2.resize(padded_img, (244, 244))
    return resized_img

# --- Hàm trích xuất đặc trưng từ ảnh ---
def extract_features(image_path):
    processed_img = resize_with_padding(image_path)
    input_tensor = tf.keras.applications.mobilenet_v2.preprocess_input(processed_img)
    input_tensor = np.expand_dims(input_tensor, axis=0)
    features = model.predict(input_tensor, verbose=0)[0]
    return features

# --- Thư mục chứa ảnh ---
IMAGE_FOLDER = 'dataset/'

# --- Duyệt ảnh và insert vào SQL ---
for filename in os.listdir(IMAGE_FOLDER):
    if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
        image_path = os.path.join(IMAGE_FOLDER, filename)
        try:
            features = extract_features(image_path)
            feature_str = ','.join(map(str, features.tolist()))
            cursor.execute("INSERT INTO Images (filename, feature_vector) VALUES (?, ?)", filename, feature_str)
            print(f"✔ Đã chèn: {filename}")
            conn.commit()
        except Exception as e:
            print(f"❌ Lỗi với ảnh {filename}: {e}")

conn.close()
print("✅ Hoàn tất chèn toàn bộ ảnh.")
