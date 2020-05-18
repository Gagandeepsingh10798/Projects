from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
def scrape(data):
    #flipkart data
    
    #for product images
    driver=webdriver.Chrome(executable_path=r"C:\Users\BROTEK\Desktop\webScraper\chromedriver.exe")
    driver.get('https://www.flipkart.com/search?q='+data)
    time.sleep(5)
    hands=BeautifulSoup(driver.page_source,'html.parser')
    images = hands.find_all("div", {"class": "_3BTv9X"})
    driver.quit()
    #for product images
    
    
    flipkartData = requests.get('https://www.flipkart.com/search?q='+data)
    soup = BeautifulSoup(flipkartData.content, 'html5lib') 
    productNames = soup.find_all("div", {"class": "_3wU53n"})
    prices = soup.find_all("div", {"class": "_1vC4OE _2rQ-NK"})
    Descriptions = soup.find_all("ul", {"class": "vFw0gD"})
    
    flipkartProductList = []
    if(len(prices)<3):
        for x in range(0,len(prices)):
            prices[x] = prices[x].get_text()
            desc = []
            for li in Descriptions[x].findAll('li'):
                desc.append(li.get_text())
            flipkartProductList.append({'productName' : productNames[x].get_text(),
                                        'productprice': prices[x][1:len(prices[x])],
                                        'productDesc': desc,
                                        'image':str(images[x].img['src'])})
    else:
        for x in range(0,3):
            prices[x] = prices[x].get_text()
            desc = []
            for li in Descriptions[x].findAll('li'):
                desc.append(li.get_text())
            flipkartProductList.append({'productName' : productNames[x].get_text(),
                                        'productprice': prices[x][1:len(prices[x])],
                                        'productDesc': desc,
                                        'image':str(images[x].img['src'])})
    
    #flipkart data
    
    #paytmMall data
    
    PaytmMallData = requests.get('https://paytmmall.com/shop/search?q='+data+'&from=organic')
    soup = BeautifulSoup(PaytmMallData.content, 'html5lib') 
    productNames = soup.find_all("div", {"class": "UGUy"})
    prices = soup.find_all("div", {"class": "_1kMS"})
    images = soup.find_all("div", {"class": "_3nWP"})
    links = soup.find_all('a', {"class":"_8vVO"})[0:3]
    Descriptions = []
    for a in links:
        link = requests.get('https://paytmmall.com'+str(a['href']))
        souper = BeautifulSoup(link.text, 'html5lib')
        Descriptions.append(souper.find_all("ul", {"class": "aile"})[0])
        
    paytmMallProductList = []
    if(len(prices)<3):
        for x in range(0,len(prices)):
            prices[x] = prices[x].get_text()
            desc = []
            for li in Descriptions[x].findAll('li'):
                desc.append(li.get_text())
            paytmMallProductList.append({'productName' : productNames[x].get_text(),
                                        'productprice': prices[x],
                                        'productDesc': desc,
                                        'image':str(images[x].img['src'])})
    else:
        for x in range(0,3):
            prices[x] = prices[x].get_text()
            desc = []
            for li in Descriptions[x].findAll('li'):
                desc.append(li.get_text())
            paytmMallProductList.append({'productName' : productNames[x].get_text(),
                                        'productprice': prices[x],
                                        'productDesc': desc,
                                        'image':str(images[x].img['src'])})
            
    # #paytmMall data
    
    jsonObject = {'query':data, 'productList':{
    'flipkart':flipkartProductList,
    'paytmMall':paytmMallProductList}}
    
    return jsonObject