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
'http://www.us-cert.gov/ncas/all.xml',
'http://www.kb.cert.org/vulfeed',
'https://www.bleepingcomputer.com/feed/',
'http://thehackernews.com/feeds/posts/default',
'http://feeds.feedburner.com/securityweek',
'http://feeds.arstechnica.com/arstechnica/security',
'https://www.endgame.com/feed.xml',
'https://www.virusbulletin.com/rss',
'http://feeds.trendmicro.com/Anti-MalwareBlog',
'https://www.fireeye.com/blog/threat-research/_jcr_content.feed',
'http://threatpost.com/feed/',
'https://securelist.com/feed/',
'https://www.welivesecurity.com/feed/',
'https://blog.malwarebytes.com/feed/',
'http://blog.shodan.io/rss/',
'https://blog.kryptoslogic.com/feed.xml',
'https://krebsonsecurity.com/feed',
'https://www.grahamcluley.com/feed/',
'https://www.schneier.com/blog/atom.xml',
'https://blog.checkpoint.com/feed/'
]

filterlist = ['APT','DragonOK','Shadowbrokers','SHADOWBROKERS','Lazarus','LAZARUS','Menupass','MENUPASS','Fancy','FANCY','Sofancy','SOFANCY','HIDENCOBRA','HIDEN COBRA','Hiden Cobra','Hidencobra','Group73','Noth Korea','NORTH KOREA','Hacker Group','Olympic','Targeted Attack','Cyber Espionage']
#filterlist2 = ['Example']

CONSUMER_KEY    = 'mkPC1IRfaYG5Lc9iJdFSIB5Pw'
CONSUMER_SECRET = 'e0nC7wl4YjEWxI14xdW7zOhUPgqnw2bZixysHlDBi4A2QNDf1S'
ACCESS_KEY      = '826728075685568517-A5WSi1ymUEWdAPMxKq03WJgV7uQYVlo'
ACCESS_SECRET   = 'aSNt8UfmlwxGUvz60oUkELBgJ8pZrBTvxkcUB2PB67FPN'
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
            (shorturl, entry.title, fd.feed.link, dt))

        connector.commit()
              
        #print("[***%s***](%s)" % (entry.title, entry.link))
        tweet = entry.title + fd.feed.title + "\n" + shorturl 
        print(tweet)
        #tw.update_status(status=tweet)

      cursor.close
      connector.close

      flag = False
      time.sleep(1)

    else:
      continue

print("------------------ %s ---" % (dt))

