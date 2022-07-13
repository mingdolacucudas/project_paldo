from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import certifi
ca = certifi.where()

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.ysqxz.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


@app.route('/')
def home():
   return render_template('index_hyemi.html')


@app.route('/secretpage')
def web_list_get():
    all_festivals = list(db.festivals.find({}, {'_id': False}))
    return jsonify({'festivals': all_festivals})

if __name__=='__main__':
    app.run('0.0.0.0',port=5000,debug=True)