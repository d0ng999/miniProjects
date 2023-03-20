import pandas as pd
import folium # pip install folium

filePath = './studyPython/university_locations.xlsx'
df_excel = pd.read_excel(filePath, engine='openpyxl', header=None)
df_excel.columns = ['학교명', '주소', 'lng', 'lat'] # lat = 위도, lng = 경도
# print(df_excel)
name_list = df_excel['학교명'].to_list()
addr_list = df_excel['주소'].to_list()
lng_list = df_excel['lng'].to_list()
lat_list = df_excel['lat'].to_list()

fMap = folium.Map(location=[37.553175, 126.989326], zoom_start=10) # 위치의 기준을 잡는다(서울)

for i in range(len(name_list)): # 466번
    if lng_list[i] != 0: # 0이면 위/경도값이 출력 불가
        marker = folium.Marker([lat_list[i], lng_list[i]], popup=name_list[i],
                               icon=folium.Icon(color='blue'))
        marker.add_to(fMap)
fMap.save('./studyPython/Korea_universites.html')