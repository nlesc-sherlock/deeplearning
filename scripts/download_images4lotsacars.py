import sqlite3
import wget

db = "../../results/lotsacars.db"
conn = sqlite3.connect(db)
curs = conn.cursor()

#f = open("urls_for_lotsacars.txt")
i=0
for make in open('../../Models/lotsacars-20151202-170935-03d3/labels.txt', 'r').readlines():
    r=curs.execute("select url from images where make = ? limit 5", (unicode(make[:-1]),)).fetchall()
    for x in r:
        try:
            url = x[0]
            filename = wget.download(url)
            print filename,i
        except:
            pass
    i+=1

