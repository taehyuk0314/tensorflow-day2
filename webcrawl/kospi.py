from urllib.request import  urlopen
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/sise/'
page = urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

all_span = soup.find_all('span', attrs={'id': 'KOSPI_now'})
all_span2 = soup.find_all('span', attrs={'id': 'time1'})

print(all_span)
print(all_span2)

res = [span.string for span in all_span]
for i in res:
   print(i)