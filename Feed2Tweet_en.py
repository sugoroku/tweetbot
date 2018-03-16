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
   key=os.environ['GOOGLE_API_KEY']
   gurl="https://www.googleapis.com/urlshortener/v1/url?key="+key
   data={}
   data['longUrl']=url
   data_json = json.dumps(data)
   headers = {'Content-type': 'application/json'}
   response = requests.post(gurl, data=data_json, headers=headers)
   a=response.json()
   return a['id']

urllist = [
'http://www.us-cert.gov/ncas/all.xml',
'http://www.kb.cert.org/vulfeed',
'https://www.bleepingcomputer.com/feed/',
'http://thehackernews.com/feeds/posts/default',
'https://www.darkreading.com/rss_simple.asp',
'http://feeds.feedburner.com/securityweek',
'http://feeds.arstechnica.com/arstechnica/security',
'https://www.endgame.com/feed.xml',
'https://www.virusbulletin.com/rss',
'http://feeds.trendmicro.com/Anti-MalwareBlog',
'https://www.fireeye.com/blog/threat-research/_jcr_content.feed',
'http://threatpost.com/feed/',
'https://securelist.com/feed/',
'https://api.connect.symantec.com/rss/v1/blogs/rss.xml',
'https://securingtomorrow.mcafee.com/feed/',
'https://www.welivesecurity.com/feed/',
'https://blog.malwarebytes.com/feed/',
'https://www.crowdstrike.com/blog/feed',
'https://www.anomali.com/site/blog-rss',
'http://feeds.feedburner.com/PaloAltoNetworks',
'http://blog.shodan.io/rss/',
'https://feeds2.feedburner.com/asert',
'http://feeds.feedburner.com/TheAkamaiBlog',
'https://blog.kryptoslogic.com/feed.xml',
'https://krebsonsecurity.com/feed',
'https://www.grahamcluley.com/feed/',
'https://www.schneier.com/blog/atom.xml',
'https://blog.checkpoint.com/feed/'
]

filterlist = ['APT','DragonOK','Shadowbrokers','SHADOWBROKERS','Lazarus','LAZARUS','Menupass','MENUPASS','Fancy','FANCY','Sofacy','SOFACY','HIDENCOBRA','HIDEN COBRA','Hiden Cobra','Hidencobra','Group73','North Korea','NORTH KOREA','Hacker Group','Olympic','Targeted Attack','SWIFT','Swift','espionage','Espionage','Threat Group','sofancy','Group123','Bear','NSA']

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

