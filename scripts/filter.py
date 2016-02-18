#!/usr/bin/env python
"""Filter a folder with images. All images of non-cars will be moved to the non-car folder while keeping all car images.
Any of the following ImageNet categories will be marked as car:
	n04285008 sports car, sport car'
	n03100240 convertible
	n03770679 minivan
	n04037443 racer, race car, racing car
	n02814533 beach wagon, station wagon, wagon, estate car, beach waggon, station waggon, waggon
	n03670208 limousine, limo
	n03594945 jeep, landrover
	n03977966 police van, police wagon, paddy wagon, patrol wagon, wagon, black Maria
	n03895866 passenger car, coach, carriage
	n03769881 minibus
Usage:
  filter.py <basepath>
"""

import os
import subprocess
from docopt import docopt

def is_car(tags):
	categories = ['n04285008', 'n03100240', 'n03770679', 'n04037443', 'n02814533', 'n03670208', 'n03594945', 'n03977966', 'n03895866', 'n03769881']
	for category in categories:
		if category in tags:
			return True
	return False

def filter(basedir):
    subdirs = os.listdir(basedir)
    for subdir in subdirs:
        if subdir == 'non_car':
            continue

        dir = basedir + '/' + subdir
        non_car_dir = dir + '/non_car'
        if os.path.exists(non_car_dir) == False:
            os.mkdir(non_car_dir)
        filenames = os.listdir(dir)
        for name in filenames:
            if name == 'non_car':
                continue

            original = dir + '/' + name
            bashCommand = 'docker run -v ' + dir + ':/data nlesc/imagenet1000 /data/' + name
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = process.communicate()[0]
            print name, is_car(output)
            if is_car(output) == False:
                print output
                target = non_car_dir + '/' + name
                print original
                print target

                os.rename(original, target)

if __name__ == '__main__':
    args = docopt(__doc__)
    filter(args['<basepath>'])



