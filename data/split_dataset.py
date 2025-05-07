import os
import random
import shutil
from pathlib import Path

# 使用相对路径
DATASET_DIR = Path('.')  # 当前目录，即data文件夹
IMAGES_DIR = DATASET_DIR / 'images'
LABELS_DIR = DATASET_DIR / 'labels'
TRAIN_RATIO = 0.8  # 训练集比例

def main():
    print("开始处理数据集...")
    
    # 确保目标目录存在
    os.makedirs(IMAGES_DIR / 'train', exist_ok=True)
    os.makedirs(IMAGES_DIR / 'val', exist_ok=True)
    os.makedirs(LABELS_DIR / 'train', exist_ok=True)
    os.makedirs(LABELS_DIR / 'val', exist_ok=True)
    
    # 获取所有图像文件
    if not os.path.exists(IMAGES_DIR):
        print(f"错误: 图像目录不存在: {IMAGES_DIR}")
        return
    
    if not os.path.exists(LABELS_DIR):
        print(f"错误: 标签目录不存在: {LABELS_DIR}")
        return
    
    image_files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and os.path.isfile(os.path.join(IMAGES_DIR, f))]
    
    if not image_files:
        print(f"错误: 在目录 {IMAGES_DIR} 中未找到图像文件")
        return
    
    # 随机打乱图像文件顺序
    random.shuffle(image_files)
    
    # 计算训练集数量
    train_count = int(len(image_files) * TRAIN_RATIO)
    
    # 划分训练集和验证集
    train_images = image_files[:train_count]
    val_images = image_files[train_count:]
    
    print(f"总图像数: {len(image_files)}")
    print(f"训练集图像数: {len(train_images)} ({TRAIN_RATIO*100:.0f}%)")
    print(f"验证集图像数: {len(val_images)} ({(1-TRAIN_RATIO)*100:.0f}%)")
    
    # 记录处理的文件数和丢失的标签数
    processed_train_images = 0
    processed_train_labels = 0
    processed_val_images = 0
    processed_val_labels = 0
    missing_labels = []
    
    # 移动训练集图像和标签
    for img_file in train_images:
        # 处理图像
        src_img = os.path.join(IMAGES_DIR, img_file)
        dst_img = os.path.join(IMAGES_DIR, 'train', img_file)
        try:
            shutil.copy2(src_img, dst_img)
            processed_train_images += 1
        except Exception as e:
            print(f"复制图像文件时出错 {src_img}: {e}")
            continue
        
        # 处理对应的标签（如果存在）
        label_file = os.path.splitext(img_file)[0] + '.txt'
        src_label = os.path.join(LABELS_DIR, label_file)
        if os.path.exists(src_label):
            dst_label = os.path.join(LABELS_DIR, 'train', label_file)
            try:
                shutil.copy2(src_label, dst_label)
                processed_train_labels += 1
            except Exception as e:
                print(f"复制标签文件时出错 {src_label}: {e}")
        else:
            missing_labels.append(label_file)
    
    # 移动验证集图像和标签
    for img_file in val_images:
        # 处理图像
        src_img = os.path.join(IMAGES_DIR, img_file)
        dst_img = os.path.join(IMAGES_DIR, 'val', img_file)
        try:
            shutil.copy2(src_img, dst_img)
            processed_val_images += 1
        except Exception as e:
            print(f"复制图像文件时出错 {src_img}: {e}")
            continue
        
        # 处理对应的标签（如果存在）
        label_file = os.path.splitext(img_file)[0] + '.txt'
        src_label = os.path.join(LABELS_DIR, label_file)
        if os.path.exists(src_label):
            dst_label = os.path.join(LABELS_DIR, 'val', label_file)
            try:
                shutil.copy2(src_label, dst_label)
                processed_val_labels += 1
            except Exception as e:
                print(f"复制标签文件时出错 {src_label}: {e}")
        else:
            missing_labels.append(label_file)
    
    # 输出处理结果
    print("\n数据集处理完成!")
    print(f"处理结果:")
    print(f"- 训练集: {processed_train_images}张图像, {processed_train_labels}个标签")
    print(f"- 验证集: {processed_val_images}张图像, {processed_val_labels}个标签")
    
    if missing_labels:
        print(f"\n警告: {len(missing_labels)}个图像缺少对应的标签文件")
        if len(missing_labels) <= 10:
            for label in missing_labels:
                print(f"  - 缺失: {label}")
        else:
            print(f"  - 缺失标签过多，仅显示前10个: {missing_labels[:10]}")
    
    # 创建或更新data.yaml
    try:
        yaml_path = DATASET_DIR / 'data.yaml'
        if os.path.exists(yaml_path):
            print("\n检测到已有data.yaml文件，将更新train和val路径")
            with open(yaml_path, 'r', encoding='utf-8') as f:
                yaml_content = f.readlines()
            
            # 更新yaml文件中的train和val路径
            updated_yaml = []
            for line in yaml_content:
                if line.strip().startswith('train:'):
                    updated_yaml.append('train: images/train  # train images\n')
                elif line.strip().startswith('val:'):
                    updated_yaml.append('val: images/val  # val images\n')
                else:
                    updated_yaml.append(line)
            
            with open(yaml_path, 'w', encoding='utf-8') as f:
                f.writelines(updated_yaml)
        else:
            print("\n未检测到data.yaml文件，将创建基本配置文件")
            # 获取类别信息
            classes_file = LABELS_DIR / 'classes.txt'
            classes = []
            if os.path.exists(classes_file):
                with open(classes_file, 'r', encoding='utf-8') as f:
                    classes = [line.strip() for line in f.readlines() if line.strip()]
            
            # 创建yaml文件
            with open(yaml_path, 'w', encoding='utf-8') as f:
                f.write(f"path: ./  # 数据集根目录\n")
                f.write(f"train: images/train  # 训练集图像\n")
                f.write(f"val: images/val  # 验证集图像\n")
                f.write(f"nc: {len(classes)}  # 类别数量\n")
                f.write(f"names: {classes}  # 类别名称\n")
        
        print("data.yaml文件已更新")
    except Exception as e:
        print(f"更新data.yaml文件时出错: {e}")

if __name__ == "__main__":
    main() 