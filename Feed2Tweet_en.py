#! /home/pi/.pyenv/shims/python
#! _*_ coding: utf-8 _*_

import feedparser
import pandas
import time
import datetime
import MySQLdb
import twython

urllist = [
'http://www.us-cert.gov/ncas/all.xml',
'https//www.veracode.com/blog/feed',
'http://www.kb.cert.org/vulfeed',
'http://blog.shodan.io/rss/',
'http://feeds.feedburner.com/securityweek',
'http://feeds.arstechnica.com/arstechnica/security',
'https://www.welivesecurity.com/feed/',
'https://blog.malwarebytes.com/feed/',
'http://thehackernews.com/feeds/posts/default',
'https://krebsonsecurity.com/feed',
'https://www.grahamcluley.com/feed/',
'https://www.schneier.com/blog/atom.xml',
'http://feeds.feedburner.com/TroyHunt',
'https://blog.kryptoslogic.com/feed.xml',
'http://www.malware-traffic-analysis.net/blog-entries.rss',
'https://www.fireeye.com/blog/threat-research/_jcr_content.feed',
'http://feeds.trendmicro.com/Anti-MalwareBlog'
]

filterlist = ['Malvertis','malvertis','Ransomeware','ransomeware','Ransomworm','ramsomworm','Malware','malware','RootKit','rootkit','Backdoor','backdoor','RAT','ShadowBrokers','Exploit','exploit','Hacking Group','SQL Injection','Vulnerab','Wikileaks','Man-in-the-Middle','NSA','DDoS','Worm','worm','CIA','hijack','Hijack','0-day','Zero-day','zero-day','Malicious','malicious']
filterlist2 = ['Example']

CONSUMER_KEY    = ''
CONSUMER_SECRET = ''
ACCESS_KEY      = ''
ACCESS_SECRET   = ''
tw = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

dt = datetime.datetime.now()

for url in urllist:
  fd = feedparser.parse(url)

  for entry in fd.entries:
    
    flag = False

    for key in filterlist:
      if key in entry.title:
        flag = True

        for key2 in filterlist2:
          if key2 in entry.title:
            flag = False
            break
          else:
            continue

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
        cursor.execute(
            "insert into secinfo_en (link, title, channel, updated) values (%s, %s, %s, %s)", 
            (entry.link, entry.title, fd.feed.link, dt))

        connector.commit()
              
        #print("[***%s***](%s)" % (entry.title, entry.link))
        tweet = entry.title + ": " + fd.feed.title + "\n" + entry.link
        print(tweet)
        tw.update_status(status=tweet)

      cursor.close
      connector.close

      flag = False

    else:
      continue

print("------------------ %s ---" % (dt))

