#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 14:56:29 2021

@author: louis
"""
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import random
url = 'https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge'




driver = None

def start_driver(url):
    global driver
    driver = webdriver.Chrome(executable_path='/Users/louis/Desktop/python/paperSearch/chromedriver')
    driver.implicitly_wait(10)
    print("取得網頁...")
    driver.get(url)
    time.sleep(2)

def close_driver():
    global driver
    time.sleep(2)
    driver.quit()
    print("關閉 WebDriver...")

def search_keyword(keyword):
    keywordInput=driver.find_element_by_xpath('//*[@id="ysearchinput0"]')
    keywordInput.send_keys(keyword)
    button=driver.find_element_by_xpath('//*[@id="gs32search"]')
    button.click()
    paper=driver.find_element_by_xpath('//*[@id="tablefmt1"]/tbody/tr[2]/td[3]/div/div[1]/table/tbody/tr[2]/td/a/span/font')
    paper.click()    
    
    
def search_paper():
    html=driver.page_source
    #get_info(html)
    info.append(get_info(html))
    totals=driver.find_element_by_xpath('//*[@id="bodyid"]/form[1]/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]/table/tbody/tr/td[1]/label/font')
    total=re.search('共 [0-9]+ 筆', totals.text).group()
    total=re.search('[0-9]+',total).group()
    total=int(total)
    
    rand=int(random.random()*2+1)
    time.sleep(rand)
    for i in range(1,total):
        nextPage=driver.find_element_by_xpath('//*[@id="bodyid"]/form[1]/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/div[1]/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[4]/input')
        nextPage.click()
        nextPageHtml=driver.page_source
        #get_info(nextPageHtml)   
        time.sleep(rand)
        info.append(get_info(nextPageHtml))
        #time.sleep(rand)
    
    
    
    
def get_info(html):  
    dic={}
    bs = BeautifulSoup(html,'lxml')
    tables = bs.find('table',attrs={'id':'format0_disparea'}).find_all('tr')
    for table in tables[2:-1]:
    #print(table.text)
        key = table.find('th').text
        value = table.find('td').text
        dic[key.replace(':','')]=value
        
    url=bs.find(id='fe_text1')["value"]
    dic['url']=url
    
    try:
        article = bs.find(class_='stdncl2').find('div').text.replace('\n','')
    except:
        article="None"
    finally:
        dic['論文摘要']=article    
    return dic



    
    

    
def save_to_csv(items, file):
    with open(file, "w+", newline="", encoding="utf-8") as fp:  #如果看到亂碼，改成encoding="utf-8"
        writer = csv.DictWriter(fp,fieldnames=['研究生','學門', '學類', '研究生(外文)', '指導教授(外文)', '中文關鍵詞', '論文名稱', '系所名稱', '指導教授', '論文摘要', '論文名稱(外文)', '論文種類', 'url', '校院名稱', '論文出版年','論文頁數', '語文別', '畢業學年度', '學位類別','口試日期', '論文名稱(外文)', '口試委員','口試委員(外文)', '外文關鍵詞','DOI','Facebook'])
        for item in items:
            writer.writerow(item)
    
    
# 主程式開始
if __name__=='__main__':
    info=[]

    start_driver(url)
    search_keyword('棒球')
    search_paper()
    
#save_to_csv(info, 'baseball.csv')
    time.sleep(2)

    close_driver()