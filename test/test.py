import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt

def detect_objects(image_path):
    # 加载模型
    model = YOLO('../model/digua_best_5_8.pt')

    # 执行推理
    results = model(image_path)

    # 提取检测结果
    detected_boxes = []
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # 边界框坐标（xyxy格式）
        classes = result.boxes.cls.cpu().numpy()  # 类别ID
        confidences = result.boxes.conf.cpu().numpy()  # 置信度

        # 保存检测结果
        for box, cls, conf in zip(boxes, classes, confidences):
            label = f"{model.names[int(cls)]} {conf:.2f}"
            detected_boxes.append((box, label))

    # 可视化结果
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换颜色通道

    # 绘制边界框和标签
    for box, label in detected_boxes:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # 显示图像
    plt.figure(figsize=(12, 8))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    image_path = "../data/images/20250407_151005_356444.jpg"
    detect_objects(image_path)