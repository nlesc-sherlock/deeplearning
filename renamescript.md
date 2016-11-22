To move all of the files from the subdirectory called car to their parent directory:  
``
find . -type f -wholename '*/car/*' -print | awk -F'/' '{system("mv \""$2"\"/car/"$4" \""$2"\"/"$4)}'
``

To delete all of the non_car/ and car/ subdirectories in the directories in this folder:  
``
for d in ./*/ ; do (rm -rf "$d/non_car/"); done

for d in ./*/ ; do (rm -rf "$d/car/"); done
``

To rename all of the .jpg images (according to mime type) {}.jpg
```
find . -mindepth 1 -type f -print | xargs -I {} file --mime-type "{}"  | grep jpeg | awk -F':' '{print $1}' | xargs -I {} mv {} {}.jpg
```

To rename all of the .png images (according to mime type) {}.png
```
find . -mindepth 1 -type f -print | xargs -I {} file --mime-type "{}"  | grep png | awk -F':' '{print $1}' | xargs -I {} mv {} {}.png
```

To delete all of the non-jpg and non-png images
```
find . -mindepth 1 -type f -print | xargs -I {} file --mime-type "{}" | grep -v 'jpeg\|png' | awk -F':' '{print $1}' | xargs -I {} rm {}
```

To rename all of the .jpg images that were apparantly not .jpg but .png images to .png:
```
 cat  /data/DIGITS/digits/jobs/20161107-144707-e748/create_val_db.log |grep LoadImageError | awk {'print $4'} | sed 's/\[//' | sed 's/\]//' | sed 's/.jpg//' | xargs -I {} mv {}.jpg {}.png
```
