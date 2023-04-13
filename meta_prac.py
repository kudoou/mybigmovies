# from http import client
import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, request,render_template,jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Kita perlu menerima informasi url, star, comment dari client, dan menyimpannya untuk digunakan di dalam database. 
# Kita juga bisa menggunakan kode dari file meta_prac.py sebelumnya
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

# client = MongoClient('mongodb://randhyar955:Ardiansyah955@ac-xeuzkcq-shard-00-00.vr2df0r.mongodb.net:27017,ac-xeuzkcq-shard-00-01.vr2df0r.mongodb.net:27017,ac-xeuzkcq-shard-00-02.vr2df0r.mongodb.net:27017/?ssl=true&replicaSet=atlas-krshns-shard-0&authSource=admin&retryWrites=true&w=majority')
# db = client.dbrandhyar955

# app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movie', methods=['POST'])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    #url ='https://www.imdb.com/title/tt6751668/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&pf_rd_r=X9NY2QBF33QPCRSFJBKX&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_30'

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # Masukkan kode disini untu mendapatkan meta tag terlebih dahulu.

    # Kita dapat menggunakan metode objek soup select_oneuntuk mencari serta mengisolasi meta tags dari halaman.
    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

# print(og_image)
# print(og_title)
# print(og_description)

# Mari sekarang kita ekstrak konten sebenarnya dari setiap objek meta tagnya.
    image = og_image['content']
    title = og_title['content']
    description = og_description['content']

    # menampilkan request yang kita minta di index.html dan mepostnya ke mongodb
    doc = {
        'image' : image,
        'title' : title,
        'description' : description,
        'star'  :star_receive,
        'comment' : comment_receive
    }
    db.bigmovie.insert_one(doc)

    return jsonify({'msg' : 'POST request!'})

# memasukkan request yang diminta 
@app.route('/movie', methods=["GET"])
def movie_get():
    # API /movie tidak membutuhkan data apapun dari Client. 
    # Apabila ada request yang dibuat dari client, server akan merespon dengan menanyakan database dari semua data movie, dan mengembalikan list full tersebut kepada client.
    movie_list =list(db.bigmovie.find({},{'_id' : False}))
    return jsonify({'bigmovie' : movie_list})

if __name__ =='__main__' :
    app.run('0.0.0.0', port=5000, debug=True)
    

    # print(image)
    # print(title)
    # print(desc)