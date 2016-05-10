import sqlite3
import wget, os

db = "../carmodels_images_10May2016.db"
conn = sqlite3.connect(db)
curs = conn.cursor()

#f = open("urls_for_lotsacars.txt")
i=0
for row in open('../carmodels.csv', 'r').readlines():
    i+=1
    make,model,frequence = row[:-1].split(',')
    if make == "make": # header line
        continue
    r=curs.execute("select url from images where make = ? and model = ?", (unicode(make),unicode(model))).fetchall()
    carmodel = make+'_'+model 
    os.mkdir(carmodel)
    for x in r:
        try:
            url = x[0]
            filename = wget.download(url)
            print filename,i
            os.rename(filename, carmodel+'/'+filename)
        except:
            pass
    i+=1

