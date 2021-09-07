import tweepy
from tweepy import auth # needed for twitter API
import yaml # needed for config
import json # needed for API stuff

import threading # needed for threading
import time # needed for sleep
import sys # needed to exit

import tkinter as tk # needed for dialog
from tkinter import filedialog as fd # needed for dialog

class rbStreamListener(tweepy.StreamListener):
    """
    Class that handles tweepy events
    """
    
    def on_status(self, status):
        print(status.text)
        
    

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
        
        try:
            self.stream = tweepy.Stream(auth= self.api.auth, listener= rbStreamListener)
            self.stream.filter(follow=[str(self.api.me().id)])
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            sys.exit(0)
            
        

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

    
    #api.update_status("Test Tweet")
    
    #test = api.list_direct_messages(5)
    #print(api.me().id)
    
    #print(test)
    