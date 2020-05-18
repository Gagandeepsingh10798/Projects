import re
import requests
url = "https://dmoz-odp.org"
page = requests.get(url)    
data = page.text
links_regex = re.compile('<a\s+.*href=[\'"]?([^\'" >]+)', re.IGNORECASE)
links = links_regex.findall(data)
for x in range(len(links)):
    if links[x][0] == '/':
        links[x] = url + links[x] 
print(links)
