from PyQt5.QtGui import QIcon
import keyboard
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit
import sys

class ScriptGUI(QWidget):
 def __init__(self):
     super().__init__()

     self.init_ui()

 def init_ui(self):
     self.setWindowTitle('森林全自动刷木头脚本')
     self.setGeometry(300, 300, 600, 600)  # 设置窗口位置和大小

     layout = QVBoxLayout()

     self.start_button = QPushButton('启动脚本')
     self.start_button.clicked.connect(self.start_script)
     layout.addWidget(self.start_button)

     self.stop_button = QPushButton('停止脚本')
     self.stop_button.clicked.connect(self.stop_script)
     layout.addWidget(self.stop_button)

     self.time_input = QLineEdit()
     self.time_input.setPlaceholderText('自动停止时间（秒）')
     layout.addWidget(self.time_input)

     self.setLayout(layout)

     # 将F6键绑定到“启动脚本”按钮
     keyboard.add_hotkey('f6', self.start_button.click)

     # 设置窗口图标
     self.setWindowIcon(QIcon('icon.png'))  # 替换为您的图标文件路径

 def start_script(self):
     start_time = time.time()
     while True:
         # 模拟按下E键
         keyboard.press_and_release('e')
         time.sleep(0.2)  # 等待0.2秒
         keyboard.press_and_release('e')
         time.sleep(0.2)  # 等待0.2秒
         keyboard.press_and_release('e')
         time.sleep(0.2)  # 等待0.2秒
         # 模拟按下C键
         keyboard.press_and_release('c')
         time.sleep(0.2)  # 等待0.2秒
         keyboard.press_and_release('c')
         time.sleep(0.2)  # 等待0.2秒

         # 检查脚本是否需要停止
         if time.time() - start_time > int(self.time_input.text()):  # 设置脚本运行的最大时间（以秒为单位）
             break

 def stop_script(self):
     keyboard.press_and_release('e')
     keyboard.press_and_release('e')
     keyboard.press_and_release('e')
     keyboard.press_and_release('c')

     # 添加以下代码，使脚本在达到自动停止时间后自动停止
     start_time = time.time()
     while True:
         if time.time() - start_time > int(self.time_input.text()):
             break

if __name__ == '__main__':
 app = QApplication(sys.argv)
 gui = ScriptGUI()
 gui.show()
 sys.exit(app.exec_())