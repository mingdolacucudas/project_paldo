from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import certifi
ca = certifi.where()

import time

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

driver = webdriver.Chrome('./chromedriver')

url = "http://ticket.interpark.com/TPGoodsList.asp?Ca=Eve&SubCa=Eve_C&Sort=2"

driver.get(url)
time.sleep(5)

req = driver.page_source
driver.quit()

# 몽고DB 연결
client = MongoClient('mongodb+srv://test:sparta@cluster0.ysqxz.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

def scraping():
    print()


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/seoul')
def seoul():
    return render_template("seoul.html")

# @app.route('/posting', methods=['POST'])
# def posting():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         # 포스팅하기
#             title_receive = request.form['title_give']
#             image_receive = request.form['image_give']
#             where_place_receive = request.form['where_place_give']
#             url_receive = request.form['url_give']
#             all_date_receive = request.form['all_date_give']
#
#             soup = BeautifulSoup(req, 'html.parser')
#
#             places = soup.select("body > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > div.con > div > table > tbody > tr")
#
#             for place in places:
#                 title = place.select_one("td.RKtxt > span > a").text
#                 image = place.select_one("td.RKthumb > a > img")['src']
#                 start_date = place.select_one("td:nth-child(4)").text[0:12]
#                 end_date = place.select_one("td:nth-child(4)").text[-11:]
#                 all_date = (start_date + end_date).strip()
#                 url = place.select_one("td.RKthumb > a")['href']
#                 where_place = place.select_one("td:nth-child(3) > a").text
#                 print(title, image, all_date, url, where_place)
#                 doc = {
#                     "title": title_receive,
#                     "image": image_receive,
#                     "all_date": all_date_receive,
#                     "url": url_receive,
#                     "where_place": where_place_receive
#                 }
#                 db.festivals.insert_one(doc)
#         return jsonify({'msg':'떠나보자!'})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))
#

@app.route("/postlist", methods=["POST"])
def festival_post():
    title_receive = request.form['title_give']
    image_receive = request.form['image_give']
    where_place_receive = request.form['where_place_give']
    url_receive = request.form['url_give']
    all_date_receive = request.form['all_date_give']

    soup = BeautifulSoup(req, 'html.parser')

    places = soup.select("body > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > div.con > div > table > tbody > tr")


    for place in places:
        title = place.select_one("td.RKtxt > span > a").text
        image = place.select_one("td.RKthumb > a > img")['src']
        start_date = place.select_one("td:nth-child(4)").text[0:12]
        end_date = place.select_one("td:nth-child(4)").text[-11:]
        all_date = (start_date + end_date).strip()
        url = place.select_one("td.RKthumb > a")['href']
        where_place = place.select_one("td:nth-child(3) > a").text
        print(title, image, all_date, url, where_place)
        doc = {
            "title": title_receive,
            "image": image_receive,
            "all_date": all_date_receive,
            "url": url_receive,
            "where_place": where_place_receive
        }
        db.festivals.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})


@app.route('/getlist', methods=["GET"])
def festival_get():
    festival_list = list(db.festivals.find({}, {'_id:0'}))
    # return jsonify({'festivals': festival_list})
    return jsonify('index.html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)



# @app.route('/memo', methods=['GET'])
# def listing():
#     articles = list(db.articles.find({}, {'_id': False}))
#     return jsonify({'all_articles':articles})

## API 역할을 하는 부분
# @app.route('/memo', methods=['POST'])
# def saving():
#     url_receive = request.form['url_give']
#     comment_receive = request.form['comment_give']
#
    # 크롤링코드
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get('https://korean.visitkorea.or.kr/list/fes_list.do?choiceTag=&choiceTagId=#0^All^07^All^All^All^1^10^1^#%EC%A0%84%EC%B2%B4', headers=headers)
    #
    # driver = webdriver.Chrome('./chromedriver')
    #
    # soup = BeautifulSoup(data.content, 'html.parser')
    #
    # all_date = soup.find('#contents')
    #
    # print(all_date)


#     title = soup.select_one('meta[property="og:title"]')['content']
#     # contents > div.wrap_contView.clfix > div.box_leftType1 > ul > li:nth-child(1) > div.area_txt > div > a
#     image = soup.select_one('meta[property="og:image"]')['content']
#     # contents > div.wrap_contView.clfix > div.box_leftType1 > ul > li:nth-child(1) > div.photo > a > img
#     # contents > div.wrap_contView.clfix > div.box_leftType1 > ul > li:nth-child(2) > div.photo > a > img
#     desc = soup.select_one('meta[property="og:description"]')['content']
#
    # DB에 저장하는 코드
    # doc = {
    #     'title':title
    # }
    #
    # db.festivals.insert_one(doc)
#
#     return jsonify({'msg':'저장이 완료되었습니다!'})
#
