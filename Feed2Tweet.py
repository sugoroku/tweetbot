#! /home/pi/.pyenv/shims/python
#! _*_ coding: utf-8 _*_

import feedparser
import pandas
import time
import datetime
import MySQLdb
import twython

urllist = [
'http://www.zou3.net/php/rss/nikkei2rss.php?head=main',
'http://rss.asahi.com/rss/asahi/newsheadlines.rdf', 
'http://rss.rssad.jp/rss/mainichi/flash.rss',
'https://headlines.yahoo.co.jp/rss/san-dom.xml',
'http://rss.wor.jp/rss1/yomiuri/latestnews.rdf',
'http://www.zou3.net/php/rss/chunichi2rss.php?cat=main',
'http://www.nikkan.co.jp/rss/nksrdf.rdf',
'http://www.security-next.com/feed',
'https://the01.jp/feed/',
'http://feed.rssad.jp/rss/gigazine/rss_2.0',
'http://rss.rssad.jp/rss/itmatmarkit/rss091.xml',
'http://itpro.nikkeibp.co.jp/rss/news.rdf',
'http://www.jpcert.or.jp/rss/jpcert.rdf',
'http://www.ipa.go.jp/security/rss/alert.rdf',
'http://feeds.trendmicro.com/TM-Securityblog/',
'https://feed43.com/0681080852134530.xml'
]

filterlist = ['情報漏洩', '情報漏えい', '情報流出', '不正アクセス', 'ハッキング', '改ざん', '改竄', '不正な通信', 'サイバー攻撃', '標的型', '個人情報']

CONSUMER_KEY    = 'Qhq2HKSNSg8TFNT0gmx2uRdu8'
CONSUMER_SECRET = '09NIhl0goiWNaSO1Z1FRvxzCU5maGuAbm6jygh8JVmjo2Issv'
ACCESS_KEY      = '826728075685568517-1uBnScjmeG9X9kCNfxaBVzrhAKSEhFM'
ACCESS_SECRET   = 'PwIStmNEtgjOwXaL68t09NTlI6AmczvPj9FR7DMPSP8AB'
#tw = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

dt = datetime.datetime.now()

for url in urllist:
  fd = feedparser.parse(url)
  channelurl = fd.feed.link
  channelname = fd.feed.title

  for entry in fd.entries:
    for key in filterlist:
      if key in entry.title :
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
          cursor.execute(
              "insert into incident (link, title, channel, updated) values (%s, %s, %s, %s)", 
              (entry.link, entry.title, channelurl, dt))

          connector.commit()
            
          #print("[***%s***](%s)" % (entry.title, entry.link))
          tweet = "\"" + entry.title + " - " + channelname + "\" " + entry.link
          print(tweet)
          #tw.update_status(status=tweet)

        cursor.close
        connector.close

        break

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

