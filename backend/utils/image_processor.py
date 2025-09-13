import os
from ultralytics import YOLO
import cv2

# 模型路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/best.pt")
MODEL_PATH = os.path.abspath(MODEL_PATH)
yolo_model = YOLO(MODEL_PATH)

# 类别字典
idx_to_class = {
    1: "PP",
    2: "PS"
}

def detect_particles(image_path, save_dir="backend/static/results/pred"):
    """
    使用 YOLO 模型检测并分割微塑料
    Args:
        image_path: 上传的图片路径
        save_dir: 保存预测结果的文件夹
    Returns:
        dict: {
            "counts": {类别: 数量},
            "output_image": "results/pred/xxx.png"  # 前端可访问路径
        }
    """
    os.makedirs(save_dir, exist_ok=True)

    # 预测，但不让 YOLO 自动保存
    results = yolo_model(image_path, save=False)

    result = results[0]

    # 输出文件名（用上传图的文件名，避免重复）
    output_filename = os.path.basename(image_path)
    output_path = os.path.join(save_dir, output_filename)

    # 保存结果图（YOLO 可视化）
    cv2.imwrite(output_path, result.plot())

    # 统计类别数量
    counts = {}
    if result.boxes is not None:
        for cls_id in result.boxes.cls.cpu().numpy():
            cls_name = idx_to_class.get(int(cls_id), f"class_{int(cls_id)}")
            counts[cls_name] = counts.get(cls_name, 0) + 1

    return {
        "counts": counts,
        "output_image": f"results/pred/{output_filename}"  # 前端访问路径
    }