from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib2 import urlopen

def parseMashable(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all("item")

    client = MongoClient()
    for idx in items: 
        title = idx.title.string
        date = idx.pubdate.string
        url = idx.comments.string
        desc = str(idx.description)
        media = idx.media
        creator = idx.find("dc:creator").string
        
        if(client.mashable.feed.find({"title": title}).count() == 0):
            item = {"title": title, "url": url, "description": desc, "media":media, "creator": creator}
            client.mashable.feed.insert_one(item)
            print "[Mashable]Added: %s" % title

    return

def parseMilliyet(url):
    
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all("item")

    client = MongoClient()
    for i in items:
        title = i.title.string
        date = i.pubdate.string
        url = i.guid.string
        description = str(i.description)    
        
        if(client.milliyet.gundem.find({"title": title}).count() == 0):
            item = {"title": title, "date": date, "url":url, "description": description}
            client.milliyet.gundem.insert_one(item)
            print "[Milliyet]Added: %s" % title
    return


def parseNTV(url):
    
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all("entry")

    client = MongoClient()
    for i in items:
        title = i.title.string
        date = i.published.string
        url = i.id.string
        description = str(i.content)    

        if(client.ntv.gundem.find({"title": title}).count() == 0):
            item = {"title": title, "date": date, "url":url, "description": description}
            client.ntv.gundem.insert_one(item)
            print "[NTV]Added: %s" % title
    return


parseMashable("http://feeds.mashable.com/Mashable")
parseMilliyet("http://www.milliyet.com.tr/rss/rssNew/gundemRss.xml")
parseNTV("http://www.ntv.com.tr/gundem.rss")
