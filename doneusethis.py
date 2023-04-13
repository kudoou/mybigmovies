from flask import Flask, request, render_template, jsonify
import requests
from pymongo import MongoClient 

client = MongoClient('mongodb://randhyar955:Ardiansyah955@ac-xeuzkcq-shard-00-00.vr2df0r.mongodb.net:27017,ac-xeuzkcq-shard-00-01.vr2df0r.mongodb.net:27017,ac-xeuzkcq-shard-00-02.vr2df0r.mongodb.net:27017/?ssl=true&replicaSet=atlas-krshns-shard-0&authSource=admin&retryWrites=true&w=majority')

db = client.dbrandhyar955

app = Flask(__name__)

@app.route('/')
def home() :
    render_template('index.html')

#kode servernya
@app.route("/movie", methods=["POST"])
def movie_post():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg':'POST request!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    return jsonify({'msg':'GET request!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)