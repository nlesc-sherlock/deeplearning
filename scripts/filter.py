#!/usr/bin/env python
"""Filter a folder with images. All images of non-cars will be moved to the non-car folder while all car images are
moved to the car directory.
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
verbose = False

def is_car(tags):
    categories = ['n04285008', 'n03100240', 'n03770679', 'n04037443', 'n02814533', 'n03670208', 'n03594945', 'n03977966', 'n03895866', 'n03769881']
    for category in categories:
        if category in tags:
            return True
    return False


def filter_including_subs(basedir):
    if verbose:
        print('entering ' + basedir)

    non_car_dir = get_or_create_noncar_dir(basedir)
    car_dir = get_or_create_car_dir(basedir)

    for entry in os.listdir(basedir):
        path = os.path.join(basedir, entry)
        if os.path.isdir(path):
            if path != non_car_dir and path != car_dir:
                filter_including_subs(path)
        else:
            filter_file(basedir, entry, non_car_dir, car_dir)


def get_or_create_noncar_dir(basedir):
    return get_or_create_dir(basedir, 'non_car')


def get_or_create_car_dir(basedir):
    return get_or_create_dir(basedir, 'car')


def get_or_create_dir(basedir, sub):
    non_car_dir = os.path.join(basedir, sub)
    if not os.path.exists(non_car_dir):
        os.mkdir(non_car_dir)
    return non_car_dir


def filter_file(dir, name, non_car_dir, car_dir):
    original = os.path.join(dir, name)
    bashCommand = ['docker', 'run', '-v', os.path.abspath(dir) + ':/data', 'nlesc/imagenet1000', '/data/' + name]
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    communication = process.communicate()
    output = str(communication[0])
    error = str(communication[1])

    if verbose:
        print('command: ' + str(bashCommand))
        print('std out: ' + output)
        print('std err: ' + error)

    print(original + ' ' + ('is a car.' if is_car(output) else 'is NOT a car.'))

    target = os.path.join(car_dir if is_car(output) else non_car_dir, name)
    os.rename(original, target)

if __name__ == '__main__':
    args = docopt(__doc__)
    filter_including_subs(args['<basepath>'])



