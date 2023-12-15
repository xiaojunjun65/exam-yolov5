import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QLineEdit, QFrame
)
from PyQt5.QtGui import QImage, QPixmap
from utils.utut import  *
from PyQt5.QtCore import Qt


class ImageWindow(QWidget):
    def __init__(self, img):
        super().__init__()
        self.setWindowTitle("Image Display")

        # 创建QLabel显示图像
        label = QLabel(self)
        height, width, channel = img.shape
        step = channel * width
        qImg = QImage(img.data, width, height, step, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qImg))
        label.setAlignment(Qt.AlignCenter)

        # 设置窗口布局
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        self.setLayout(layout)
class AIPlatformMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('人工智能实训平台')
        self.setFixedSize(1024, 768)  # Fixed window size

        centralWidget = QWidget(self)
        mainLayout = QVBoxLayout(centralWidget)

        # Button layout at the top
        buttonLayout = QHBoxLayout()

        # Create buttons and add them to the layout
        self.button1 = QPushButton('手册阅读', self)
        self.button2 = QPushButton('查看数据集样图', self)
        self.button3 = QPushButton('弹出编码框', self)
        self.button4 = QPushButton('测试按钮', self)
        self.button5 = QPushButton('提交按钮', self)
        buttonLayout.addWidget(self.button1, 1)
        buttonLayout.addWidget(self.button2, 2)
        buttonLayout.addWidget(self.button3, 2)
        buttonLayout.addWidget(self.button4, 1)
        buttonLayout.addWidget(self.button5, 2)
        # Bottom layout for logs, image display, and info
        bottomLayout = QHBoxLayout()

        # Log display
        self.logDisplay = QTextEdit(self)
        self.logDisplay.setPlaceholderText('运行日志')
        self.logDisplay.append(GONGGAO)
        bottomLayout.addWidget(self.logDisplay, 2)

        # Image display
        self.imageDisplay = QLabel(self)
        self.imageDisplay.setStyleSheet('background-color: lightgray')
        self.imageDisplay.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        bottomLayout.addWidget(self.imageDisplay, 3)

        # Info display
        infoLayout = QVBoxLayout()

        self.confidenceDisplay = QLineEdit(self)
        self.confidenceDisplay.setPlaceholderText('置信度')
        infoLayout.addWidget(self.confidenceDisplay)

        self.categoryCountDisplay = QLineEdit(self)
        self.categoryCountDisplay.setPlaceholderText('类别个数')
        infoLayout.addWidget(self.categoryCountDisplay)
        self.button2.clicked.connect(self.up_pic)
        self.button3.clicked.connect(self.mkpy_or_test)
        self.button4.clicked.connect(self.py_test)
        self.timeDisplay = QLineEdit(self)
        self.timeDisplay.setPlaceholderText('时间')
        infoLayout.addWidget(self.timeDisplay)

        bottomLayout.addLayout(infoLayout, 1)

        # Add top and bottom layouts to the main layout
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(bottomLayout)

        self.setCentralWidget(centralWidget)
    def up_pic(self):
        self.image = read_pic_look()
        # cv2.imwrite("1.jpg",self.image)
        # # 转换颜色从BGR到RGB
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        self.image_window = ImageWindow(self.image)
        self.image_window.show()
    def mkpy_or_test(self):
        if os.path.exists(PY_PATH):
            self.logDisplay.append("PY文件已存在")
        else:
            with open(PY_PATH, 'w') as file:
                file.write(f'import os\nimport cv2\nimport torch\nimport numpy as np\n#现在我们要完成安全帽检测，安全帽模型需要的输入维度为【1.3.640.640】请按照这个维度完成前处理编码\n#输入图片为单张图片路径，请输出一个torch.Size([1, 3, 640, 640])维度\n#单张图片测试路径{PIC_TEST}\ndef preprocess(pic):\n')
                self.logDisplay.append("PY文件创建成功")
        import subprocess
        subprocess.Popen([PYCHARM_PATH, PY_PATH])

    def py_test(self):
        try:
            import shutil
            shutil.copy(PY_PATH, TATGET_FILE)
            from utils.test_demo import model_test
            show_image,cls,cnf,ti = model_test()
            self.confidenceDisplay.setText(str(cnf))
            self.categoryCountDisplay.setText(str(cls))
            self.timeDisplay.setText(str(ti)+"s")
            height, width, channel = show_image.shape
            bytes_per_line = 3 * width
            q_image = QImage(show_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            # 将 QImage 转换为 QPixmap 并调整大小以适应 QLabel
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(self.imageDisplay.size(), Qt.KeepAspectRatio)

            # 将 QPixmap 设置到 QLabel 上
            self.imageDisplay.setPixmap(scaled_pixmap)
            self.logDisplay.append("推理成功")

        except Exception as e:
            self.logDisplay.append(f"错误，报错信息{e}")






