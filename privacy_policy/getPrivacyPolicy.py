from privacy_policy.preprocessing import clean_text
from nltk.tokenize import word_tokenize
from os.path import join, dirname, realpath
import pickle
import sys

import nltk.data
from bson import decode_all


def getData(data, mongo):
    print('In getData functiondfgsdfgdfg',file=sys.stderr)
    res = mongo.db.privacypolicy.find({'name': data['body']})
    print('datebase response',res)
    res = list(res)[0]

    # print('value of return Hello'+returnHello())
    result={}
    arr=[]
    if(len(res) == 0):
        print('Not Found')
    else:
        arr = runModel(res)
        print(arr,flush=True)
        result={'name':res['name'],'date':res['date'],'output':arr}
        return result
        


def runModel(res):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    labels = ['children_sent', 'collectionway_sent', 'contact_sent', 'cookies_sent','infocollect_sent', 'others', 'purpose_sent', 'security_sent', 'thirdparty_infoshare_sent']
    UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/model.pkl')
    model = pickle.load(open(UPLOADS_PATH, "rb"))
    temp = str(res['file'], 'utf-8')
    initial_sentence_list = tokenizer.tokenize(temp)
    sentence_list = [clean_text(x) for x in initial_sentence_list]
    print('In run model')
    output=[]
    for sentence in sentence_list:
        featuresets = find_features(sentence)
        prediction = model.classify(featuresets)
        # print(str(labels[prediction]))
        output.append(str(labels[prediction]))
    
    res=zip(initial_sentence_list,output)
    # print(dict(res))
    ret=list(res)
    return ret

def load_word_features():
    UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/word_features')
    with open(UPLOADS_PATH, 'rb') as f:
        word_features = pickle.load(f)
    
    return word_features

def load_messages():
    UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/messages')
    with open(UPLOADS_PATH, 'rb') as f:
        messages = pickle.load(f)
    
    return messages

def find_features(message):
    word_features=load_word_features()
    words = word_tokenize(message)
    features = {}
    for word in word_features:
        features[word] = (word in words)

    return features

def returnHello():
    return 'hello'