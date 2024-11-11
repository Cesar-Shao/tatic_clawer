import pandas as pd
import requests
import urllib.request
from bs4 import BeautifulSoup
import os
from create_json import create_json
from download_pic import download_pic
from tqdm import tqdm
from itertools import count

def create_unique_folder(folder_name):
    # 先尝试创建原始文件夹名称
    try:
        os.mkdir(folder_name)
        return folder_name
    except FileExistsError:
        # 如果已经存在同名文件夹,则尝试添加后缀
        for i in count(1):
            new_folder_name = f"{folder_name}_{i}"
            try:
                os.mkdir(new_folder_name)
                return new_folder_name
            except FileExistsError:
                continue


# 定义目标 URL
url = "https://playbank.fastmodelsports.com/library/basketball/all_tags"


response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")

category_ls=soup.find_all('section',class_="category")

warning_list=[]

for i,category in enumerate(category_ls):
    if not i ==1:
        
        df = pd.DataFrame(columns=['link', 'max_page', 'now_page'])
        
        links = [link['href'] for link in category.find_all('a', href=True)]
        links=[lk for lk in links if lk!='#']

        for lk in tqdm(links):

            name=lk.split('=')[-1].replace('+', '%20')
            lk_url=f"https://playbank.fastmodelsports.com{lk.split('?')[0]}/{name}"
            response = requests.get(lk_url)
            html_content = response.content
            html_soup = BeautifulSoup(html_content, "html.parser")
            search_count=html_soup.find('span',class_="search_count")
            max_page=search_count.text.split('of')[-1].strip()
            
            new_row=pd.Series([f'{lk_url}',max_page,1],index=['link', 'max_page', 'now_page'])
            print(new_row)
            df.loc[len(df)]=new_row
            print(df)

        df.to_csv(f'data_0618/{i}.csv')
        
            