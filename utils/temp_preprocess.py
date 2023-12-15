import os
import cv2
import torch
import numpy as np
#��������Ҫ��ɰ�ȫñ��⣬��ȫñģ����Ҫ������ά��Ϊ��1.3.640.640���밴�����ά�����ǰ�������
#����ͼƬΪ����ͼƬ·���������һ��torch.Size([1, 3, 640, 640])ά��
#����ͼƬ����·��D:\exam\data\img_v3_025q_477893a1-7acf-4b00-8ab9-995c9cc5cc9g.jpg
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