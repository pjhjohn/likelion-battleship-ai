from urllib import urlopen
from bs4 import BeautifulSoup

data = urlopen('http://www.huffingtonpost.kr/2014/07/17').read()
soup = BeautifulSoup(data)


news_list = soup.select('#news_entries h3 a')
for i in news_list:
	data = urlopen(i['href']).read()
	soup = BeautifulSoup(data)
	print soup.select('h1.title')[0].text