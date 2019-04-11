import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager,rc
import seaborn as sns
import folium
from sklearn import preprocessing
import googlemaps

ctx ='../data/'
df_crime_police=pd.read_csv(ctx+'crime_police', encoding='UTF-8'
                                     , sep=',')
print(df_crime_police)

df_police = pd.pivot_table(df_crime_police
                          , index='구별'
                          ,aggfunc=np.sum) #aggfunc 은 평균값 리턴

df_police['강간검거율'] = df_police['강간 검거'] /  df_police['강간 발생'] * 100
df_police['강도검거율'] = df_police['강도 검거'] /  df_police['강도 발생'] * 100
df_police['살인검거율'] = df_police['살인 검거'] /  df_police['살인 발생'] * 100
df_police['절도검거율'] = df_police['절도 검거'] /  df_police['절도 발생'] * 100
df_police['폭력검거율'] = df_police['폭력 검거'] /  df_police['폭력 발생'] * 100
df_police.drop(['강간 검거','강도 검거','살인 검거','절도 검거','폭력 검거'],1,inplace=True)

#print(df_police)
ls_rate =['강간검거율','강도검거율','살인검거율','절도검거율','폭력검거율']
for i in ls_rate:
    df_police.loc[df_police[i] > 100,i] = 100



df_police.rename(columns = {'강간 발생':'강간'
                            ,'강도 발생':'강도'
                            ,'살인 발생':'살인'
                            ,'절도 발생':'절도'
                            ,'폭력 발생':'폭력'},inplace=True)
ls_crime = ['강간','강도','살인','절도','폭력']
#print(df_police)
x = df_police[ls_crime].values
min_max_scalar = preprocessing.MinMaxScaler()
"""
스케일링은 선형변환을 적용하여 전체 자료의 분포를
평균 0, 분산 1이 되도록 만드는 과정
"""
x_scaled = min_max_scalar.fit_transform(x.astype(float))
df_police_norm = pd.DataFrame(x_scaled
                              , columns = ls_crime
                              , index = df_police.index)

df_police_norm[ls_rate] = df_police[ls_rate]

df_pop_cctv = pd.read_csv(ctx+'cctv_pop.csv'
                             ,encoding='UTF-8'
                             ,index_col='구별')

df_police_norm[['인구수','CCTV']] = df_pop_cctv[['인구수','소계']]
df_police_norm['범죄'] = np.sum(df_police_norm[ls_crime], axis=1)
df_police_norm['검거'] = np.sum(df_police_norm[ls_rate], axis=1)
#print(df_police_norm.columns)
"""
['강간', '강도', '살인', '절도', '폭력', '강간검거율', '강도검거율', '살인검거율', '절도검거율',
       '폭력검거율', '인구수', 'CCTV', '범죄', '검거']
"""
font = 'C:\Windows\Fonts\malgunbd.ttf'
font_name = font_manager.FontProperties(fname=font).get_name()
#print(font_name)
rc('font'
   ,family=font_name)
sns.pairplot(df_police_norm
             ,vars=['강도','살인','폭력']
             ,kind='reg'
             ,height=3)

sns.pairplot(df_police_norm
             ,x_vars=['인구수','CCTV']
             ,y_vars=['살인','강도']
             ,kind='reg'
             ,height=3)

tmp_max =df_police_norm['검거'].max()
df_police_norm['검거'] = df_police_norm['검거'] / tmp_max * 100
df_police_norm_sort = df_police_norm\
    .sort_values(by='검거'
                 ,ascending=False)
plt.figure(figsize=(10,10))
sns.heatmap(df_police_norm_sort[ls_rate]
            , annot=True
            ,fmt='f'
            ,linewidths=5)
plt.title('범죄 검거 비율')


ls_crime =['강간','강도','살인','절도','폭력','범죄']
df_police_norm['범죄'] = df_police_norm['범죄'] /5
df_police_norm_sort = df_police_norm.sort_values(by='범죄'
                                                 ,ascending=False)
plt.figure(figsize=(10,10))
sns.heatmap(df_police_norm_sort[ls_crime]
            ,annot=True
            ,fmt='f'
            ,linewidths=5)
plt.title('범죄 비율')
df_police_norm.to_csv(ctx+'police_norm.csv'
                        ,sep=','
                       ,encoding='UTF-8')
