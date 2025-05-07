# 数据集合并工具

此脚本用于合并两个YOLO格式的标注数据集，适用于在不同电脑上标注的数据集合并场景。

## 功能特点

1. 自动合并两个子数据集的所有图像和标签文件
2. 智能处理类别合并，确保标签不会错乱
3. 自动创建合并后的classes.txt文件，包含所有类别
4. 生成符合YOLO要求的data.yaml配置文件
5. 全部使用相对路径，便于跨平台使用

## 使用方法

1. 确保两个子数据集已经按以下结构放置：
   - 数据集1: `../dataLei/`
     - 图像: `../dataLei/images/`
     - 标签: `../dataLei/labels/`
     - 类别文件: `../dataLei/labels/classes.txt`
   
   - 数据集2: `../photo/`
     - 图像: `../photo/images/`
     - 标签: `../photo/lables/` (注意这个文件夹名称是lables而不是labels)
     - 类别文件: `../photo/lables/classes.txt`

2. 运行合并脚本：
   ```
   python merge_datasets.py
   ```

3. 脚本会:
   - 合并两个数据集的类别文件
   - 复制所有图像文件到`./images/`目录
   - 复制并重新映射所有标签文件到`./labels/`目录
   - 创建新的`data.yaml`文件

4. 运行完成后，合并的数据集将包含:
   - 所有图像文件: `./images/`
   - 所有标签文件: `./labels/`
   - 合并后的类别文件: `./labels/classes.txt`
   - YOLO配置文件: `./data.yaml`

## 类别映射说明

脚本会自动处理类别ID的映射，确保:

1. 合并后的classes.txt包含所有不重复的类别名称
2. 每个标签文件中的类别ID会根据新的类别列表正确重新映射
3. 相同类别名称在合并后会使用同一个类别ID

这样可以确保训练时不会出现类别混淆的问题。 