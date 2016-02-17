import urllib2
import json
import sqlite3

keyBing = 'MeAuVCPpeae5Lflf9dmJD0EU3Pe/KHH/tlbyTijGDik'        # get Bing key from: https://datamarket.azure.com/account/keys
credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds
top = 50
offset = 51

def search_bing(keyword):
    searchString = '%27' + keyword + '%27'
    url = 'https://api.datamarket.azure.com/Bing/Search/Image?' + \
          'Query=%s&$top=%d&$skip=%d&$format=json' % (searchString, top, offset)

    request = urllib2.Request(url)
    request.add_header('Authorization', credentialBing)
    requestOpener = urllib2.build_opener()
    response = requestOpener.open(request) 
    results = json.load(response)
    return results


db = "../results/carmodels.db"
conn = sqlite3.connect(db)
curs = conn.cursor()
#curs.execute("CREATE TABLE images (make TEXT, model TEXT, url TEXT, title TEXT)")
#conn.commit()

i=0
for row in open('../results/carmodels.csv', 'r').readlines()[0:]:
    i+=1
    make,model,frequence = row[:-1].split(',')
    if make == "make": # header line
        continue
    makestr = make.replace(" ","%20")
    modelstr = model.replace(" ","%20")
    query = "%22"+makestr+"%20"+modelstr+"%22%20%22te%20koop%22"
    print i, query
    result = search_bing(query)
    for r in result['d']['results']:
        curs.execute("INSERT INTO images (make,model,url,title) VALUES (?,?,?,?)", (
            unicode(make), unicode(model), unicode(r['MediaUrl']), unicode(r['Title'])))
    conn.commit()
    
