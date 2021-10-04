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
        
    #def on_data(self, raw_data):
    #    print(str(raw_data))
    
    def sample(self):
        return super().sample()

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

        try:
            self.api.verify_credentials()
            self.id = str(self.api.verify_credentials().id)
            self.name = self.api.verify_credentials().name
            print(f"Credentials loaded, running as: {self.name}")
        except:
            print("Error, credentials not valid")
        
    def startStream(self):
        print("Starting stream, press Ctrl + C to exit")
        
        try:
            self.stream = ReplyListener(self.apiKey, self.apiSecret, self.accessToken, self.accessTokenSecret)
            #self.stream = tweepy.Stream(self.apiKey, self.apiSecret, self.accessToken, self.accessTokenSecret)
            
            
            #self.stream.sample()
            self.stream.filter(follow=[self.id])
            
            #print(self.stream.running)
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            self.stream.disconnect()
            sys.exit(0)

    def dmRead(self):

        messageList = self.api.get_direct_messages()

        for msg in messageList:
            #print(str(msg.message_create))
            #self.api.delete_direct_message(msg.id)
            if msg.message_create['sender_id'] == self.id : # check to see if DM is from us
                print("its me")
                # Go ahead and delete the message, we don't care about our messages
                self.api.delete_direct_message(msg.id)
            else:
                print("not me")
            
                try:
                    print(str(msg.message_create['message_data']['quick_reply_response']['metadata']))
                    self.api.send_direct_message(msg.message_create['sender_id'], f"Thank you for selecting option {str(msg.message_create['message_data']['quick_reply_response']['metadata'])}")
                    self.api.delete_direct_message(msg.id)
                except KeyError:
                    print("not a quick repsonse, sending starting message")

                    options = [
                        {
                        "label": "I'm good",
                        "description": "It means you're doing good",
                        "metadata": "1"
                        },
                        {
                        "label": "Not so good",
                        "description": "It means you're not doing good",
                        "metadata": "2"
                        }
                    ]
                    
                    self.api.send_direct_message(msg.message_create['sender_id'], "Quick reply Test", quick_reply_options=options)
                    self.api.delete_direct_message(msg.id)


            
    def test(self):
        #print(str(self.api.get_direct_messages()))
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
        
        self.api.send_direct_message(target_id, "Quick reply Test", quick_reply_options=options)
            
        

if __name__ == "__main__":
    
    print("Welcome to ReplyBot, a simple twitter bot to monitor an account and auto reply")
    
    with open("config.yml", "r") as ymlfile:
        CFG = yaml.safe_load(ymlfile)
        apiKey = CFG["twitter"]["API_key"]
        apiSecret = CFG["twitter"]["API_secret"]
        accessToken = CFG["twitter"]["access_token"]
        accessTokenSecret = CFG["twitter"]["access_token_secret"] 
    
    replyBot = ReplyBot(apiKey, apiSecret, accessToken, accessTokenSecret)
        
    #replyBot.startStream()
    #replyBot.test()
    replyBot.dmRead()
    
    