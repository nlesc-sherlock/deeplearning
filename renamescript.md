To move all of the files from the subdirectory NOT called non_car to the current directory:  
``
find . -mindepth 2 -print ! -wholename '*non_car*' -exec mv $PWD/{} $PWD/. \;
``

To do this for all subdirectories in this directory:  
``
for d in ./*/ ; do (cd "$d" && find . -mindepth 2 -print ! -wholename '*non_car*' -exec mv $PWD/{} $PWD/. \; ); done
``

To delete all of the non_car/ and car/ subdirectories in the directories in this folder:  
``
for d in ./*/ ; do (cd "$d" && rm -rf $PWD/car/ $PWD/non_car/ ); done
``

To rename all of the .jpg images that were apparantly not .jpg but .png images to .png:
```
 cat  /data/DIGITS/digits/jobs/20161107-144707-e748/create_val_db.log |grep LoadImageError | awk {'print $4'} | sed 's/\[//' | sed 's/\]//' | sed 's/.jpg//' | xargs -I {} mv {}.jpg {}.png
```
