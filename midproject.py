import sys,os
# streamlit run midproject.py # 웹 실행 위한 명령프롬포트 입력문장 100100118
# print(os.getcwd())
# c:\lang_practice\Python_practice

sys.path.append('c:/Users/LG/anaconda3/Lib/site-packages')
import requests,re
from bs4 import BeautifulSoup as bs 
import streamlit as st
import folium
from streamlit_folium import st_folium
import time

# title_alignment = """
# <style>
# #the-title {
#   text-align: center
# }
# </style>
# """
# st.markdown(title_alignment, unsafe_allow_html=True)
# st.title('서울시 버스위치 정보 조회')

# title 가운데 정렬을 위한 코드
st.markdown("<h1 style='text-align: center; color: black;'>서울시 버스위치 정보 조회</h1>", unsafe_allow_html=True)
# https://imgur.com/a/HXZaRau
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.imgur.com/6570N9e.jpg[/img]");
             background-attachment: fixed;
             background-size: cover
             
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def find_values(data) :
    # write 즉, 출력내용 구하기 : 버스 번호, 좌표값
        find_lon = float(data.find('tmX').text)
        find_lat = float(data.find('tmY').text)
        find_busnum = data.find('plainNo').text
        
        return find_lon, find_lat, find_busnum
    
def on_enter_pressed(busid) :
   # 입력 전 문구
    if (busid == ''):
        st.write('please write data and press or click the enter')
        
    # if 정보를 입력하고 해당 정보가 옳은 정보라면 ~ 
    elif (re.match('\d{9}',busid)) :

        params ={'serviceKey' : servicekey, 'busRouteId' : busid, 'startOrd' : '1', 'endOrd' : '10'}

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
            lon, lat, busnum = find_values(soup)
            
        
        # data_key = ['busnum', 'LAT', 'lon']
        # data_list = [busnum, lat, lon]
        # data_dict = {'lat':[lat], 'lon':[lon]}
        
        # show a bus number required before
        st.write('bus number : ' + busnum)
        # st.write(data_dict)
        
        # draw a map by using folium lib
        m = folium.Map(location=[lat, lon], zoom_start=16)
        
        folium.Marker([lat, lon], popup= f"{busnum}'s now location", 
                    tooltip="현재 버스 위치입니다.",
                    icon = folium.Icon(icon='bus',prefix = 'fa',color = 'green')).add_to(m)
        
        st_data = st_folium(m, width=725)
    
    # if 만약 입력된 정보가 틀리다면 Error msg를 띄운다.
    else :
        with st.spinner('Wait for it'):
            time.sleep(5)
        
        st.error('Error! please write correct bus number again')


# main함수부분
sys.path.append('c:\lang_practice\Python_practice')
url = 'http://ws.bus.go.kr/api/rest/buspos/getBusPosByRouteSt'

servicekey = '0OhBU7ZCGIobDVKDeBJDpmDRqK3IRNF6jlf/JB2diFAf/fR2czYO9A4UTGcsOwppV6W2HVUeho/FPwXoL6DwqA=='
busrouteid = ''

# background 꾸미기
add_bg_from_url()

# 값 입력받기
trynum = 1
busrouteid = st.text_input('please write busRouteId', key = trynum)
# clicked = st.button('click button') # 버튼은 따로 만들지 않는다. press button하면 값이 자동으로 입력되기 때문
trynum += 1
on_enter_pressed(busrouteid)

# # 초기 세션 상태 설정 (최초 실행 시에만 초기화)
# if 'key_pressed' not in st.session_state:
#         st.session_state.key_pressed = False
        
    
# if st.session_state.key_pressed :
#     on_enter_pressed(busrouteid)
    # st.session_state.sync()  # 상태 동기화
    

    


    
    
    
    
    
