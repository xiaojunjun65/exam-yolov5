import os
import cv2
import torch
import numpy as np
#现在我们要完成安全帽检测，安全帽模型需要的输入维度为【1.3.640.640】请按照这个维度完成前处理编码
#输入图片为单张图片路径，请输出一个torch.Size([1, 3, 640, 640])维度
#单张图片测试路径D:\exam\data\img_v3_025q_477893a1-7acf-4b00-8ab9-995c9cc5cc9g.jpg
def preprocess(pic):
    img = cv2.imread(pic)
    img = cv2.resize(img,(640,640))
    img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    img = np.ascontiguousarray(img)
    im = torch.from_numpy(img)
    im = im.float()  # uint8 to fp16/32
    im /= 255  # 0 - 255 to 0.0 - 1.0
    if len(im.shape) == 3:
        im = im[None]  # expand for batch dim
    return im