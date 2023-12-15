import cv2
from yolov5.models.yolo import Model
import torch
import numpy as np
from config import *
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import  non_max_suppression, scale_coords
from yolov5.utils.augmentations import Albumentations, augment_hsv, copy_paste, letterbox, mixup, random_perspective
def scale_boxes(img1_shape, boxes, img0_shape, ratio_pad=None):
    # Rescale boxes (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    boxes[:, [0, 2]] -= pad[0]  # x padding
    boxes[:, [1, 3]] -= pad[1]  # y padding
    boxes[:, :4] /= gain
    clip_boxes(boxes, img0_shape)
    return boxes
def clip_boxes(boxes, shape):
    # Clip boxes (xyxy) to image shape (height, width)
    if isinstance(boxes, torch.Tensor):  # faster individually
        boxes[:, 0].clamp_(0, shape[1])  # x1
        boxes[:, 1].clamp_(0, shape[0])  # y1
        boxes[:, 2].clamp_(0, shape[1])  # x2
        boxes[:, 3].clamp_(0, shape[0])  # y2
    else:  # np.array (faster grouped)
        boxes[:, [0, 2]] = boxes[:, [0, 2]].clip(0, shape[1])  # x1, x2
        boxes[:, [1, 3]] = boxes[:, [1, 3]].clip(0, shape[0])  # y1, y2
import random
def plot_one_box(x, img, color=None, label=None, line_thickness=3):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
    return img
model = DetectMultiBackend(MODEL_URL, device="cpu", dnn=False)
model.model.float()

def model_test():
    import  time
    a1 = time.time()
    image = cv2.imread(PIC_TEST)
    img0 = image
    from temp_preprocess import preprocess

    img = preprocess(PIC_TEST)
    pred = model(img)
    pred = non_max_suppression(pred, 0.3, 0.4, None, True)
    for i, det in enumerate(pred):
        import json

        print(det)
        data_list = []
        cls_list = []
        conf_list = []
        if len(det):
            # Rescale boxes from img_size to im0 sizes
            print(img0.shape)
            det[:, :4] = scale_boxes((640, 640, 3), det[:, :4], img0.shape).round()
            # Write results
            for *xyxy, conf, cls in reversed(det):
                # label = f'{names[int(cls)]} {conf:.2f}'
                img_result = plot_one_box(xyxy, img0, line_thickness=3)
                data_list_a = {
                    "class": int(cls.item()),  # 目标分类id
                    "confidence": float(conf.item()),  # 目标置信度
                    "name": int(cls.item()),  # 目标分类名称
                    "xmin": float(xyxy[0].item()),  # 目标位置矩形框左上角顶点X轴坐标值
                    "ymin": float(xyxy[1].item()),  # 目标位置矩形框左上角顶点Y轴坐标值
                    "xmax": float(xyxy[2].item()),  # 目标位置矩形框右下角顶点X轴坐标值
                    "ymax": float(xyxy[3].item())  # 目标位置矩形框右下角顶点Y轴坐标值
                }
                conf_list.append(float(conf.item()))
                cls_list.append(cls.item())
                data_list.append(data_list_a)
                print("xyxy:", xyxy)
                print("conf  or cls", conf, cls)
    print(len(cls_list))
    print(sum(conf_list) / len(conf_list))
    b1 = time.time()
    return img0,len(cls_list),sum(conf_list) / len(conf_list),b1-a1
