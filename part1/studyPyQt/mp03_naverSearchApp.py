import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from NaverApi import *
from PyQt5.QtGui import *
import webbrowser # 웹브라우저 모듈

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiSearch.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/newspaper.png'))

        # 검색 버튼 클릭 시그널에 대한 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 엔터를 치면 처리하는 함수
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)

    def tblResultDoubleClicked(self):
        # row = self.tblResult.currentIndex().row()
        # column = self.tblResult.currentIndex().column()
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 1).text()
        webbrowser.open(url) # 뉴스기사 웹사이트 오픈!


    def txtSearchReturned(self):
        self.btnSearchClicked()

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '검색어를 입력하세요^오^')
            return 
        else:
            api = NaverApi() # NaverApi 클래스의 객체를 생성
            node = 'news' # movie로 변경하면 영화를 검색할 수 있다.
            outputs = [] # 결과를 담을 리스트 변수
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            # print(result)
            # QMessageBox.about(self, 'result', result)
            # 테이블 위젯에 출력 기능
            items = result['items'] # Json 결과중에서 items 아래 배열만 추출
            self.makeTable(items) # 테이블 위젯에 데이터들을 할당하는 함수
    
    # 테이블 위젯에 데이터 표시하기 위한 함수
    def makeTable(self, items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) # 단일선택만 할 수 있게 만듦
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(items)) # items의 개수만큼 행이 생성
        self.tblResult.setHorizontalHeaderLabels(['기사제목', '뉴스링크'])
        self.tblResult.setColumnWidth(0, 310)
        self.tblResult.setColumnWidth(1, 260)
        # 컬럼의 데이터를 수정할 수 없게 만들어줌
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 뉴스...
            title = self.replaceHtmlTag(post['title']) # HTML 특수문자
            originallink = post['originallink']
            
            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(originallink))
            
    def replaceHtmlTag(self, sentence) -> str:
        result = sentence.replace('&lt;', '<') # lesser than
        result = result.replace('&gt;', '>') # greater than
        result = result.replace('<b>', '') # bold , 글자를 진하게 하는 방법은 없다.
        result = result.replace('</b>', '') # bold
        result = result.replace('&apos', "'") # apostopy
        result = result.replace('&quot', '"') # quotation mark 
        # 변환 안된 특수문자가 나타나면 여기에 추가
        return result
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())