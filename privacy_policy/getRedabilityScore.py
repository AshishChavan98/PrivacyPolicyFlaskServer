from privacy_policy.preprocessing import clean_text_for_scoring
from nltk.tokenize import word_tokenize
from os.path import join, dirname, realpath
import decimal
import textstat
import pickle
import sys

import nltk.data
from bson import decode_all

def getScoreValues(data,mongo):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    res = mongo.db.privacypolicy.find({'name': data['body']})
    res = list(res)[0]

    temp = str(res['file'], 'utf-8')
    text=clean_text_for_scoring(temp)
    wordcount=len(text.split(' '))
    wordinfo=[]
    time=round(wordcount/200,2)
    min,sec=str(time).split(".")
    min=int(min)
    sec=int(sec)
    sec=round(sec*0.60)

    time=str(min)+' minutes and '+str(sec)+' seconds'
    arr=[]
    flesch=textstat.flesch_reading_ease(text)
    flesch_grade=round((150-int(flesch))/10)
    print(flesch_grade)
    arr.append(("Flesch Reading Ease",flesch,flesch_grade))
    smog=round(textstat.smog_index(text),2)
    arr.append(("Smog Index",smog,round(smog)))
    flesch_kincaid=round(textstat.flesch_kincaid_grade(text),2)
    arr.append(("Flesch Kincaid Grade",flesch_kincaid,round(flesch_kincaid)))
    coleman_liau=round(textstat.coleman_liau_index(text),2)
    arr.append(("Coleman Liau Index",coleman_liau,round(coleman_liau)))
    automated_readability=round(textstat.automated_readability_index(text),2)
    arr.append(("Automated Readability Index",automated_readability,round(automated_readability)))
    dale_chall_readability=round(textstat.dale_chall_readability_score(text),2)
    arr.append(("Dale Call Readability Score",dale_chall_readability,round(dale_chall_readability+3)))
    linsear_write=textstat.linsear_write_formula(text)
    arr.append(("Linsear Write Formula",round(linsear_write,2),round(linsear_write)))

    score_info=[[5,'Readable'],[10,'Hard'],[15,'Difficult'],[100,'Very Difficult']]
    fog=textstat.gunning_fog(text)
    fog_grade=''
    for x in score_info:
        if(fog<x[0]):
            fog_grade=x[1]
    
    arr.append(("Gunning Fog",fog,fog_grade))
    
    res={'wordcount':wordcount,'time':time,'difficulty':textstat.difficult_words(text),'standard':flesch_grade,'score':arr}


    return res