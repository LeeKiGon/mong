import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb://test:test@13.125.48.221/.dbuserinfo')
# client = MongoClient('localhost', 27017)
db = client.dbuserinfo

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/playlist/detailView?plmSeq=12556', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#body-content > div.songlist-box > div.music-list-wrap > table > tbody > tr')
trs2 = soup.select('#body-content > div.playlist-info > div.info > dl')

base = "https:" #이미지 url에 https:없어서 링크가 안걸려서 추가!!

# db.sleep_list.delete_many({}) ##기존 db데이터 삭제!!
for tr2 in trs2: #앨범 title 정보 크롤링
        make_name = tr2.select_one('dd > a').text
        m_number = tr2.select_one('dd:nth-child(4)').text
        tag = tr2.select_one('dd.tags').text
for tr in trs: #앨범 안 음악 크롤링
        name = tr.select_one('td.info > a.artist.ellipsis').text
        number = tr.select_one('td.number').text[0:2].strip()
        title = tr.select_one('td.info > a.title.ellipsis')['title']
        img = tr.select_one('td > a > img')['src']
        album = tr.select_one('td.info > a.albumtitle.ellipsis').text
        doc = {
            'number': number,
            'name': name,
            'title': title,
            'img_url': base + img,
            'album': album,
            'make_name': make_name,
            'm_umber': m_number,
            'tag': tag
        }
        # db.happy_list.insert_one(doc)    #기쁨
        # db.flutter_list.insert_one(doc)    #설렘
        # db.worry_list.insert_one(doc)      #일/공부
        # db.cvs_list.insert_one(doc)    #기분전환
        # db.sad_list.insert_one(doc)       #슬픔
        # db.comfort_list.insert_one(doc)   #위로
        # db.anger_list.insert_one(doc)     #분노
        # db.eht_list.insert_one(doc)    #지침
        # db.sleep_list.insert_one(doc)      #새벽