import  os
from datetime import datetime

CURRENT_TIME = datetime.now()
ADMIN_XLSX_FILE = "admin.csv"
DATASET_SET = "D:\exam\data"
LOGING=False
PYCHARM_PATH = r"D:\PyCharm Community Edition 2023.2.5\bin\pycharm64.exe"

PY_PATH = r"D:\exam\py_sys\temp_preprocess.py"

GONGGAO = """
=========================================
登录成功，下面来做平台讲解

手册阅读-接口文档及注意事项

查看数据集样图-弹出每张数据集的第一张样图

弹出编码框-会打开所需要的编码环境，编码完成直接关闭即可

测试按钮：后台会直接调用你的编码环境模拟运行，提供第一张图的结果

提交按钮：测试结果无误之后，就可以直接提交了

!!如果第二次点击测试按钮后，结果有误，请重启程序后再点击测试按钮即可。

=========================================
"""

PIC_TEST = "D:\exam\data\img_v3_025q_477893a1-7acf-4b00-8ab9-995c9cc5cc9g.jpg"

TATGET_FILE = r"D:\exam\utils"

MODEL_URL ="D:\exam\yolov5\yolov5s.pt"