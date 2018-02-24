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
'http://www3.nhk.or.jp/rss/news/cat0.xml',
'http://www.zou3.net/php/rss/nikkei2rss.php?head=main',
'http://rss.rssad.jp/rss/mainichi/flash.rss',
'https://headlines.yahoo.co.jp/rss/san-dom.xml',
'http://rss.wor.jp/rss1/yomiuri/latestnews.rdf',
'http://www.zou3.net/php/rss/chunichi2rss.php?cat=main',
'http://www.nikkan.co.jp/rss/nksrdf.rdf',
'http://www.jiji.com/rss/ranking.rdf',
'http://feeds.cnn.co.jp/rss/cnn/cnn.rdf',
'http://feeds.japan.cnet.com/rss/cnet/all.rdf',
'http://www.security-next.com/feed',
'https://the01.jp/feed/',
'http://feed.rssad.jp/rss/gigazine/rss_2.0',
'http://rss.rssad.jp/rss/itmatmarkit/rss091.xml',
'http://rss.rssad.jp/rss/itmnews/2.0/news_bursts.xml',
'http://itpro.nikkeibp.co.jp/rss/news.rdf',
'http://feeds.japan.zdnet.com/rss/zdnet/all.rdf',
'http://www.ipa.go.jp/security/rss/alert.rdf',
'http://feeds.trendmicro.com/TM-Securityblog/',
'https://feed43.com/0681080852134530.xml'
]

#'http://rss.asahi.com/rss/asahi/newsheadlines.rdf', 
#'http://www.jpcert.or.jp/rss/jpcert.rdf',

filterlist = ['情報漏洩', '情報漏えい', '情報流出', '不正アクセス', 'ハッキング', '改ざん', '改竄', '不正な通信', 'サイバー攻撃', '標的型', '個人情報','DDoS', 'マイナンバー', '顧客情報', '不審な通信',  'なりすまし', 'インシデント', 'ハッカー', 'サイバーテロ','サイト攻撃', 'フィッシングサイト', 'フィッシング攻撃', 'メール誤送信','ハッキング', '脆弱性', 'ランサム', 'アドレス流出', 'バックドア', 'マルウェア','トロジャン']
filterlist2 = ['PR：', 'AD：', 'PR: ','AD: ']

CONSUMER_KEY    = os.environ['TW_SECNEWS_JP_C_KEY']
CONSUMER_SECRET = os.environ['TW_SECNEWS_JP_C_SECRET']
ACCESS_KEY      = os.environ['TW_SECNEWS_JP_A_KEY']
ACCESS_SECRET   = os.environ['TW_SECNEWS_JP_A_SECRET']
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
          "select link from incident where link=%s", (entry.link,))

      if len(cursor.fetchall()) == 0:
        shorturl=urlShotern(entry.link)
        cursor.execute(
            "insert into incident (link, title, channel, updated) values (%s, %s, %s, %s)", 
            (shorturl, entry.title, fd.feed.link, dt))

        connector.commit()
              
        #print("[***%s***](%s)" % (entry.title, entry.link))
        tweet = entry.title + ": " + fd.feed.title + "\n" + shorturl 
        print(tweet)
        tw.update_status(status=tweet)

      cursor.close
      connector.close

      flag = False

    else:
      continue

print("------------------ %s ---" % (dt))

# Security Corporation
#  JPCERT
#   http://www.jpcert.or.jp/rss/jpcert.rdf
#  IPA
#   http://www.ipa.go.jp/security/rss/alert.rdf

# Security Vender
#  TrendMicro
#   http://feeds.trendmicro.com/TM-Securityblog/
#  CISCO TAROS
#   https://feed43.com/0681080852134530.xml

# IT media
#  Security-Next
#   http://www.security-next.com/feed
#  The Zero/One
#   https://the01.jp/feed/ 
#  @IT market
#   http://rss.rssad.jp/rss/itmatmarkit/rss091.xml
#  GIGAZINE
#   http://feed.rssad.jp/rss/gigazine/rss_2.0
#  ITpro
#   http://itpro.nikkeibp.co.jp/rss/news.rdf
#  ZD Net Japan
#   http://feeds.japan.zdnet.com/rss/zdnet/all.rdf

# News Paper
#  Asashi
#   http://rss.asahi.com/rss/asahi/newsheadlines.rdf
#   https://headlines.yahoo.co.jp/rss/asahik-dom.xml
#  Mainichi
#   http://rss.rssad.jp/rss/mainichi/flash.rss
#  Chyunichi
#   http://www.zou3.net/php/rss/chunichi2rss.php?cat=main
#  Yomiuri
#   http://rss.wor.jp/rss1/yomiuri/latestnews.rdf
#  Sankei
#   https://headlines.yahoo.co.jp/rss/san-dom.xml
#   http://rss.wor.jp/rss1/sankei/flash.rdf
#  Nikkei
#   http://www.zou3.net/php/rss/nikkei2rss.php?head=main
#  Nikkankougyou
#   http://www.nikkan.co.jp/rss/nksrdf.rdf

# Terevision Station
#  NHK
#   http://www3.nhk.or.jp/rss/news/cat0.xml

