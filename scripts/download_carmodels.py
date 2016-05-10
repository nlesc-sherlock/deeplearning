import sqlite3
import wget, os

db = "../carmodels_images_10May2016.db"
conn = sqlite3.connect(db)
curs = conn.cursor()

#f = open("urls_for_lotsacars.txt")
i=0
for row in open('../carmodels.csv', 'r').readlines():
    make,model,frequence = row[:-1].split(',')
    if make == "make": # header line
        continue
    r=curs.execute("select url from images where make = ? and model = ?", (unicode(make),unicode(model))).fetchall()
    carmodel = make+'_'+model

    if os.path.exists(carmodel) is False:
        os.mkdir(carmodel)

    for x in r:
        i+=1
        target = carmodel + '/' + str(i)
        if os.path.exists(target):
            continue
        try:
            url = x[0]
            filename = wget.download(url)
            print(filename + str(i))
            os.rename(filename, target)
        except:
            pass


