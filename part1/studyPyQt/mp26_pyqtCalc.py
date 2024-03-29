import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * # QIcon은 여기 있음

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/calculator.ui', self)
        # self.setWindowIcon(QIcon('./studyPyQt/movie.png'))

        # 시그널 16개에 슬롯함수는 1개
        self.btn_C.clicked.connect(self.btnClicked)
        self.btn_number0.clicked.connect(self.btnClicked)
        self.btn_number1.clicked.connect(self.btnClicked)
        self.btn_number2.clicked.connect(self.btnClicked)
        self.btn_number3.clicked.connect(self.btnClicked)
        self.btn_number4.clicked.connect(self.btnClicked)
        self.btn_number5.clicked.connect(self.btnClicked)
        self.btn_number6.clicked.connect(self.btnClicked)
        self.btn_number7.clicked.connect(self.btnClicked)
        self.btn_number8.clicked.connect(self.btnClicked)
        self.btn_number9.clicked.connect(self.btnClicked)
        self.btn_result.clicked.connect(self.btnClicked)
        self.btn_add.clicked.connect(self.btnClicked)
        self.btn_minus.clicked.connect(self.btnClicked)
        self.btn_divide.clicked.connect(self.btnClicked)
        self.btn_multipy.clicked.connect(self.btnClicked)
        
        self.txt_view.setEnabled(False)
        self.text_value = ''
        
    def btnClicked(self):
        btn_val = self.sender().text()
        if btn_val == 'C': # clear
            print('clear')
            self.txt_view.setText('0')
            self.text_value = ''

        elif btn_val == '=': # 계산결과
            print('=')
            try:
                result = eval(self.text_value.lstrip('0')) # eval : 스트링 문자값을 숫자로 계산
                print(round(result, 4)) # 반올림 4째 자릿수
                self.txt_view.setText(str(round(result, 4)))
            except:
                self.text_view.setText('ERROR')
        else:
            self.text_value += btn_val
            self.txt_view.setText(self.text_value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())