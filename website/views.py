
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core import serializers

import os
import requests
import csv
import twitter
import json

import tweepy
from textblob import TextBlob



### For Logging purposes to console.. disable in production
# import logging
# logger = logging.getLogger(__name__)

def twitterHero(data,size):

    consumer_key = "Y5XFRuxBWJ1btZU6xu93IGCGF"
    consumer_secret = "lbCJ8qP79EKqlzkrsGvegUbE7k3rm2JZDYqX3TbbcPaj6ZVfkh"
    access_token = "1032328800321777664-uvHGxG2TwP110GSWlLdYOv483fqNNX"
    access_token_secret = "NiCzXy0cQ3QzeYDpq539lSXQ4jFzQEmYINEgu7N8gjndW"

    

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)


    api=tweepy.API(auth)

    # print "IN TWITTER HERO"


    


    S=[]
    counter=[0,0,0] # positive, negative, neutral
    for tweet in tweepy.Cursor(api.search, q=data, rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(size):
        # logger.log(100,tweet)  # MASSIVE DATA DUMP for debugging
        analysis=TextBlob(tweet.text)

        # print analysis.sentiment.polarity
        if analysis.sentiment.polarity > 0:
            res='positive'
            counter[0]+=1
        elif analysis.sentiment.polarity == 0:
            res='neutral'
            counter[2]+=1
        else:
            res='negative'
            counter[1]+=1
        S.append((tweet.text,analysis.sentiment,res,tweet.user.name,tweet.user.profile_image_url_https,tweet.user.screen_name))
    # print counter
    positivePer=(counter[0]%size)*4
    negativePer=(counter[1]%size)*4
    neutralPer=(counter[2]%size)*4

    # print counter[0]
    # print (counter[0]%size)*4
    
    S.append((positivePer,negativePer,neutralPer))
    # print S[0]
    # print S[0][2]
    # print S[0][0]
    # print S[0][3]
    return S






def index(request):
    return render(request,'website/home.html',{})









def form_data(request):
    try:
        data=request.POST['q']
        size=int(request.POST['size'])
    except MultiValueDictKeyError:
        data='data science'
        size=50
    if data=='':
        data='data science'
    S=twitterHero(data,size)
    # logger.log(100,"Called function.")
    posPer,negPer,ntrPer=S[-1][0],S[-1][1],S[-1][2]

    # print "IN FORM_DATA FUNCTION"
    
    del S[-1]
       
    return render(request,"website/index.html",{'data':S,'search':data,'posPer':posPer,'negPer':negPer,"ntrPer":ntrPer})















def fetch_keyword(request):


    CONSUMER_KEY = "Y5XFRuxBWJ1btZU6xu93IGCGF"
    CONSUMER_SECRET = "lbCJ8qP79EKqlzkrsGvegUbE7k3rm2JZDYqX3TbbcPaj6ZVfkh"
    OAUTH_TOKEN = "1032328800321777664-uvHGxG2TwP110GSWlLdYOv483fqNNX"
    OAUTH_TOKEN_SECRET = "NiCzXy0cQ3QzeYDpq539lSXQ4jFzQEmYINEgu7N8gjndW"

    auth = twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)

    twitter_api=twitter.Twitter(auth=auth)


    # print "IN FETCH_KEYWORD FUNCTION"


    



     
    WORLD_WOE_ID = 1
    US_WOE_ID = 23424977
    IN_WOE_ID = 23424848

    # world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    # us_trends = twitter_api.trends.place(_id=US_WOE_ID)
    in_trends = twitter_api.trends.place(_id=IN_WOE_ID)

    # print world_trends[0][0]
    # print
    # print us_trends


    # print json.dumps(world_trends[0]["trends"], indent=1)
    print
    # print json.dumps(us_trends, indent=1)

    # for tname in world_trends[0]["trends"]:
    #     print tname["name"]
    print 
    print "============================="
    print "TRENDS IN INDIA IS HERE "
    print "============================="





    for tname in in_trends[0]["trends"]:
        R = twitterHero(tname["name"],20)
        # print tname["name"]

        return HttpResponse({tname["name"], '\n' +R[0][3] + "---tweeted---" + R[0][0], '\n' +"*************************"}, content_type='application/json')

       
        
        
        
       
    