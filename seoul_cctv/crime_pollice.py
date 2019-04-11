import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from sklearn import preprocessing
import  googlemaps

ctx = '../data/'
df_crime = pd.read_csv(ctx+'crime_in_Seoul.csv', encoding='euc-kr'
                                                , thousands=',')
#df_json = pd.read_excel(ctx+'geo_simple.json',)

gmaps_key = "AIzaSyDBBxV_6m_wxhh9P-23y-3-jJHklZBiAIY"
gmaps = googlemaps.Client(key=gmaps_key)
#print(df_crime)
# print(gmaps.geocode('서울중부경찰서',language='ko'))
"""
['관서명', '살인 발생', '살인 검거', '강도 발생', '강도 검거', '강간 발생', '강간 검거', '절도 발생',
       '절도 검거', '폭력 발생', '폭력 검거']
"""
station_name = []
for name in df_crime['관서명']:
    station_name.append('서울'+str(name[:-1])+'경찰서')

#print(station_name)

station_addr = []
station_lat = [] # 위도
station_lng = [] # 경도
for name in station_name:
    tmp = gmaps.geocode(name, language='ko')
    station_addr.append(tmp[0].get('formatted_address'))
    tmp_loc = tmp[0].get('geometry')
    station_lat.append(tmp_loc['location']['lat'])
    station_lng.append(tmp_loc['location']['lng'])
    #print(name + '--->'+tmp[0].get('formatted_address'))
station_name
station_lat
station_lng

gu_names =[]
for name in station_addr:
    tmp = name.split()
    tmp_gu = [gu for gu in tmp if gu[-1] == '구'][0]
    #print('--->'+tmp_gu)
    gu_names.append(tmp_gu)

#print(len(df_crime['관서명']))
df_crime['구별'] = gu_names
#print(df_crime) # 31개의 관서명 존재

#금천경찰서는 관악구 위체 있어서 금천서를 찾아서 금천구라고 수동작업

df_crime.loc[df_crime['관서명']=='금천서',['구별']] = '금천구'
df_crime.loc[df_crime['관서명']=='강서서',['구별']] = '강서구'
#print(df_crime)

df_crime.to_csv(ctx+'crime_police', sep=',',encoding='UTF-8')

