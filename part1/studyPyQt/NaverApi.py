# NaverApi 클래스 - OpenApi : 인터넷을 통해서 데이터를 전달받는다.
from urllib.request import Request,  urlopen
from urllib.parse import quote
import datetime # 현재시간 사용
import json # 결과는 json으로 확인

class NaverApi:
    # 생성자
    def __init__(self) -> None:
        print(f'[{datetime.datetime.now()}] Naver API 생성')    
        
    # Naver API를 요청하는 중요한 함수
    def get_request_url(self, url):
        req = Request(url)

        # Naver API 개인별 인증
        req.add_header('X-Naver-Client-Id', 'SQqJyKQTKTlV_nAnylvw')
        req.add_header('X-Naver-Client-Secret', 'Y8w_59XP0C')

        try:
            res = urlopen(req) # 요청 결과가 바로 돌아온다.
            if res.getcode() == 200: # Response OK, 제대로 값을 돌려받았다.
                print(f'[{datetime.datetime.now()}] NaverAPI 요청 성공')
                return res.read().decode('utf-8')
            else:
                print(f'[{datetime.datetime.now()}] NaverAPI 요청 실패')
                return None
        except Exception as e:
            print(f'[{datetime.datetime.now()}] 예외발생 : {e}')
            return None
    
    # 실제 (중요한) 호출함수
    def get_naver_search(self, node, search, start, display):
        base_url = 'https://openapi.naver.com/v1/search'
        node_url = f'/{node}.json'
        params = f'?query={quote(search)}&start={start}&display={display}'

        url = base_url + node_url + params
        retData = self.get_request_url(url)

        if retData == None:
            return None
        else:
            return json.loads(retData) # json으로 return해준다.