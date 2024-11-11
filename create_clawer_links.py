
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

        links = [link['href'] for link in category.find_all('a', href=True)]
        links=[lk for lk in links if lk!='#']

        print(links)

        
        
        with open(f'data_0618/{i}_links.txt','w') as f:
            for lk in tqdm(links):
                f.write(f"{lk}\n")
                
                '''
                lk_name=lk.split('=')[-1]
                os.mkdir(f'{i}/{lk_name}')
                
                for page_num in range(1,9999):
                    name=lk.split('=')[-1].replace('+', '%20')
                    lk_url=f"https://playbank.fastmodelsports.com{lk.split('?')[0]}/{name}?page={page_num}"
                    try:
                        response = requests.get(lk_url)
                        html_content = response.content
                        html_soup = BeautifulSoup(html_content, "html.parser")
                        html_ls = [html['href'] for html in html_soup.find_all('a',href=True)]
                        html_ls=[html for html in html_ls if html!='#' and len(html.split('/'))>4]
                        html_ls=[html for html in html_ls if html.split('/')[4].isdigit()]
                        html_ls=list(set(html_ls))
                        
                        if not len(html_ls)==0:
                            print('-----')
                            print('html_ls:',len(html_ls))
                            
                            
                            for html in html_ls:
                                print('-----')
                                print(html)
                                
                                html_name=html.split('/')[-1]
                                create_unique_folder(f'{i}/{lk_name}/{html_name}')
                                html_url="https://playbank.fastmodelsports.com"+html
                                
                                
                                #测试服务器是否正常
                                
                                
                                warning_name=create_json(html_url,f'{i}/{lk_name}/{html_name}')
                                download_pic(html_url,f'{i}/{lk_name}/{html_name}')
                                if len(warning_name)>0:
                                    warning_list.append(warning_name)
                                    with open('warning_file.txt', 'a') as file:
                                        file.write('\n' + f'{warning_name}')
                        
                        else:
                            print(f'达到最大页码{page_num}')
                            break
                    except Exception as e:
                        # 将异常信息写入 txt 文件
                        error_file = "error.txt"
                        with open(error_file, "a") as f:
                            f.write(f"Error occurred: {str(e)}\n")
                            f.write("------------------------------\n")
                        
                    print('warning_list:',warning_list)'''