# 쓰레드 App
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # QIcon
from PyQt5.QtCore import * # Qt.white
import time

class BackgroundWorker(QThread): # PyQt5에 스레드를 위한 클래스가 존재
    procChanged = pyqtSignal(int)



    def __init__(self, count=0, parent=None) -> None:
        super().__init__()
        self.main = parent
        self.working = True # 스레드 동작여부
        self.count = count

    def run(self):
        # self.parent.pgbTask.setRange(0, 100)
        # for i in range(0, 101):
        #     print(f'스레드 출력 > {i}')
        #     self.parent.pgbTask.setValue(i)
        #     self.parent.txbLog.append(f'스레드 출력 > {i}') - 이 모든것들은 스레드를 위한 것
        while self.working:
            self.procChanged.emit(self.count) # 시그널을 내보냄
            self.count += 1 # 값 증가
            time.sleep(0.0001)

class qtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyThread/threadApp.ui', self)
        self.setWindowTitle('ThreadApp v0.5')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked)
        # 스레드 초기화
        self.worker = BackgroundWorker(parent=self, count=0)
        # 백그라운드 워커에 있는 시그널을 접근해서 처리해주기 위한 슬롯함수
        self.worker.procChanged.connect(self.procUpdated) 

        # 초기화
        self.pgbTask.setRange(0, 1000000)
    
    @pyqtSlot(int) # 데코레이션
    def procUpdated(self, count):
        self.txbLog.append(f'스레드 출력 > {count}')
        self.pgbTask.setValue(count)
        print(f'스레드 출력 > {count}')

    @pyqtSlot()
    def btnStartClicked(self):
        self.worker.start()
        self.worker.working = True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())