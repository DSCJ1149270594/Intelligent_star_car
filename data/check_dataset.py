import os
from pathlib import Path

# 使用相对路径
DATASET_DIR = Path('.')  # 当前目录，即data文件夹
IMAGES_DIR = DATASET_DIR / 'images'
LABELS_DIR = DATASET_DIR / 'labels'

def check_train_val_consistency(subset='train'):
    """检查指定子集（train或val）的图像和标签文件名是否一致"""
    print(f"\n正在检查{subset}集...")
    
    images_path = IMAGES_DIR / subset
    labels_path = LABELS_DIR / subset
    
    # 检查目录是否存在
    if not os.path.exists(images_path):
        print(f"错误: 图像子目录不存在: {images_path}")
        return
    
    if not os.path.exists(labels_path):
        print(f"错误: 标签子目录不存在: {labels_path}")
        return
    
    # 获取图像和标签文件名（不带扩展名）
    image_files = []
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    for file in os.listdir(images_path):
        file_lower = file.lower()
        if any(file_lower.endswith(ext) for ext in image_extensions):
            # 去除扩展名，用于匹配标签文件
            base_name = os.path.splitext(file)[0]
            image_files.append((base_name, file))
    
    label_files = []
    for file in os.listdir(labels_path):
        if file.lower().endswith('.txt'):
            # 去除扩展名，用于匹配图像文件
            base_name = os.path.splitext(file)[0]
            label_files.append((base_name, file))
    
    # 转换为集合以便于比较
    image_bases = {item[0] for item in image_files}
    label_bases = {item[0] for item in label_files}
    
    # 找出存在不匹配的文件
    missing_labels = image_bases - label_bases
    missing_images = label_bases - image_bases
    
    # 输出统计信息
    print(f"图像数量: {len(image_files)}")
    print(f"标签数量: {len(label_files)}")
    
    if not missing_labels and not missing_images:
        print(f"✅ {subset}集图像和标签文件名完全匹配!")
    else:
        if missing_labels:
            print(f"❌ 有{len(missing_labels)}个图像缺少对应的标签文件:")
            for i, base in enumerate(sorted(missing_labels)):
                if i < 10:  # 只显示前10个
                    # 查找完整的文件名
                    full_name = next(name for b, name in image_files if b == base)
                    print(f"  - 图像: {full_name}，缺少标签: {base}.txt")
                else:
                    print(f"  ... 还有 {len(missing_labels) - 10} 个未显示")
                    break
        
        if missing_images:
            print(f"❌ 有{len(missing_images)}个标签文件缺少对应的图像:")
            for i, base in enumerate(sorted(missing_images)):
                if i < 10:  # 只显示前10个
                    # 查找完整的文件名
                    full_name = next(name for b, name in label_files if b == base)
                    print(f"  - 标签: {full_name}，缺少图像文件")
                else:
                    print(f"  ... 还有 {len(missing_images) - 10} 个未显示")
                    break
    
    return len(missing_labels), len(missing_images)

def main():
    print("开始检查数据集文件名一致性...")
    
    # 检查目录是否存在
    if not os.path.exists(IMAGES_DIR):
        print(f"错误: 图像目录不存在: {IMAGES_DIR}")
        return
    
    if not os.path.exists(LABELS_DIR):
        print(f"错误: 标签目录不存在: {LABELS_DIR}")
        return
    
    # 检查训练集
    train_missing_labels, train_missing_images = check_train_val_consistency('train')
    
    # 检查验证集
    val_missing_labels, val_missing_images = check_train_val_consistency('val')
    
    # 总结
    total_issues = train_missing_labels + train_missing_images + val_missing_labels + val_missing_images
    print("\n检查完成!")
    
    if total_issues == 0:
        print("✅ 恭喜! 数据集的图像和标签文件名完全匹配!")
    else:
        print(f"❌ 发现{total_issues}个不匹配问题:")
        print(f"  - 训练集: {train_missing_labels}个缺失标签, {train_missing_images}个缺失图像")
        print(f"  - 验证集: {val_missing_labels}个缺失标签, {val_missing_images}个缺失图像")
        print("\n建议: 运行split_dataset.py重新分割数据集或手动添加缺失的文件")

if __name__ == "__main__":
    main() 