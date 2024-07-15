from PyQt5.QtCore import QThread, pyqtSignal
import time
import keyboard

class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, duration, interval, keys):
        super().__init__()
        self.duration = duration
        self.interval = interval
        self.keys = keys
        self._running = True

    def run(self):
        start_time = time.time()
        while self._running and (time.time() - start_time) < self.duration:
            for key, count in self.keys:
                if not self._running:
                    break
                for _ in range(count):
                    keyboard.press(key)
                    time.sleep(0.05)  # ���º��ͷ�֮��Ķ��ݼ��
                    keyboard.release(key)
                    time.sleep(self.interval)
        
        self.finished.emit()

    def stop(self):
        self._running = False
