import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from NaverApi import *
from PyQt5.QtGui import *
import webbrowser # 웹브라우저 모듈
from urllib.request import urlopen

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiMovie.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/movie.png'))

        # 검색 버튼 클릭 시그널에 대한 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 엔터를 치면 처리하는 함수
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)

    def tblResultDoubleClicked(self):
        # row = self.tblResult.currentIndex().row()
        # column = self.tblResult.currentIndex().column()
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 5).text() # url 링크 컬럼 변경
        webbrowser.open(url) # 네이버 영화 링크가 열린다.


    def txtSearchReturned(self):
        self.btnSearchClicked()

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '영화명을 입력하세요^오^')
            return 
        else:
            api = NaverApi() # NaverApi 클래스의 객체를 생성
            node = 'movie' # movie로 변경하면 영화를 검색할 수 있다.
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            print(result)
            # QMessageBox.about(self, 'result', result)
            # 테이블 위젯에 출력 기능
            items = result['items'] # Json 결과중에서 items 아래 배열만 추출
            self.makeTable(items) # 테이블 위젯에 데이터들을 할당하는 함수
    
    # 테이블 위젯에 데이터 표시하기 위한 함수 --> 네이버영화 결과에 맞게 변경 필요!
    def makeTable(self, items) -> None:
        # 단일선택만 할 수 있게 만듦
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) 
        self.tblResult.setColumnCount(7) # 컬럼 갯수 변경
        self.tblResult.setRowCount(len(items)) # items의 개수만큼 행이 생성
        self.tblResult.setHorizontalHeaderLabels(['영화제목', '개봉연도', '감독', '배우진',
                                                   '평점', '링크', '포스터'])
        self.tblResult.setColumnWidth(0, 150)
        self.tblResult.setColumnWidth(1, 60) # 개봉연도
        self.tblResult.setColumnWidth(4, 40) # 평점
        # 컬럼의 데이터를 수정할 수 없게 만들어줌
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # enumerate 각 행의 인덱스 값도 들고 온다아아!
        for i, post in enumerate(items): # 0, 영화...
            title = self.replaceHtmlTag(post['title']) # HTML 특수문자 / 영어제목 가져오기 추가
            subtitle = post['subtitle']
            title = f'{title}\n({subtitle})'
            pubDate = post['pubDate'] # HTML 특수문자
            director = post['director'].replace('|', ',')[:-1] # HTML 특수문자, [:-1]마지막 쉼표는 없애
            actor = post['actor'].replace('|',',')[:-1] # HTML 특수문자, [:-1]마지막 쉼표는 없애
            userRating = post['userRating'] # HTML 특수문자
            link = post['link']
            img_url = post['image']
            
            # print(img_url == '') image 값이 None인지, '' = 빈 값인지 확인 
            if img_url != '': # 빈 값이면 포스터가 없음
                # 2진 데이터 - 네이버영화에 있는 이미지 다운, 데이터를 불러온다.
                data = urlopen(img_url).read() # -> 텍스트 형태의 데이터
                image = QImage() # 이미지를 담을 수 있는 객체를 만들어줌
                image.loadFromData(data)
                # QTableWidget은 이미지를 그냥 넣을 수 없음
                # QLabel()에 넣은 후 이를 QTableWidget에 넣어야 한다
                imgLabel = QLabel()
                imgLabel.setPixmap(QPixmap(image))
                
                # data를 이미지로 저장가능!
                # 테스트 - 이미지를 가져오는 용도(필요시 사용)
                # f = open(f'./studyPyQt/temp/image_{i+1}.png', mode = 'wb') # 파일쓰기
                # f.write(data)
                # f.close()
                            
            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))
            self.tblResult.setItem(i, 2, QTableWidgetItem(director))
            self.tblResult.setItem(i, 3, QTableWidgetItem(actor))
            self.tblResult.setItem(i, 4, QTableWidgetItem(userRating))
            self.tblResult.setItem(i, 5, QTableWidgetItem(link))
            
            if img_url != '':
                self.tblResult.setCellWidget(i, 6, imgLabel)
                self.tblResult.setRowHeight(i, 110) # 포스터가 있으면 쉘의 높이를 늘려줌
            else:
                self.tblResult.setItem(i, 6, QTableWidgetItem('No Poster'))
                
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