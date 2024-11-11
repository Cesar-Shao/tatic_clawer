
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
        os.makedirs(folder_name)
        return folder_name
    except FileExistsError:
        # 如果已经存在同名文件夹,则尝试添加后缀
        for i in count(1):
            new_folder_name = f"{folder_name}_{i}"
            try:
                os.makedirs(new_folder_name)
                return new_folder_name
            except FileExistsError:
                continue

def crawler(tag,lk):

    warning_list=[]
    lk_name=lk.split('?')[0].split('/')[-1].replace('%20','_')
    
    try:
        response = requests.get(lk)
        html_content = response.content
        
        html_soup = BeautifulSoup(html_content, "html.parser")
        html_ls = [html['href'] for html in html_soup.find_all('a',href=True)]
        html_ls=[html for html in html_ls if html!='#' and len(html.split('/'))>4]
        html_ls=[html for html in html_ls if html.split('/')[4].isdigit()]
        html_ls=list(set(html_ls))
        
        print('-----')
        print(f'tactics_in_page:',len(html_ls))
        
        
        for html in html_ls:
            print('-----')
            print(html)
            html_name=html.split('/')[-1].replace('%20','_')
            create_unique_folder(f'./data_0624/{tag}/{lk_name}/{html_name}')
            html_url="https://playbank.fastmodelsports.com"+html
            
            
            warning_res=create_json(html_url,f'data_0624/{tag}/{lk_name}/{html_name}')
            download_pic(html_url,f'data_0624/{tag}/{lk_name}/{html_name}')
            for warning_i in warning_res:
                warning_lk=warning_res[warning_i]
                if len(warning_lk)!= 0:
                    with open(f'data_0624/{tag}/{lk_name}/{warning_i}_warning_file.txt', 'a') as file:
                        file.write('\n' + f'{warning_lk}')
        
    except Exception as e:
        # 将异常信息写入 txt 文件
        with open(f'data_0624/{tag}/{lk_name}/error.txt', "a") as f:
            f.write(f"{tag}/{lk_name}/{html_name}\n")
            f.write(f"Error occurred: {str(e)}\n")
            f.write("------------------------------\n")
    
    return True




