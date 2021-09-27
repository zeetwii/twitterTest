import tweepy
from tweepy import auth # needed for twitter API
import yaml # needed for config
import json # needed for API stuff

import threading # needed for threading
import time # needed for sleep
import sys # needed to exit

import tkinter as tk # needed for dialog
from tkinter import filedialog as fd # needed for dialog

class ReplyListener(tweepy.Stream):
    """
    Class that handles tweepy events
    """
    
    def on_connect(self):
        print("stream connected")
        return super().on_connect()
    
    def on_status(self, status):
        print(status.text)
        
    def on_connection_error(self):
        self.disconnect()
        
    def on_data(self, raw_data):
        print(str(raw_data))
    
    def filter(self, *, follow=None, track=None, locations=None, filter_level=None, languages=None, stall_warnings=False, threaded=False):
        return super().filter(follow=follow, track=track, locations=locations, filter_level=filter_level, languages=languages, stall_warnings=stall_warnings, threaded=threaded)        
    

class ReplyBot:
    """
    Simple python bot to listen to and auto reply to twitter events
    """
    
    def __init__(self, apiKey, apiSecret, accessToken, accessTokenSecret):
        """
        Init method

        Args:
            apiKey ([type]): The API Key to use
            apiSecret ([type]): The API secret to use
            accessToken ([type]): The access token to use
            accessTokenSecret ([type]): The access token secret to use
        """
                 
        self.auth = tweepy.OAuthHandler(apiKey, apiSecret)
        self.auth.set_access_token(accessToken, accessTokenSecret)

        self.api = tweepy.API(self.auth)
        
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.accessToken = accessToken
        self.accessTokenSecret = accessTokenSecret
        
    def validateBot(self):
        """
        Validates that the credientals are working on the bot

        Returns:
            bool: True if valid, False otherwise
        """
        
        try:
            self.api.verify_credentials()
            return True
        except:
            return False
        
    def startStream(self):
        print("Starting stream, press Ctrl + C to exit")
        
        try:
            #self.stream = ReplyBot(self.apiKey, self.apiSecret, self.accessToken, self.accessTokenSecret)
            self.stream = tweepy.Stream(self.apiKey, self.apiSecret, self.accessToken, self.accessTokenSecret)
            self.stream.sample()
            
            #print(self.stream.running)
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            self.stream.disconnect()
            sys.exit(0)
            
    def test(self):
        print(str(self.api.get_direct_messages()))
        target_id = 1288710030880104448
        
        options = [
            {
              "label": "I'm good",
              "description": "It means you're doing good",
              "metadata": "external_id_1"
            },
            {
              "label": "Not so good",
              "description": "It means you're not doing good",
              "metadata": "external_id_2"
            }
          ]
        
        #self.api.send_direct_message(target_id, "Quick reply Test", quick_reply_options=options)
            
        

if __name__ == "__main__":
    
    print("Welcome to ReplyBot, a simple twitter bot to monitor an account and auto reply")
    
    with open("config.yml", "r") as ymlfile:
        CFG = yaml.safe_load(ymlfile)
        apiKey = CFG["twitter"]["API_key"]
        apiSecret = CFG["twitter"]["API_secret"]
        accessToken = CFG["twitter"]["access_token"]
        accessTokenSecret = CFG["twitter"]["access_token_secret"] 
    
    replyBot = ReplyBot(apiKey, apiSecret, accessToken, accessTokenSecret)

    if replyBot.validateBot():
        print("Creds Valid")
    else:
        print("Creds invalid, shutting down")
        sys.exit("Invalid configs")
        
    replyBot.startStream()
    #replyBot.test()
    
    