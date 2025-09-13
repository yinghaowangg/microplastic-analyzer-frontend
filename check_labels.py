from pathlib import Path
from collections import Counter

# 修改这里为你的数据路径
train_label_dir = Path("backend/train/yolo_dataset/labels/train")
val_label_dir   = Path("backend/train/yolo_dataset/labels/val")

def count_classes(label_dir):
    counter = Counter()
    if not label_dir.exists():
        print(f"❌ 路径不存在: {label_dir}")
        return counter

    for txt_file in label_dir.glob("*.txt"):
        with open(txt_file, "r") as f:
            for line in f:
                cls_id = line.strip().split()[0]
                if cls_id.isdigit():
                    counter[int(cls_id)] += 1
    return counter

# 统计
print("📊 训练集类别统计：")
train_counter = count_classes(train_label_dir)
for cls_id, count in sorted(train_counter.items()):
    print(f"类 {cls_id}: {count} 个实例")

print("\n📊 验证集类别统计：")
val_counter = count_classes(val_label_dir)
for cls_id, count in sorted(val_counter.items()):
    print(f"类 {cls_id}: {count} 个实例")