import  os
import cv2
from  utils.config import *
def read_pic_look():
    pic_path = os.listdir(DATASET_SET)
    img = cv2.imread(DATASET_SET+str('/')+str(pic_path[0]))
    return img
