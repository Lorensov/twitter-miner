from tweepy.streaming import StreamListener

import threading
import sys
import os
import time
import json

def count_time( threadName, delay, limit):
    count = 0
    while count < limit:
        time.sleep(delay)
        count += 1
        print ("%s: %s" % ( threadName, time.ctime(time.time()) )  )
    print('finished ', threadName)
    #os._exit(0)


class TwitterListener(StreamListener):
    def __init__(self, collection):
        super().__init__()
        self.counter = 0
        self.limit = 100

        self.mongo_collection = collection

        print('Listener Created!')
        
        #using multithread on the object construction
        #threading.Thread(target = count_time,
            #args= ("Time Counter", 1, 5)
        #).start()
        
    def on_data(self,data):
        
        tweet = json.loads(data)

        created_at = tweet["created_at"]
        id_str = tweet["id_str"]
        text = tweet["text"]
        
        user_id = tweet["user"]["id_str"]
        user_name = tweet["user"]["name"]
        screen_name = tweet["user"]["screen_name"]
        user_created_at = tweet["user"]["created_at"]
        
        obj = {
            "message_created_at":time.mktime(time.strptime( created_at,"%a %b %d %H:%M:%S +0000 %Y" )),
            "message_id":id_str,
            "message_text":text,
            "author_user_id": user_id,
            "author_created_at": time.mktime(time.strptime( user_created_at,"%a %b %d %H:%M:%S +0000 %Y" )),
            "author_user_name": user_name,
            "author_screen_name": screen_name
        }
        
        print('🐦', end='')

        tweetind = self.mongo_collection.insert_one(obj).inserted_id
        
        #Tweet limitation counter
        self.counter += 1
        if self.counter < self.limit:
            return True
        else:
            print()
            print('========')
            print('Maximum Tweet limitation reached')
            print('========')
            return False
        
        return True
    
    def on_error(self, status):
        print('error code: ', status)
        return False