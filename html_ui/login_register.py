import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QHBoxLayout, QDesktopWidget
from PyQt5.QtGui import QColor, QFont
import  os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QLineEdit
)
from utils.config import  *
def create_admin_file_if_not_exist():
    # 检查文件是否存在
    if not os.path.isfile(ADMIN_XLSX_FILE):
        # 创建一个包含必要列的空 DataFrame
        df = pd.DataFrame(columns=['username', 'password', 'role'])
        # 将空 DataFrame 保存为 CSV 文件
        df.to_csv(ADMIN_XLSX_FILE, index=False)
create_admin_file_if_not_exist()

from html_ui.demo import AIPlatformMainWindow
class RegisterWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window  # 保存登录窗口的引用
        self.initUI()

    def initUI(self):
        self.setWindowTitle('注册')
        self.resize(300, 200)
        self.center()

        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #DDEEFF; font: 12pt 'Verdana';")


        # 创建注册窗口控件
        self.usernameLabel = QLabel('用户名')
        self.usernameLineEdit = QLineEdit()

        self.passwordLabel = QLabel('密码')
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.roleLabel = QLabel('职位')
        self.roleComboBox = QComboBox()
        self.roleComboBox.addItems(['管理员', '学生'])

        self.registerButton = QPushButton('注册')
        self.registerButton.clicked.connect(self.register)

        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameLineEdit)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordLineEdit)
        layout.addWidget(self.roleLabel)
        layout.addWidget(self.roleComboBox)
        layout.addWidget(self.registerButton)

        self.setLayout(layout)

    def register(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        role = self.roleComboBox.currentText()
        if not username.strip():
            QMessageBox.warning(self, '错误', '用户名不能为空')
            return
        # 检查用户名是否已存在
        # try:
        df = pd.read_csv(ADMIN_XLSX_FILE)
        if username.strip() in df['username'].astype(str).values:
            QMessageBox.warning(self, '错误', '用户名已存在')
            return
        # except FileNotFoundError:
        df = pd.DataFrame(columns=['username', 'password', 'role'])

        # 将新用户信息添加到DataFrame并保存
        df = df.append({'username': username, 'password': password, 'role': role}, ignore_index=True)
        df.to_csv(ADMIN_XLSX_FILE, mode='a', header=not os.path.isfile('admin.csv'),index=False)

        QMessageBox.information(self, '注册成功', '注册成功！')
        self.close()
        self.login_window.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('人工智能实训平台')
        self.resize(300, 200)
        self.center()
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #DDEEFF; font: 12pt 'Verdana';")


        # 创建登录界面控件
        self.usernameLabel = QLabel('用户名')
        self.usernameLineEdit = QLineEdit()

        self.passwordLabel = QLabel('密码')
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.loginButton = QPushButton('登录')
        self.loginButton.clicked.connect(self.login)

        self.registerButton = QPushButton('注册')
        self.registerButton.clicked.connect(self.openRegisterWindow)
        self.loginButton.clicked.connect(self.onLoginClicked)
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameLineEdit)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordLineEdit)
        layout.addWidget(self.loginButton)
        layout.addWidget(self.registerButton)

        self.setLayout(layout)

    def login(self):
        global  LOGING
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        if not username.strip():
            QMessageBox.warning(self, '错误', '用户名不能为空')
            return
        try:
            df = pd.read_csv(ADMIN_XLSX_FILE)
            user = df[(df['username'].astype(str).values == username.strip()) & (df['password'].astype(str).values == password.strip())]
            if not user.empty:
                role = user['role'].values[0]
                LOGING = True
                QMessageBox.information(self, '登录成功', f'{role}登录成功！')


            else:
                QMessageBox.warning(self, '登录失败', '用户名或密码错误')
        except FileNotFoundError:
            QMessageBox.warning(self, '登录失败', '用户不存在')

    def onLoginClicked(self):
        # 当登录按钮被点击时弹出新窗口
        if LOGING:
            self.close()
            self.popUp = AIPlatformMainWindow()
            self.popUp.show()
    def openRegisterWindow(self):
        self.hide()  # 隐藏登录窗口
        self.registerWindow = RegisterWindow(self)  # 将当前登录窗口传递给注册窗口
        self.registerWindow.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())




