#! /home/pi/.pyenv/shims/python
#! _*_ coding: utf-8 _*_

import feedparser
import pandas
import time
import datetime
import MySQLdb
import twython
import json
import requests
import time
import os

#function to shorten the url
def urlShotern(url):
   key=""
   gurl="https://www.googleapis.com/urlshortener/v1/url?key="+key
   data={}
   data['longUrl']=url
   data_json = json.dumps(data)
   headers = {'Content-type': 'application/json'}
   response = requests.post(gurl, data=data_json, headers=headers)
   a=response.json()
   return a['id']

urllist = [
'http://feeds.washingtonpost.com/rss/national',
'http://feeds.reuters.com/reuters/technologyNews'
]

filterlist = ['APT','Hacker Group','targeted attack','Targeted Attack','Cyber Espionage','cyber espionage','hack','hacker','Hacker','spy','Spy','cyber attack']
#filterlist2 = ['Example']

CONSUMER_KEY    = os.environ['TW_SECNEWS_EN_C_KEY']
CONSUMER_SECRET = os.environ['TW_SECNEWS_EN_C_SECRET']
ACCESS_KEY      = os.environ['TW_SECNEWS_EN_A_KEY']
ACCESS_SECRET   = os.environ['TW_SECNEWS_EN_A_SECRET']
tw = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

dt = datetime.datetime.now()

for url in urllist:
  fd = feedparser.parse(url)

  for entry in fd.entries:
    
    flag = False

    for key in filterlist:
      if key in entry.title:
        flag = True

#        for key2 in filterlist2:
#          if key2 in entry.title:
#            flag = False
#            break
#          else:
#            continue

    if flag:
      connector = MySQLdb.connect(
          user = 'root',
          passwd = 'dbmaster',
          host = 'localhost',
          db = 'rss',
          charset = 'utf8',
          use_unicode = True)

      cursor = connector.cursor()

      cursor.execute(
          "select link from secinfo_en where link=%s", (entry.link,))

      if len(cursor.fetchall()) == 0:
        shorturl=urlShotern(entry.link)
        cursor.execute(
            "insert into secinfo_en (link, title, channel, updated) values (%s, %s, %s, %s)", 
            (entry.link, entry.title, fd.feed.link, dt))

        connector.commit()
              
        #print("[***%s***](%s)" % (entry.title, entry.link))
        tweet = entry.title + ": " +fd.feed.title + "\n" + shorturl 
        print(tweet)
        tw.update_status(status=tweet)

      cursor.close
      connector.close

      flag = False
      time.sleep(1)

    else:
      continue

print("------------------ %s ---" % (dt))

