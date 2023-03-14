# 텍스트가 음성으로
# pip install gTTS
# pip install playsound

from gtts import gTTS
from playsound import playsound # 바로 음성출력됨

text = '안녕하세요, 홍동현입니다'

tts = gTTS(text = text, lang = 'ko', slow = False)
tts.save('./studyPython/output/hi.mp3')

print('완료')
playsound('./studyPython/output/hi.mp3')
print('음성출력완료')