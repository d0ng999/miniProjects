# 전국 대학교 List
# pandas
import pandas as pd # pip install pandas

filePath = './studyPython/university_list_2020.xlsx'
df_excel = pd.read_excel(filePath, engine='openpyxl') # 이미 설치한 openpyxl

df_excel.columns = df_excel.loc[4].tolist()
df_excel = df_excel.drop(index=list(range(0, 5))) # 실제 데이터 이외 행을 다 날려버림

print(df_excel.head()) # head() 는 상위 5개만 출력
print(df_excel['학교명'].values)
print(df_excel['주소'].values)

