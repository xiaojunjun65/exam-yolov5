import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit

class EmittingStream(object):
    """
    一个重定向类，它将stdout重定向到指定的槽。
    """
    def write(self, text):
        """
        在写入时调用。
        """
        window.append_text(text)

    def flush(self):
        """
        必须实现的flush方法。
        """
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建QTextEdit控件
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # 设置窗口的标题和大小
        self.setWindowTitle("Terminal Output")
        self.resize(400, 300)

    def append_text(self, text):
        """
        将文本追加到文本编辑器中。
        """
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.insertPlainText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建窗口实例
    window = MainWindow()
    window.show()

    # 重定向stdout
    sys.stdout = EmittingStream()

    # 测试输出
    print("Hello, world!")

    sys.exit(app.exec_())
