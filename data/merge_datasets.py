import os
import shutil
from pathlib import Path

# 使用绝对路径
PROJECT_ROOT = Path('D:/MyProject/LocalRepository/YOLO/Intelligent_star_car')
CURRENT_DIR = PROJECT_ROOT / 'data'  # 当前目录，即data文件夹

# 源数据集路径（使用绝对路径）
DATASET1_PATH = PROJECT_ROOT / 'dataLei'
DATASET2_PATH = PROJECT_ROOT / 'photo'

# 目标数据集路径
TARGET_PATH = PROJECT_ROOT / 'data'
TARGET_IMAGES = TARGET_PATH / 'images'
TARGET_LABELS = TARGET_PATH / 'labels'

# 创建必要的目录
os.makedirs(TARGET_IMAGES, exist_ok=True)
os.makedirs(TARGET_LABELS, exist_ok=True)

def read_classes(file_path):
    """读取classes.txt文件内容"""
    classes = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            classes = [line.strip() for line in f.readlines() if line.strip()]
        print(f"成功读取类别文件: {file_path}")
    except Exception as e:
        print(f"读取类别文件时出错: {e}")
        # 如果读取失败，尝试创建一个空的类别文件
        if not classes:
            print(f"为路径 {file_path} 创建默认类别列表")
            if "dataLei" in str(file_path):
                classes = ['Nezha', 'Nezha2', 'Red', 'Red_Yellow']
            elif "photo" in str(file_path):
                classes = ['Aobing', 'Nezha', 'Red', 'Red_Yellow', 'Green', 'Yellow']
    return classes

def merge_classes():
    """合并两个数据集的类别文件"""
    # 读取两个数据集的类别
    dataLei_classes_path = DATASET1_PATH / 'labels' / 'classes.txt'
    photo_classes_path = DATASET2_PATH / 'lables' / 'classes.txt'
    
    # 检查classes.txt文件是否存在，如果不存在，尝试其他可能的位置
    if not os.path.exists(dataLei_classes_path):
        alt_path = DATASET1_PATH / 'labels' / 'classes.txt'
        if os.path.exists(alt_path):
            dataLei_classes_path = alt_path
        else:
            print(f"找不到数据集1的classes.txt文件，将使用默认类别")
    
    if not os.path.exists(photo_classes_path):
        alt_path = DATASET2_PATH / 'labels' / 'classes.txt'
        if os.path.exists(alt_path):
            photo_classes_path = alt_path
        else:
            print(f"找不到数据集2的classes.txt文件，将使用默认类别")
    
    classes1 = read_classes(dataLei_classes_path)
    classes2 = read_classes(photo_classes_path)
    
    print(f"数据集1类别: {classes1}")
    print(f"数据集2类别: {classes2}")
    
    # 合并类别（去重）
    merged_classes = list(dict.fromkeys(classes1 + classes2))
    print(f"合并后的类别: {merged_classes}")
    
    # 创建类别ID映射关系（用于重新映射标签文件）
    mapping1 = {cls: merged_classes.index(cls) for cls in classes1}
    mapping2 = {cls: merged_classes.index(cls) for cls in classes2}
    
    # 保存合并后的classes.txt
    with open(TARGET_LABELS / 'classes.txt', 'w', encoding='utf-8') as f:
        for cls in merged_classes:
            f.write(f"{cls}\n")
    
    return merged_classes, mapping1, mapping2

