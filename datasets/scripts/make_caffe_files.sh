#!/bin/bash

DIRECTORY=$1

echo "Finding all images..."
find $DIRECTORY -name *.jpg > images.txt
#ls $DIRECTORY/**/*.png >> images.txt
#ls $DIRECTORY/**/*.gif >> images.txt
NUMIMAGES=$(wc -l < images.txt)
echo "Found $NUMIMAGES images."

files=('train_sorted.txt' 'train.txt' 'test_sorted.txt' 'test.txt')

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
    fi
done

echo "Generating train and test files"
awk -F/ '
    BEGIN {
        if ((getline < "labels.txt") < 0) {
            m = "unexpected EOF or error"
            m = (m ": " ERRNO)
            print m > "/dev/stderr"
            exit
        }
        close("labels.txt")
        while ((getline <"labels.txt") > 0) {
            label[$0] = i++
        }
        print "Found", length(label), "labels:"
        test = 0
        train = 0
    }
    
    {
        out = "train_sorted.txt"
        num = rand()
        if (num < 0.3) {
            test++
            out = "test_sorted.txt"
        } else {
            train++
        }
        
        print $0, label[$2] >> out
    }
    END {
        print "Wrote", train, "training instances and", test,"test instances"
    }' images.txt

echo "Shuffeling training and test files"
cat 'test_sorted.txt' | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' > test.txt
cat 'train_sorted.txt' | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' > train.txt
