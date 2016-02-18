import sqlite3
db = "../results/lotsacars.db"
conn = sqlite3.connect(db)
curs = conn.cursor()

#f = open("urls_for_lotsacars.txt")
i=0
for make in open('../Models/lotsacars-20151202-170935-03d3/labels.txt', 'r').readlines():
    i+=1
    r=curs.execute("select url from images where make = ? limit 3", (unicode(make[:-1]),)).fetchall()
    for x in r:
        print x[0],i