def remap_label_file(src_file, dst_file, mapping, original_classes):
    """重新映射标签文件中的类别ID"""
    try:
        with open(src_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if parts and len(parts) >= 5:  # YOLO格式: class_id x y width height
                try:
                    class_id = int(parts[0])
                    if class_id < len(original_classes):
                        # 获取原始类别名
                        class_name = original_classes[class_id]
                        # 获取新的类别ID
                        new_class_id = mapping[class_name]
                        # 替换类别ID
                        parts[0] = str(new_class_id)
                        new_lines.append(' '.join(parts) + '\n')
                    else:
                        # 如果类别ID超出范围，保持原样
                        new_lines.append(line)
                except ValueError:
                    # 如果无法解析类别ID，保持原样
                    new_lines.append(line)
            else:
                # 不符合YOLO格式的行，保持原样
                new_lines.append(line)
        
        with open(dst_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    except Exception as e:
        print(f"重新映射标签文件时出错 {src_file}: {e}")
        # 如果出错，复制原始文件
        shutil.copy2(src_file, dst_file)

def copy_files(src_images, src_labels, label_mapping=None, original_classes=None):
    """复制图像和标签文件到目标目录"""
    # 检查目录是否存在
    if not os.path.exists(src_images):
        print(f"警告: 图像目录不存在: {src_images}")
        return
    
    if not os.path.exists(src_labels):
        print(f"警告: 标签目录不存在: {src_labels}")
        return
    
    # 复制图像文件
    for img_file in os.listdir(src_images):
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            src_img = os.path.join(src_images, img_file)
            dst_img = os.path.join(TARGET_IMAGES, img_file)
            if os.path.isfile(src_img):
                shutil.copy2(src_img, dst_img)
                print(f"复制图像: {img_file}")
    
    # 复制并重新映射标签文件
    for label_file in os.listdir(src_labels):
        if label_file.lower().endswith('.txt') and label_file != 'classes.txt':
            src_label = os.path.join(src_labels, label_file)
            dst_label = os.path.join(TARGET_LABELS, label_file)
            if os.path.isfile(src_label):
                if label_mapping and original_classes:
                    # 重新映射标签文件
                    remap_label_file(src_label, dst_label, label_mapping, original_classes)
                    print(f"重新映射标签: {label_file}")
                else:
                    # 直接复制
                    shutil.copy2(src_label, dst_label)
                    print(f"复制标签: {label_file}")

def create_yaml(merged_classes):
    """创建data.yaml文件"""
    yaml_content = f"""path: ./  # 相对路径，dataset root dir
train: images  # train images (relative to 'path')
val:   # 没有验证集
nc: {len(merged_classes)}  # 类别数量
names: {merged_classes}  # 类别名称
"""
    with open(TARGET_PATH / 'data.yaml', 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    print("创建data.yaml文件完成")

def main():
    print("开始合并数据集...")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"数据集1路径: {DATASET1_PATH}")
    print(f"数据集2路径: {DATASET2_PATH}")
    print(f"目标数据集路径: {TARGET_PATH}")
    
    # 检查目录是否存在
    for path, name in [(DATASET1_PATH, "数据集1"), (DATASET2_PATH, "数据集2")]:
        if not os.path.exists(path):
            print(f"警告: {name}根目录不存在: {path}")
    
    # 合并类别并获取映射关系
    merged_classes, mapping1, mapping2 = merge_classes()
    
    # 读取原始类别列表
    classes1 = read_classes(DATASET1_PATH / 'labels' / 'classes.txt')
    classes2 = read_classes(DATASET2_PATH / 'lables' / 'classes.txt')
    
    # 尝试多种可能的目录结构
    dataset1_images_paths = [
        DATASET1_PATH / 'images', 
        DATASET1_PATH / 'image',
        DATASET1_PATH / 'img'
    ]
    
    dataset1_labels_paths = [
        DATASET1_PATH / 'labels',
        DATASET1_PATH / 'label',
        DATASET1_PATH / 'lables'  # 可能的拼写错误
    ]
    
    dataset2_images_paths = [
        DATASET2_PATH / 'images',
        DATASET2_PATH / 'image',
        DATASET2_PATH / 'img'
    ]
    
    dataset2_labels_paths = [
        DATASET2_PATH / 'lables',  # 注意这里是'lables'而不是'labels'（根据原有代码）
        DATASET2_PATH / 'labels',
        DATASET2_PATH / 'label'
    ]
    
    # 找到有效的图像目录和标签目录
    dataset1_images = None
    dataset1_labels = None
    for path in dataset1_images_paths:
        if os.path.exists(path):
            dataset1_images = path
            print(f"找到数据集1图像目录: {path}")
            break
    
    for path in dataset1_labels_paths:
        if os.path.exists(path):
            dataset1_labels = path
            print(f"找到数据集1标签目录: {path}")
            break
    
    dataset2_images = None
    dataset2_labels = None
    for path in dataset2_images_paths:
        if os.path.exists(path):
            dataset2_images = path
            print(f"找到数据集2图像目录: {path}")
            break
    
    for path in dataset2_labels_paths:
        if os.path.exists(path):
            dataset2_labels = path
            print(f"找到数据集2标签目录: {path}")
            break
    
    # 复制并重新映射第一个数据集
    print(f"\n处理数据集1: {DATASET1_PATH}")
    if dataset1_images and dataset1_labels:
        copy_files(
            dataset1_images, 
            dataset1_labels, 
            mapping1, 
            classes1
        )
    else:
        print("无法找到数据集1的图像或标签目录，跳过处理")
    
    # 复制并重新映射第二个数据集
    print(f"\n处理数据集2: {DATASET2_PATH}")
    if dataset2_images and dataset2_labels:
        copy_files(
            dataset2_images, 
            dataset2_labels, 
            mapping2, 
            classes2
        )
    else:
        print("无法找到数据集2的图像或标签目录，跳过处理")
    
    # 创建data.yaml文件
    create_yaml(merged_classes)
    
    # 统计文件数量
    image_count = len([f for f in os.listdir(TARGET_IMAGES) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    label_count = len([f for f in os.listdir(TARGET_LABELS) if f.lower().endswith('.txt') and f != 'classes.txt'])
    
    print(f"\n合并完成！")
    print(f"合并后的数据集包含:")
    print(f"- 图像文件: {image_count}张")
    print(f"- 标签文件: {label_count}个")
    print(f"- 类别总数: {len(merged_classes)}个")
    
if __name__ == "__main__":
    main() 