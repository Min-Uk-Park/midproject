import sys,os
# streamlit run midproject.py # 웹 실행 위한 명령프롬포트 입력문장예시 100100118

# 현재 작업 위치 확인
# print(os.getcwd())
# c:\lang_practice\Python_practice

# 현재 시간 표시와 버스 라우트 ID 엑셀로 받아와서 multiselect로 구현해보기
sys.path.append('c:/Users/LG/anaconda3/Lib/site-packages')
import requests,re
from bs4 import BeautifulSoup as bs 
import streamlit as st
import folium
from streamlit_folium import st_folium
import time
import csv
import pandas as pd
bus = 100100118

url = 'http://ws.bus.go.kr/api/rest/buspos/getLowBusPosByRtid'
params ={'serviceKey' : '0OhBU7ZCGIobDVKDeBJDpmDRqK3IRNF6jlf/JB2diFAf/fR2czYO9A4UTGcsOwppV6W2HVUeho/FPwXoL6DwqA==', 'busRouteId' : bus }

response = requests.get(url, params=params)
soup = bs(response.text,'lxml-xml')

os.chdir('C:/CBNU_data/2_2/opensource2_2')


RoutedID_df = pd.read_csv('서울시버스노선별정류소정보(20231026).csv',encoding='cp949',thousands=',')
        
   
RoutedIDList = list(RoutedID_df['ROUTE_ID'])
print(RoutedIDList)

