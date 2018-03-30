# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:12:22 2017

@author: Rodolfo Benedech; silviofischer
"""

#Variables that contains the user credentials to access Twitter API 
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import os
import time

class PackageInstall():
    
    def install(self):
        estimatedTime = 30
        PackageInstall.tweeperInstall(self)
        for x in range(int(estimatedTime)):
            zeit = estimatedTime-x
            print(zeit,"Sekunden bis zur nächsten Installation")
            time.sleep(1)              
        PackageInstall.textblobInstall(self)
    
    def tweeperInstall(self):
        os.system("pip install tweepy")
        
    def textblobInstall(self):
        os.system("pip install textblob")

class Twitter_Stream():
    # Login-Data for Twitter
    consumer_key= 'Ohf3Mqdww0aENBXyUAEbYbev3'
    consumer_secret= 'm0BXG5Z1m6Sw0p8nYAFgMIItEnadydIfalh6QrffjZ2PF0EnbB'
    access_token='847859417701904385-0do5uFOZySHKMieSxNyNPm13KALX1Dw'
    access_token_secret='viQnv7V95K8QGlkaZa6yAbv27UI9efZNTvegerACIAHwY'    
    
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(IntakeData.Datum(data[0:700]))
        print(IntakeData.TweetText(data[0:700]))
        print(IntakeData.Writer(data[0:800]))
        blob = TextBlob(IntakeData.TweetText(data[0:700]))
        sentimental = str(blob.sentiment)
        print(sentimental)
        return True

class IntakeData():
       
    def Datum(eingabe):
        Date = eingabe[15:45]
        Teiler = Date.split(" ")
        DatumDict = {"Tag":"X","Monat":"","Tagesnummer":0,"Zeit":"","unwichtig":"","Jahr":0}
        DatumDictKeys = list(DatumDict.keys())
        for x in range(0,len(Teiler)):
            DatumDict[DatumDictKeys[x]] = Teiler[x]
        return DatumDict
 
    def TweetText(eingabe):
        start = 0
        ende = 700
        for x in range(0,len(eingabe)):
#            print (eingabe[x-8:x])
            if eingabe [x-8:x]=='"text":"':
                start = x       
        for y in range(start,len(eingabe)):
            if eingabe [y-3:y]=='","':
                if y < ende:
                    ende = y-3
        tweet = eingabe[start:ende]
        return tweet
    
    def Writer(eingabe):
        start = 0
        ende = 800
        
        for x in range(0,len(eingabe)):
#            print (eingabe[x-15:x])
            if eingabe [x-15:x]=='"screen_name":"':
                start = x       
        for y in range(start,len(eingabe)):
            if eingabe [y-3:y]=='","':
                if y < ende:
                    ende = y-3
        WriterName = eingabe[start:ende]
        return WriterName

if __name__ == '__main__':
    
#    install = PackageInstall()
#    install.install()

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(Twitter_Stream.consumer_key, Twitter_Stream.consumer_secret)
    auth.set_access_token(Twitter_Stream.access_token, Twitter_Stream.access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'Brexit'
    stream.filter(track=['brexit'])
