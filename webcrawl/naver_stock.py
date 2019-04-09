from urllib.request import  urlopen
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/marketindex/'
page = urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

# print(soup.prettify())


all_divs = soup.find_all('span', attrs={'class':'value'})
print(all_divs)
res = [span.string for span in all_divs]
for i in res:
   print(i)