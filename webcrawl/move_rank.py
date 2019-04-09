from selenium import webdriver
from bs4 import BeautifulSoup
ctx = '../crawler/chromedriver'
driver = webdriver.Chrome(ctx)
driver.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
soup = BeautifulSoup(driver.page_source, 'html.parser')
#print(soup.prettify())

all_div = soup.find_all('div', attrs={'class':'tit3'})
res = [div.a.string for div in all_div]
for i in res:
    print(i)