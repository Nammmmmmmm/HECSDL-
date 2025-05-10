import cv2
import numpy as np

# Hàm thêm padding vào ảnh và resize về kích thước 244x244
def resize_with_padding(image_path):
    # Đọc ảnh
    img = cv2.imread(image_path)
    h, w, _ = img.shape

    # Tính toán độ lệch giữa chiều dài và chiều rộng
    delta_w = max(0, 400 - w)  # Tính padding chiều rộng
    delta_h = max(0, 400 - h)  # Tính padding chiều cao

    # Padding để chiều dài và chiều rộng đều bằng 400
    top_padding = delta_h // 2
    bottom_padding = delta_h - top_padding
    left_padding = delta_w // 2
    right_padding = delta_w - left_padding

    # Thêm padding vào ảnh (màu đen)
    padded_img = cv2.copyMakeBorder(img, top_padding, bottom_padding, left_padding, right_padding, 
                                    cv2.BORDER_CONSTANT, value=(0, 0, 0))  

    # Resize ảnh về kích thước 244x244
    resized_img = cv2.resize(padded_img, (244, 244))

    return resized_img
