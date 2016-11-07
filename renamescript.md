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
