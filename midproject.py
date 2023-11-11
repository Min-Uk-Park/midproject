# streamlit run midproject.py # 웹 실행 위한 명령프롬포트 입력문장예시 100100118
# https://imgur.com/a/HXZaRau 이미지 배경화면 저장 url
# 현재 시간 표시와 버스 라우트 ID 엑셀로 받아와서 multiselect로 구현해보기
import sys,os
sys.path.append('c:/Users/LG/anaconda3/Lib/site-packages')
import requests,re
from bs4 import BeautifulSoup as bs 
import streamlit as st
import folium
from streamlit_folium import st_folium
import time
import csv
import pandas as pd

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.imgur.com/KDDTdC9.png[/img]");
             background-attachment: fixed;
             background-size: cover
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def find_values(data) :
        # write 즉, 출력내용 구하기 : 버스 번호, 좌표값
        bus_list = [i.text for i in data.find_all('plainNo')]
        x_list = [i.text for i in data.find_all('tmX')]
        y_list = [i.text for i in data.find_all('tmY')]
        
        return x_list, y_list, bus_list
    
def on_enter_pressed(key, busid, Routed, is_button_clicked) :
   # 입력 전 문구
    if is_button_clicked :
        if (busid == ''):
            st.write('please write data and press or click the enter')
            
        # if 정보를 입력하고 해당 정보가 옳은 정보라면 ~ 
        elif busid in  Routed :
            
            params ={'serviceKey' : key, 'busRouteId' : busid}

            response = requests.get(url, params=params)

            soup = bs(response.text,'lxml-xml')
            
            if (soup.find('headerMsg').text == '결과가 없습니다.') : 
                st.write('현재 버스가 조회되지 않습니다.')
                return
            
            else :
            # 입력 정보가 맞다면 'Success' 문구를 띄운다!
                with st.spinner('Wait for it'):
                    time.sleep(5)
                
                st.success("Success")
            
                lon_list, lat_list, busnum_list = find_values(soup)
                
                # show a bus number required before and total bus count
                count = str(len(busnum_list))
                st.write('조회된 총 버스 수 : ' + count)
            
                st.markdown(f"<h12 style='text-align: left; color: black;'>버스 번호 : {', '.join(map(str, busnum_list))}</h12>", unsafe_allow_html=True)

                # draw a map by using folium lib
                k = 0
                for busnum, lon, lat in zip(busnum_list, lon_list, lat_list) :
                    if (k == 0) :
                        m = folium.Map(location=[float(lat), float(lon)], zoom_start=12)
                        k += 1
                        
                    folium.Marker([float(lat), float(lon)], popup= f"{busnum}'s now location", 
                                tooltip="현재 버스 위치입니다.",
                                icon = folium.Icon(icon='bus',prefix = 'fa',color = 'green')).add_to(m)
                    
                st_data = st_folium(m, width=725)
                time.sleep(500)
            
        # if 만약 입력된 정보가 틀리다면 Error msg를 띄운다.
        else :
            # with st.spinner('Wait for it'):
            #     time.sleep(5)
            
            st.error('Error! please write correct bus number again')


# main함수부분
# title 가운데 정렬을 위한 코드
st.markdown("<h1 style='text-align: center; color: black;'>서울시 버스위치 정보 조회</h1>", unsafe_allow_html=True)

sys.path.append('c:\lang_practice\Python_practice')
url = 'http://ws.bus.go.kr/api/rest/buspos/getLowBusPosByRtid'


servicekey = '0OhBU7ZCGIobDVKDeBJDpmDRqK3IRNF6jlf/JB2diFAf/fR2czYO9A4UTGcsOwppV6W2HVUeho/FPwXoL6DwqA=='
busrouteid = ''

# background 꾸미기
add_bg_from_url()

# 값 입력받기
os.chdir('c://CBNU_data/2_2')
trynum = 1
RoutedID_df = pd.read_csv('서울시버스노선별정류소정보20231026.csv',encoding='cp949',thousands=',')
RoutedIDList = list(RoutedID_df['ROUTE_ID'])
    
busrouteid = st.selectbox('please write busRouteId', RoutedIDList ,key = "bus_input")
 
# clicked = st.button('click button') # 버튼은 따로 만들지 않는다. press button하면 값이 자동으로 입력되기 때문
trynum += 1
submit_button = st.button("Click")
on_enter_pressed(servicekey, busrouteid, RoutedIDList, submit_button)


    

    


    
    
    
    
    
