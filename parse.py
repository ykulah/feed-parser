from pymongo import MongoClient
import datetime

def insertoMongo( item, dbName ):
    client=MongoClient()
    if(dbName == "Mashable"):
        db=client.mashable
    elif(dbName == "The Next Web"):
        db=client.thenextweb
    else:
        db=client.test_database
    test = db.feed
    test.insert_one(item)
    return

from bs4 import BeautifulSoup
from urllib2 import urlopen

def scrap(url, db):
    #url = "http://feeds.mashable.com/Mashable"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all("item")

    for idx in items: 
        title = idx.title.string
        date = idx.pubdate.string
        url = idx.comments.string
        desc = str(idx.description)
        media = idx.media
        creator = idx.find("dc:creator").string
        rawCategories = idx.find_all("category")
        categories = []

        for val in rawCategories:
            categories.append(val.string)
        if(checkItemExistsInDB(title) == False):
            print "Inserting:%s" % title
            insertoMongo({"title": title, "url": url, "description": desc, "media":media, "creator": creator, "categories": categories}, db)
        else:
            print "Item exists in db"

    return

def checkItemExistsInDB( key ):
    client=MongoClient()
    db=client.mashable
    res = db.feed.find({"title": key})
    if(res.count() > 0):
        return True
    else:
        return False

scrap("http://feeds.mashable.com/Mashable", "Mashable")
scrap("http://feeds2.feedburner.com/thenextweb", "The Next Web")
