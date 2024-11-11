import pandas as pd
from crawler import crawler
from tqdm import tqdm
tag=0
work_df=pd.read_csv(f'data_0624/{tag}.csv')

for row_num,row in work_df.iterrows():
    
    if row['now_page']!=row['max_page']:
        start_page= row['now_page'] if row['now_page']==1 else row['now_page']+1
        for page_num in tqdm(range(start_page,row['max_page']+1)):
            row_link=row['link']
            crawl_link=f'{row_link}?page={page_num}'
            over=crawler(tag,crawl_link)
            if(over):
                work_df.loc[row_num,'now_page']=page_num
                work_df.to_csv(f'data_0624/{tag}.csv')
                print(f'{crawl_link}_page{page_num} downloaded !!!!! ')
                print('+++++++++++++++++++++++++++++++')