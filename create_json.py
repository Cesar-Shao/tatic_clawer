import requests
from bs4 import BeautifulSoup
import json

def create_json(url,loc):
    warning_name=''
    data={"title":'',
          "website":f'{url}',
        "abstract":'',
        "description":[],
        "labels":[]}

    warning_res={
        "title":'',
        "abstract":'',
        "description":'',
        "labels":''
    }

    # 获取页面内容
    response = requests.get(url)
    html_content = response.content

    # 解析HTML内容
    soup = BeautifulSoup(html_content, "html.parser")

    title=soup.find('title')
    if 'sorry, but something went wrong' in title.text:
        print('!!!!!!!!!!!!Server_Error!!!!!!!!!!!!!')
        warning_name=loc+'/'+data['title']
        warning_res['title']=warning_name
        return warning_res

    # 提取文字描述
    description_elements = soup.find_all('div', class_='play description')
    abstract_elements=soup.find_all('div', class_='override-gray-background')
    title_elements=soup.find_all('title')
    ul_tag = soup.find('ul', class_='tags')
    label_elements=ul_tag.find_all('a',class_='tag action-button--with-text')

    data['title']=title_elements[0].text.replace(' - FastModel Sports','')

    if not len(abstract_elements)==1:
        print('!!!!!!!!!Error:abstract_lenth != 1!!!!!!')
        warning_name=loc+'/'+data['title']
        warning_res['abstract']=warning_name
        return warning_res
    #elif len(abstract_elements)!=0 :
    #0624改
    else:
        try:
            data['abstract']=abstract_elements[0].find('p').text.strip()
        except:
            print('!!!!!!!!abstract_warning!!!!!!!!!!')
            warning_name=loc+'/'+data['title']
            warning_res['abstract']=warning_name


    if not len(description_elements)==1:
        print('!!!!!!!!!Error:description_lenth != 1!!!!!!')
        warning_name=loc+'/'+data['title']
        warning_res['description']=warning_name
        return warning_res
    else:
        try:
            ul = description_elements[0].find('ul')
            all_li=ul.find_all('li')
            all_text=[i for i in all_li]
            #0618_修改解决ul中没有<p>的情况
            #all_text=[i.find_all('p') for i in all_li]
            text_res=[]
            for text_set_n in all_text:
                text=''
                for temp_text in text_set_n:
                    text= text+temp_text.text.strip()
                text_res.append(text)
            data['description']=text_res
        except:
            print('!!!!!!!!description_warning!!!!!!!!!!')
            warning_name=loc+'/'+data['title']
            warning_res['description']=warning_name
            try:
                one_text=description_elements[0].find('p').text.strip()
                data['description']=[one_text]
            except:
                print('!!!!!!!!description_warning_2!!!!!!!!!!')
                warning_res['description']=warning_name

    if len(label_elements)<1:
        print('!!!!!!!!!Error:label_lenth = 0!!!!!!')
        warning_name=loc+'/'+data['title']
        warning_res['labels']=warning_name
        return warning_res
    else:
        try:
            labels=[element.text.strip() for element in label_elements]
            data['labels']=labels
        except:
            print('!!!!!!!!labels_warning!!!!!!!!!!')
            warning_name=loc+'/'+data['title']
            warning_res['labels']=warning_name


    with open(f"{loc}/data.json", "w") as f:
        json.dump(data, f, indent=4)

    return warning_res