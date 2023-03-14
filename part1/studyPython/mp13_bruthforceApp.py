# 암호해제 App
# 무차별 대입 공격 - zip파일
import itertools
import time
import zipfile

passwd_string = '0123456789' # 패스워드에 영문자도 들어있으면 
# passwd_string = '0123456789abc..xyzABC..XYZ'

file = zipfile.ZipFile('./studyPython/새 압축.zip')

isFind = False # 암호를 찾았는지 물어보는것

for i in range(6,7):
    attempts = itertools.product(passwd_string, repeat=i)
    for attempt in attempts:
        try_pass = ''.join(attempt)
        print(try_pass)

        try:
            file.extractall(pwd = try_pass.encode(encoding='utf-8'))
            print(f'암호는 {try_pass}입니다')
            isFind = True; break
        except:
            pass

    if isFind == True: break