from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import certifi
ca = certifi.where()

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.9qdtqor.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


@app.route('/')
def home():
   return render_template('index_hyemi.html')


@app.route("/postList", methods=["POST"])
def festival_post():
    url_receive = request.form["url"]

    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    places = soup.select("body > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > div.con > div > table > tbody > tr")
    array = []

    for place in places:
        title = place.select_one("td.RKtxt > span > a").text
        tag = place.select_one("td.RKthumb > a > img")
        start_date = place.select_one("td:nth-child(4)").text[0:12]
        end_date = place.select_one("td:nth-child(4)").text[-11:]
        date = (start_date + end_date).strip()
        a_url = place.select_one("td.RKthumb > a")['href']
        where_place = place.select_one("td:nth-child(3) > a").text

        if tag is not None:
            image = tag['src']
        else:
            image = "NONE"

        array.append({'title': title, 'image': image, 'date': date, 'a_url': a_url, 'where_place': where_place})

    return jsonify({'result': 'success', 'list': array})


if __name__=='__main__':
    app.run('0.0.0.0',port=5000,debug=True)