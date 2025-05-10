import os
from PIL import Image

# Thư mục chứa ảnh gốc và nơi lưu ảnh đã resize
input_dir = 'Dataset'       # Thay bằng thư mục chứa ảnh gốc của bạn
output_dir = 'dataset'         # Thư mục lưu ảnh đã resize
os.makedirs(output_dir, exist_ok=True)

# Kích thước resize
target_size = (224, 400)  # (width, height)

# Lặp qua từng ảnh trong thư mục gốc
for idx, filename in enumerate(sorted(os.listdir(input_dir))):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(input_dir, filename)
        try:
            # Mở và resize ảnh
            img = Image.open(img_path).convert('RGB')
            resized_img = img.resize(target_size)

            # Tạo tên mới và lưu ảnh
            new_filename = f"img_{idx+1:03d}.jpg"
            resized_img.save(os.path.join(output_dir, new_filename))
            print(f"Đã xử lý: {filename} → {new_filename}")
        except Exception as e:
            print(f"Lỗi với file {filename}: {e}")
