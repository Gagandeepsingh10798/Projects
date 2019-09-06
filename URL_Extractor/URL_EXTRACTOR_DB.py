import re
import requests
import pymysql
db = pymysql.connect("localhost","root","","gagan" )
cursor = db.cursor()
# from bs4 import BeautifulSoup
url = "https://dmoz-odp.org"

page = requests.get(url)    
data = page.text
# soup = BeautifulSoup(data, 'html.parser')
# links = []
# for link in soup.find_all('a'):
    # links.append(link.get('href'))
# links = [x for x in links if x is not None]
# for x in range(len(links)):
    # if links[x][0] == '/':
        # links[x] = url + links[x] 

# print(len(links))
links_regex = re.compile('<a\s+.*href=[\'"]?([^\'" >]+)', re.IGNORECASE)
links = links_regex.findall(data)
for x in range(len(links)):
    if links[x][0] == '/':
        links[x] = url + links[x] 
links = links[:50]
values = [[item] for item in links]
cursor.executemany("INSERT INTO GAGAN(LINKS) VALUES (%s)",values)
db.commit()
cursor.close()
db.close()

