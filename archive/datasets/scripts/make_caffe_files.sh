#!/bin/bash

#
# Usage:
#    make_caffe_files.sh <directory>
#
# This script generates a labels.txt, train.txt and test.txt for use with caffe
#
# The first argument should be a directory which has one sub-directory per label
# each sub-directory should contain the images of that class.
#
# - labels.txt will contain a list of labels
# - train.txt will contain roughly 70% of the images as a training set
# - test.txt will contain the other 30% as a test set
#
# Both test and training sets are randomized, the script also generates
# sorted versions of both train and test files.
#
# The script depends on getopts, gawk and perl, but should run fine on most
# linux systems
#
# @author: Berend, Lars
#


# Parse the options
while getopts "s:" opt; do
    case $opt in
        s)
            seed=$OPTARG
            ;;
        \?)
#            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
#            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done

# "Parse" the positional arguments
shift $(( OPTIND - 1 )) # shift off the other options
if [ "$#" -ne 1 ]; then
    echo 'Usage: make_caffe_files.sh [OPTIONS] [DIRECTORY]

    Options:
        -s  Seed for the randomization  optional
    '
    exit
fi

DIRECTORY=$1
pwd=$PWD


# Clean up previous files
files=('labels.txt' 'images.txt' 'train_sorted.txt' 'train.txt' 'test_sorted.txt' 'test.txt')
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
    fi
done


#
# Finding Labels in the supplied directory
#
echo "Finding labels"
labels=()
# To get a nice list with just the directory names we have to cd
# into the directory
cd $DIRECTORY
for file in *; do
    if [[ -d "$file" ]]; then
        labels+=("$file")
    fi
done
# Go back to the previous working directory to write the labels file
cd $pwd
printf "%s\n" "${labels[@]}" > labels.txt
echo "Found " ${#labels[@]} " directories as labels"

#
# Find all images in the directory
#
echo "Finding all images..."
find $DIRECTORY -name *.jpg > images.txt
NUMIMAGES=$(wc -l < images.txt)
echo "Found $NUMIMAGES images."


echo "Generating train and test files"
# Get the fully qualified path of the parent directory
# of the images directory. This will be prefixed to the
# output of find
FULLPATH=$(readlink -e $DIRECTORY/..)
awk -F/ -v prefix=$FULLPATH '
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
        print "Found", length(label), "labels"
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
        
        print prefix"/"$0, label[$2] >> out
    }
    END {
        print "Wrote", train, "training instances and", test,"test instances"
    }' images.txt


# We're using a perl trick to randomize the order in the test and train file
# it was the shortest way I could find to do this.
echo "Shuffling training and test files"

if [ -z $seed ]; then
    shuffle_command="print shuffle(<STDIN>);"
else
    echo "Using $seed as seed"
    shuffle_command="srand $seed; print shuffle(<STDIN>);"
fi

cat 'test_sorted.txt' | perl -MList::Util=shuffle -e "$shuffle_command" > test.txt
cat 'train_sorted.txt' | perl -MList::Util=shuffle -e "$shuffle_command" > train.txt
