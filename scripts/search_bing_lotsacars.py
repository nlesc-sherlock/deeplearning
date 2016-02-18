import urllib2
import json
import sqlite3

keyBing = 'MeAuVCPpeae5Lflf9dmJD0EU3Pe/KHH/tlbyTijGDik'        # get Bing key from: https://datamarket.azure.com/account/keys
credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds
top = 50
offset = 0

def search_bing(keyword):
    searchString = '%27' + keyword + '%27'
    url = 'https://api.datamarket.azure.com/Bing/Search/Image?' + \
          'Query=%s&$top=%d&$skip=%d&$format=json' % (searchString, top, offset)
    print url

    request = urllib2.Request(url)
    request.add_header('Authorization', credentialBing)
    requestOpener = urllib2.build_opener()
    response = requestOpener.open(request) 
    results = json.load(response)
    print results
    return results


db = "../results/lotsacars.db"
conn = sqlite3.connect(db)
curs = conn.cursor()
curs.execute("CREATE TABLE images (make TEXT, url TEXT, title TEXT)")
conn.commit()

i=0
for make in open('../Models/lotsacars-20151202-170935-03d3/labels.txt', 'r').readlines():
    i+=1
    query = make[:-1]+"%20occasion"
    print i, query
    result = search_bing(query)
    for r in result['d']['results']:
        curs.execute("INSERT INTO images (make,url,title) VALUES (?,?,?)", (
            unicode(make[:-1]), unicode(r['MediaUrl']), unicode(r['Title'])))
    conn.commit()
    
