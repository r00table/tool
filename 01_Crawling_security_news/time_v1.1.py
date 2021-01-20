from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
from datetime import date, timedelta

def crawling(url):
    res = urlopen(url)
    return BeautifulSoup(res, "html.parser")

def timeCheck(index,soup):
    criterion_Time=datetime.time(7,30) # 7:30 기준으로 뉴스 스크래핑
    today=datetime.datetime.combine(date.today(),criterion_Time)
    yesterday = datetime.datetime.combine((date.today()-timedelta(days=1)),criterion_Time)

    first_news=0; # 첫번째 뉴스
    final_news=0; # 마지막 뉴스

    if index==0:    # boannews
        news_writer=soup.find_all('span',class_='news_writer')
        
        i=0
        while True:
            news_time=datetime.datetime(int(news_writer[i].text[-19:-15]),int(news_writer[i].text[-13:-11]),int(news_writer[i].text[-9:-7]),int(news_writer[i].text[-5:-3]),int(news_writer[i].text[-2:]))
            print(news_time)
            if(today<news_time):
                final_news+=1
            
            if(yesterday>news_time):
                break

            first_news+=1
            i+=1

        return final_news,first_news-1

    elif index==1 or 2: #krcert
        news=soup.find_all('td',class_='gray')

        index=0
        while True:
            news_time_text = news[3*index+2].text
            news_time=datetime.date(int(news_time_text[0:4]),int(news_time_text[5:7]),int(news_time_text[8:10]))

            if(news_time<date.today()-timedelta(days=1)):
                break
            index+=1

        return 0,index-1

    elif index==3:
        news=soup.find_all('span',class_='date')

        index=0
        while True:
            news_time_text = news[index].text
            news_time=datetime.date(int(news_time_text[0:4]),int(news_time_text[5:7]),int(news_time_text[8:10]))

            if(news_time<date.today()-timedelta(days=1)):
                break
            index+=1

        return 0, index-1
        

def getNews(index,soup,start,end):
    file=open(date.today().strftime("%Y-%m-%d")+'.txt','a',encoding='UTF-8')
    
    if index==0:
        news=soup.find_all('div',class_='news_list')
        
        for i in range(start,end+1):
            news_title=news[i].find('span',class_='news_txt').text
            news_link=news[i].find('a')['href']

            file.write("▶ "+news_title+"\n"+url[index]+news_link+"\n")

        file.write("\n")

    elif index==1 or 2:
        news=soup.find_all('td',class_='colTit')

        for i in range(start,end+1):
            news_title=news[i].a.text
            news_link=news[i].a.get('href')

            file.write("▶ "+news_title+"\n"+url[index]+news_link+"\n")

        file.write("\n")

    elif index==3:
        news=soup.select("#secuNewsForm > div > div.listWrap > ul > li > div > a > p.tit")
        news_index=soup.find_all('input',class_='secuNewsSeq')

        for i in range(start,end+1):
            news_title=news[i].get('title')
            news_link='https://www.ahnlab.com/kr/site/securityinfo/secunews/secuNewsView.do?seq='+news_index[i].get('value')

            file.write("▶ "+news_title+"\n"+url[index]+news_link+"\n")

    file.close()


if __name__=="__main__":
    url=['https://www.boannews.com/media/t_list.asp',
         'https://krcert.or.kr/data/secNoticeList.do',
         'https://krcert.or.kr/data/secInfoList.do',
         'https://www.ahnlab.com/kr/site/securityinfo/secunews/secuNewsList.do?menu_dist=1',
         'https://www.dailysecu.com/news/articleList.html','https://www.exploit-db.com']
    
    #for index in range(0,len(url)):
    for index in range(0,3):
        soup = crawling(url[index])
        start,end = timeCheck(index,soup)
        getNews(index,soup,start,end)
