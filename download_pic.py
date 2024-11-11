import requests
from bs4 import BeautifulSoup
import json

def download_pic(url,loc):
    # 获取页面内容
    response = requests.get(url)
    html_content = response.content

    # 解析HTML内容
    soup = BeautifulSoup(html_content, "html.parser")

    
    title=soup.find('title')
    if 'sorry, but something went wrong' in title.text:
        print('!!!!!!!!!!!!Server_Error_pic!!!!!!!!!!!!!')
    
    else:
        # 提取页面元素

        # 提取图像链接
        image_links = [img['src'] for img in soup.find_all('img', class_='play_img')]

        #print(len(image_links))
        # 下载图像并保存到文件
        for i, link in enumerate(image_links):
            #print(link)
            response = requests.get(link)
            with open(f'{loc}/image_{i+1}.png', 'wb') as f:
                f.write(response.content)
