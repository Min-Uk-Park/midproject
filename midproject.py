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

sys.path.append('c:\lang_practice\Python_practice')
url = 'http://ws.bus.go.kr/api/rest/buspos/getBusPosByRouteSt'

servicekey = '0OhBU7ZCGIobDVKDeBJDpmDRqK3IRNF6jlf/JB2diFAf/fR2czYO9A4UTGcsOwppV6W2HVUeho/FPwXoL6DwqA=='
busrouteid = ''



def on_enter_pressed(busid) :
    # if 정보를 입력하기 전이라면 ~ 
    if (busid == "") :
        st.write('please write data and press or click the enter')

    # if 정보를 입력하고 해당 정보가 옳은 정보라면 ~ 
    elif (re.match('\d{9}',busid)) :
        
        # 입력 정보가 맞다면 'Success' 문구를 띄운다!
        with st.spinner('Wait for it'):
            time.sleep(5)
        
        st.success("Success")
        
        params ={'serviceKey' : servicekey, 'busRouteId' : busid, 'startOrd' : '1', 'endOrd' : '10'}

        response = requests.get(url, params=params)


        soup = bs(response.text,'lxml-xml')
        st.title('서울시 버스위치 정보 조회')



        # write 즉, 출력내용 구하기 : 버스 번호, 좌표값

        lon = float(soup.find('tmX').text)
        lat = float(soup.find('tmY').text)
        busnum = soup.find('plainNo').text

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
        # st.map(data=data_dict)
        # st.session_state.sync()

    # if 만약 입력된 정보가 틀리다면 Error msg를 띄운다.
    else :
        with st.spinner('Wait for it'):
            time.sleep(5)
        
        st.error('Error! please write bus number again')

def main() :
    
    
    # 값 입력받기
    trynum = 1
    busrouteid = st.text_input('please write busRouteId', key = trynum)
    # clicked = st.button('click button') # 버튼은 따로 만들지 않는다. press button하면 값이 자동으로 입력되기 때문
    trynum += 1
    on_enter_pressed(busrouteid)

    # # 초기 세션 상태 설정 (최초 실행 시에만 초기화)
    if 'key_pressed' not in st.session_state:
            st.session_state.key_pressed = False
            
        
    # if st.session_state.key_pressed :
    #     on_enter_pressed(busrouteid)
        # st.session_state.sync()  # 상태 동기화
        
if __name__ == "__main__":
    # 메인 함수 실행
    main()
    
    
    
    
    
    
    # ----------------------------
    
    
    
    
    
