#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 22:02:07 2017

@author: silviofischer
"""

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

#Variables that contains the user credentials to access Twitter API 
consumer_key= 'Ohf3Mqdww0aENBXyUAEbYbev3'
consumer_secret= 'm0BXG5Z1m6Sw0p8nYAFgMIItEnadydIfalh6QrffjZ2PF0EnbB'

access_token='847859417701904385-0do5uFOZySHKMieSxNyNPm13KALX1Dw'
access_token_secret='viQnv7V95K8QGlkaZa6yAbv27UI9efZNTvegerACIAHwY'



#This is a basic listener that just prints received tweets and their sentiments.
class StreamListener(StreamListener):

    def on_status(self, status):
        print(status.text)
        blob = TextBlob(status.text)
        sent = blob.sentiment
        print(sent)
        print()
        
    def on_error(self, status_code):
        if status_code == 420:
            return False


if __name__ == '__main__':

    #This handles Twitter authentification and the connection to Twitter Streaming API
    l = StreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filters Twitter Streams to capture data by the keywords: 'brexit'
    subject = 'brexit'
    stream.filter(track=[subject])
