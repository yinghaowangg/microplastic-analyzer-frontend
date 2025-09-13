
import os
import shutil
import random

# 原始图像和txt标签文件的路径
source_dir = "path_to_your_300_images"  # 替换为你真实路径

# 输出路径
output_dir = "backend/yolo_data"
train_ratio = 0.8

image_files = [f for f in os.listdir(source_dir) if f.endswith('.jpg') or f.endswith('.png')]
random.shuffle(image_files)

split_idx = int(len(image_files) * train_ratio)
train_images = image_files[:split_idx]
val_images = image_files[split_idx:]

def move_files(file_list, split):
    for img in file_list:
        label = img.replace(".jpg", ".txt").replace(".png", ".txt")
        shutil.copy(os.path.join(source_dir, img), os.path.join(output_dir, "images", split, img))
        shutil.copy(os.path.join(source_dir, label), os.path.join(output_dir, "labels", split, label))

move_files(train_images, "train")
move_files(val_images, "val")