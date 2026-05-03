import os
import requests
import certifi
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from snownlp import SnowNLP

load_dotenv()

def get_all_news():
    news_list = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    
    # 第一抓：UDN
    res_udn = requests.get("https://udn.com/news/breaknews/1", headers=headers)
    soup_udn = BeautifulSoup(res_udn.text, 'html.parser')
    for item in soup_udn.select('.story-list__text')[:10]:
        a = item.select_one('a')
        if a:
            news_list.append({
                "title": a.get('title') or a.text.strip(),
                "url": "https://udn.com" + a['href'] if not a['href'].startswith('http') else a['href'],
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "source": "聯合新聞網"
            })

    # 第二抓：中時
    res_ct = requests.get("https://www.chinatimes.com/hotnews/?chdtv", headers=headers)
    soup_ct = BeautifulSoup(res_ct.text, 'html.parser')
    for a in soup_ct.select('.vertical-list h3 a')[:5]:
        news_list.append({
            "title": a.text.strip(),
            "url": "https://www.chinatimes.com" + a['href'],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "source": "中時新聞網"
        })
    return news_list

def save_and_verify(news_data):
    client = MongoClient(os.getenv('MONGO_URI'), tlsCAFile=certifi.where())
    db = client['Project0']
    col = db['NewsCrawler']
    
    col.delete_many({})
    col.insert_many(news_data)
    print(f"成功存入 {len(news_data)} 筆新聞")
    
    print("\n--- 資料庫讀回驗證 ---")
    for doc in col.find().limit(3):
        sentiment_label = "正向" if doc['polarity'] == 1 else "負向" if doc['polarity'] == -1 else "中立"
        print(f"[{doc['source']}] ({sentiment_label}) {doc['title']}")
    
    stats = list(col.aggregate([{"$group": {"_id": "$polarity", "count": {"$sum": 1}}}]))
    print("\n情緒分布統計 (-1負, 0中, 1正)：", stats)

if __name__ == "__main__":
    data = get_all_news()

    for news in data:
        s = SnowNLP(news['title'])
        score = s.sentiments
        
        if score < 1/3:
            polarity = -1
        elif score < 2/3:
            polarity = 0
        else:
            polarity = 1
        
        news['sentiment_score'] = score
        news['polarity'] = polarity

    save_and_verify(data)