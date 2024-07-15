from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QSlider, QLabel, QComboBox, QDialog, QDialogButtonBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent
from WorkerThread import WorkerThread

import keyboard,keyword
import time
import sys

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('设置')
        self.setGeometry(350, 350, 400, 300)  # 设置窗口位置和大小

        layout = QVBoxLayout()

        self.interval_slider = QSlider(Qt.Horizontal)
        self.interval_slider.setRange(10, 1000)  # 设置滑块范围（10ms到1000ms）
        self.interval_slider.setValue(100)  # 设置默认值
        layout.addWidget(QLabel('点击间隔（毫秒）'))
        layout.addWidget(self.interval_slider)

        self.key_combobox_1 = QComboBox()
        self.key_combobox_1.addItems(self.get_keyboard_keys())
        self.key_combobox_1.setCurrentText('e')
        layout.addWidget(QLabel('选择拾取键'))
        layout.addWidget(self.key_combobox_1)

        self.key_combobox_2 = QComboBox()
        self.key_combobox_2.addItems(self.get_keyboard_keys())
        self.key_combobox_2.setCurrentText('c')
        layout.addWidget(QLabel('选择丢弃键'))
        layout.addWidget(self.key_combobox_2)
        
        self.start_shortcut_input = QLineEdit()
        self.start_shortcut_input.setPlaceholderText('启动脚本快捷键')
        self.start_shortcut_input.setFocusPolicy(Qt.StrongFocus)  # 设置文本框可以接收键盘焦点
        layout.addWidget(QLabel('启动脚本快捷键'))
        layout.addWidget(self.start_shortcut_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

        # 监听文本框的键盘事件
        self.start_shortcut_input.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj == self.start_shortcut_input:
            key_text = event.text()
            if key_text:
                self.start_shortcut_input.setText(key_text)
                return True
        return super().eventFilter(obj, event)

    def get_settings(self):
        return (
            self.interval_slider.value(),
            self.key_combobox_1.currentText(),
            self.key_combobox_2.currentText(),
            self.start_shortcut_input.text()  # 返回启动脚本快捷键文本
        )

    def get_keyboard_keys(self):
        # 返回所有键盘按键作为选项
        keys = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'space', 'enter', 'shift', 'ctrl', 'alt', 'tab', 'esc', 'backspace',
            'delete', 'home', 'end', 'page_up', 'page_down', 'up', 'down', 'left', 'right'
        ]
        return keys

class ScriptGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.thread = None
        self.interval = 100
        self.key1 = 'e'
        self.key2 = 'c'
        self.start_shortcut = 'f6'  # 默认启动快捷键为 F6
        self.setup_global_shortcut()
    def setup_global_shortcut(self):
        # 使用keyboard库监听全局快捷键
        keyboard.add_hotkey(self.start_shortcut, self.start_script)


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

        self.settings_button = QPushButton('设置')
        self.settings_button.clicked.connect(self.open_settings_dialog)
        layout.addWidget(self.settings_button)

        self.setLayout(layout)

        # 设置窗口图标
        self.setWindowIcon(QIcon('icon.png'))  # 替换为您的图标文件路径

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        # 设置对话框中的默认启动快捷键
        dialog.start_shortcut_input.setText(self.start_shortcut)
        if dialog.exec_() == QDialog.Accepted:
            self.interval, self.key1, self.key2, self.start_shortcut = dialog.get_settings()

    def start_script(self):
        if self.thread is None or not self.thread.isRunning():
            try:
                duration = int(self.time_input.text())
                interval = self.interval / 1000.0  # 转换为秒
                keys = [(self.key1, 3), (self.key2, 2)]  # 设置按键和按压次数
            except ValueError:
                return

            self.thread = WorkerThread(duration, interval, keys)
            self.thread.finished.connect(self.on_thread_finished)
            self.thread.start()

    def stop_script(self):
        if self.thread is not None:
            self.thread.stop()

    def on_thread_finished(self):
        self.thread = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ScriptGUI()
    gui.show()
    sys.exit(app.exec_())
