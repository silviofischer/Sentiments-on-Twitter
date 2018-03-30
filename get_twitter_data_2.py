# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 09:34:16 2017

@author: Rodolfo Benedech
"""
import threading
import sys
import numpy
import os
import time


# für die Kalkulation
from scipy.stats.stats import pearsonr

# Tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

# GUI
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject, pyqtSignal

"""
NOTIZEN
30.04.2017: 1051: Das GUI muss nicht als Thread abgehen, aber alles andere.
"""

class Twitter_Stream():
    # Login-Data for Twitter
    consumer_key= 'Ohf3Mqdww0aENBXyUAEbYbev3'
    consumer_secret= 'm0BXG5Z1m6Sw0p8nYAFgMIItEnadydIfalh6QrffjZ2PF0EnbB'
    access_token='847859417701904385-0do5uFOZySHKMieSxNyNPm13KALX1Dw'
    access_token_secret='viQnv7V95K8QGlkaZa6yAbv27UI9efZNTvegerACIAHwY'
    
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
        ende = 600
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
        ende = 600
        
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
    
    def AnalysisSentimentalis(eingabe):
        blob = TextBlob(IntakeData.TweetText(eingabe[0:600]))
        sentimental = str(blob.sentiment)
        return sentimental      
        
    def NumPolarity(eingabe):
        start = 0
        ende = 0
        for x in range(0,len(eingabe)):
            if eingabe [x-9:x]=="polarity=":
#                print(eingabe)
                start = x
#                print ("Start:",start)
        for y in range(start,len(eingabe)):
#            print(eingabe[y-5:y])
            if eingabe [y-5:y]==", sub":
                ende = y-5
#                print("Ende:",ende)
        polarity = float(eingabe[start:ende])
        return polarity

    def NumSubjektivity(eingabe):
        start = 0
        ende = 0
        for x in range(0,len(eingabe)):
            if eingabe [x-13:x]=="subjectivity=":
                start = x
#            print ("Start:",start)
        for y in range(start,len(eingabe)):
#        print(eingabe[y-5:y])
            if eingabe [y]==")":
                ende = y
#            print("Ende:",ende)
        subjectivity = float(eingabe[start:ende])
        return subjectivity
    
class SaveData():
    def __init__(self):
        self.SubjektVektor = []
        self.PolarVektor = []
        self.TweetData = []
        self.TweetTime = []
        self.TweetText = []
        
    def EntrSubjektivityVektor(self,eingabe):
        self.SubjektVektor.append(eingabe)
        
    def EntrPolarityVektor(self,eingabe):
        self.PolarVektor.append(eingabe)
        
    def EntrTweetData(self,eingabe):
        time.sleep(0.02)
        self.TweetData.append(eingabe)

    def EntrTweetTime(self,eingabe):
        self.TweetTime.append(eingabe)

    def EntrTweetText(self,eingabe):
        self.TweetText.append(eingabe)
        print(eingabe)

    # Returns polarity and subjectivity in Tupel
    def ReturnVektors(self):
        return self.PolarVektor,self.SubjektVektor
    
    def ReturnTweetData(self,eingabe):
        return self.TweetData[eingabe]
    
    def ReturnAmountTweets(self):
        laenge = len(self.TweetData)
        return laenge
    
    def ReturnTweet(self,eingabe):
        return self.TweetText[eingabe]
    

class Kalkulation():
    def Korrelation(TTPEL):
        polar,subje = TTPEL
#        print(polar)
#        print(subje)
        corr = pearsonr(polar,subje)
        return corr
    
    def Standardabweichung(tupel):
        polar,subje = tupel
        

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowTitle("Hauptprogramm")

# FENSTERDIMENSION
        breite = 800
        hohe = 600
        #self.resize(dimension,dimension)
        self.setMinimumSize(breite,hohe)
        self.setMaximumSize(breite,hohe) 

# LABELS
        massiv = "Text 1"
        massiv2 = "Text 2"

        self.label1 = QLabel("Startwert")         
        self.label1.setWordWrap(True)
        self.label1.setAlignment(Qt.AlignTop)
        self.label1.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.label1, 0, 0)

        self.label2 = QLabel(massiv)        
        self.label2.setWordWrap(True)
        self.label2.setAlignment(Qt.AlignTop)
        self.label2.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.label2, 1, 0)        
        
        self.label2 = QLabel(massiv2)
        self.label2.setWordWrap(True)
        self.label2.setAlignment(Qt.AlignTop)
        self.label2.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.label2, 1, 1, 2, 2)
#        label = QLabel("POSITION 0 2 2 1")
#        label.setWordWrap(True)
#        layout.addWidget(label, 0, 2, 2, 1)

       
# BUTTON

        self.buttonGroup1 = QButtonGroup()
        self.buttonGroup1.setExclusive(False)
#        self.buttonGroup1.buttonClicked[int].connect(self.on_button_clicked)        

        self.button1 = QPushButton("Plus 100")
        self.buttonGroup1.addButton(self.button1, 1)
        layout.addWidget(self.button1,3,0)

        self.button2 = QPushButton("Button 2")
        self.buttonGroup1.addButton(self.button2, 2)
        layout.addWidget(self.button2,3,1,1,2)       
  
# RADIO BUTTON
        self.radiobutton = QRadioButton("Brazil")
        self.radiobutton.setChecked(True)
        self.radiobutton.country = "Brazil"
        self.radiobutton.toggled.connect(self.on_radio_button_toggled)
        layout.addWidget(self.radiobutton, 4, 0)

        self.radiobutton = QRadioButton("Argentina")
        self.radiobutton.country = "Argentina"
        self.radiobutton.toggled.connect(self.on_radio_button_toggled)
        layout.addWidget(self.radiobutton, 4, 1)

        self.radiobutton = QRadioButton("Ecuador")
        self.radiobutton.country = "Ecuador"
        self.radiobutton.toggled.connect(self.on_radio_button_toggled)
        layout.addWidget(self.radiobutton, 4, 2)

# CHECK - BOX
        self.checkbox1 = QCheckBox("Kestrel")
        self.checkbox1.setChecked(True)
        self.checkbox1.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.checkbox1, 5, 0)
        self.checkbox2 = QCheckBox("Sparrowhawk")
        self.checkbox2.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.checkbox2, 5, 1)
        self.checkbox3 = QCheckBox("Hobby")
        self.checkbox3.toggled.connect(self.checkbox_toggled)
        layout.addWidget(self.checkbox3, 5, 2)

# LINE EDIT
        self.lineedit = QLineEdit()
        self.lineedit.returnPressed.connect(self.return_pressed)
        layout.addWidget(self.lineedit, 6,0,1,3)

# LCD - SHOW
#        self.lcdshow = QLCDNumber()
#        self.lcdshow.display(str(DoThis.getValue()))
#        layout.addWidget(self.lcdshow,7,0,1,3)

## FUNKTIONEN ##

# BUTTON - Funktion

#    def on_button_clicked(self,buttonNumber):
#        if buttonNumber==1:
#            GuiMemory.increase100()
#        else:
#            GuiMemory.increaseValue()
#        self.label1.setText(str(GuiMemory.getValue()))
#        
    
# Aktualisierung Label 1

    def changedValue(self):
        self.label1.setText("Anzahl Tweets: "+str(GuiMemories.returnTweetAmount()))
        
        
# RADIOBUTTON - Funktion
        
    def on_radio_button_toggled(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
            print("Selected country is %s" % (radiobutton.country))

# CHECKBOX - Funktion

    def checkbox_toggled(self):
        selected = []
        
        if self.checkbox1.isChecked():
            selected.append("Kestrel")
        if self.checkbox2.isChecked():
            selected.append("Sparrowhawk")
        if self.checkbox3.isChecked():
            selected.append("Hobby")
        print("Selected: %s" % (" ".join(selected)))

# LINE-EDIT - Funktion
    def return_pressed(self):
        print(self.lineedit.text())
        print(type(self.lineedit.text()))
        eingabe = self.lineedit.text()
        while True:
            try:
                eingabe = float(eingabe)
            except ValueError:
                print("STOP")
                break
            print(eingabe,type(eingabe))
            break
        
# RECHENFUNKTIONEN

class GuiMemory():
    def __init__(self):
        self.value = 0
        self.increaseInput = 0
        self.TweetAmount = 0
        self.LastTweet = "noch kein Tweet vorhanden"

    def increaseTweetAmount(self,eingang):
        self.TweetAmount = eingang
        
    def lastTweet(self,eingang):
        self.LastTweet = eingang
        
    def increaseValue(self):
        self.value = self.value+1
        
    def increaseInput(self):
        zahl = zahl
        self.value=self.value+zahl                    
        
    def increase100(self):
        self.value = self.value+100
        
    def showTest(self):
        print("TestShowTest")
        
    def drucken(self):
        print(self.value)
        
    def getValue(self):
        return self.value
    
    def returnTweetAmount(self):
        return self.TweetAmount
    
    def returnLastTweet(self):
        return self.LastTweet


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        Save.EntrTweetData(data)
        print("In Twitterlistener: Neuer Tweet")
        """Funktioniert"""
#        print(Save.ReturnTweetData())
        return True

#        print(IntakeData.Datum(data[0:700]))
#        print(IntakeData.TweetText(data[0:700]))
#        print(IntakeData.Writer(data[0:800]))
#        Save.EntrPolarityVektor(IntakeData.NumPolarity(sentimental))
#        Save.EntrSubjektivityVektor(IntakeData.NumSubjektivity(sentimental))
#        print(Save.ReturnVektors())
#        print(Kalkulation.Korrelation(Save.ReturnVektors()))
#        print("Polarity:",IntakeData.NumPolarity(sentimental))
#        print("Subjectivity:",IntakeData.NumSubjektivity(sentimental))
#        print(sentimental)
#        print(type(sentimental))

class TwitterApp(threading.Thread):
    def run(self):
        Listener = StdOutListener()
        auth = OAuthHandler(Twitter_Stream.consumer_key, Twitter_Stream.consumer_secret)
        auth.set_access_token(Twitter_Stream.access_token, Twitter_Stream.access_token_secret)
        stream = Stream(auth, Listener)
        stream.filter(track=['swiss'])

# Datenabspreicherung und Verwertung
class Verarbeitungsprozess(threading.Thread):
    
    def run(self):
        counter = 0   
        loopcounter = 0
        
#        while True:
#            print ("Type RAMT: "+str(type(Save.ReturnAmountTweets()))+"\nRAMT:")
#            print (Save.ReturnAmountTweets())
#            print ("Type Counter: "+str(type(counter))+"\nCounter:")
#            print(counter)
#            time.sleep(0.5)
#        
        while True:
#            if int(Save.ReturnAmountTweets()) == int(counter):
##                print("Same")
            if int(Save.ReturnAmountTweets()) != int(counter):
                print(Save.ReturnAmountTweets())
                time.sleep(0.15)
                print(counter)
                print(Use.GetTheTweet(counter))

#                print("Len:"+str(Save.ReturnAmountTweets()))
#                print("Counter: "+str(counter))
#                data = Save.ReturnTweetData(counter)
#                tweet = IntakeData.TweetText(data)
#                Save.EntrTweetText(tweet)
#                print(Save.ReturnTweetData(counter)) 
#                """FUNKTIONIERT """ 
##                print(tweet)
                counter = counter+1 

                # Der Counter wird bei einem neuen Tweet um 1 höher gesetzt um auszugleichen


#                print(Use.DataToUse(counter))
#                print(Use.GetTheTweet(counter))

                
                
#                print("Verarbeiter startet: "+str(counter)+" Lauf")
#                GuiMemories.increaseTweetAmount(Save.ReturnAmountTweets())
#                print("Anzahl Tweets in GM: "+str(GuiMemories.returnTweetAmount()))
#                counter = Save.ReturnAmountTweets()
#                screen.changedValue()
                
            loopcounter = loopcounter+1
            if counter == 1000:
                break
            elif loopcounter == 1000:
                break

"""Die Ausgabe ist permanent None, Returnwert von DataToUse prüfen"""
                
class UsableData():
    def GetTheTweet(self,eingabe):
        data = Save.ReturnTweetData(eingabe)
        tweet = IntakeData.TweetText(data)
        return tweet

    def DataToUse(self,eingabe):
        if eingabe != 0:
            Save.EntrTweetText(IntakeData.TweetText(Save.ReturnTweetData(eingabe)))
            text = Save.ReturnTweet(eingabe)
            return text

#Vorher
Save = SaveData()
GuiMemories = GuiMemory()
Use = UsableData()


Verarb = Verarbeitungsprozess()           
Verarb.start()

TwitterStart = TwitterApp()
TwitterStart.start()

# GUI
GuiMemories = GuiMemory()
app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())


#if __name__ == '__main__':
#    
##    install = PackageInstall()
##    install.install()
#
#    Save = SaveData()
#    l = StdOutListener()
#    
#    #This handles Twitter authetification and the connection to Twitter Streaming API
#    auth = OAuthHandler(Twitter_Stream.consumer_key, Twitter_Stream.consumer_secret)
#    auth.set_access_token(Twitter_Stream.access_token, Twitter_Stream.access_token_secret)
#    stream = Stream(auth, l)
#
#    #This line filter Twitter Streams to capture data by the keywords: 'Brexit'
#    stream.filter(track=['brexit'])
