from flask import Flask, render_template,request, jsonify
from nltk.tokenize import word_tokenize
from flask_pymongo import PyMongo
from flask_cors import CORS
from privacy_policy.getPrivacyPolicy import getData
from privacy_policy.getRedabilityScore import getScoreValues
import pickle


app=Flask(__name__)
cors = CORS(app)
app.config.from_pyfile('production.cfg')
try:
    app.config.from_pyfile('development.cfg')
except FileNotFoundError:
    pass

mongo=PyMongo(app)

@app.route('/')
def home():
    return render_template("./index.html",title="HOME PAGE")

@app.route('/ml',methods=['POST'])
def index():
    labels=['children_sent','collectionway_sent' ,'contact_sent' ,'cookies_sent','infocollect_sent', 'others' ,'purpose_sent' ,'security_sent','thirdparty_infoshare_sent']
    print("\nRequest\n",str(request.get_data()))
    print("\nRequest\n",request)
    print("request headers",request.headers)
    feature_array=request.get_json()
    res=getData(feature_array,mongo)
    return jsonify(res)

@app.route('/getdata',methods=['POST'])
def getdata():
    print("\nRequest\n",str(request.get_data()))

@app.route('/readability',methods=['POST'])
def getScore():
    req=request.get_json()
    res=getScoreValues(req,mongo)
    return jsonify(res)

@app.route('/getsites',methods=['GET','POST'])
def getsites():
    res=mongo.db.privacypolicy.find({},{'name':1,'_id':False})
    site_list=[]
    for x in list(res):
        site_list.append((x['name']))
    print(site_list[0:2])
    return jsonify(site_list)




