#!/usr/bin/env python

import argparse, json, os, subprocess, unicodedata, re

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))

    return value


def crop(item, cclass, index, basedir, outputdir):
    """
    This function crops the image indicated by item.path according to
    item.bbox and stores it in output_folder by a filename that is
    composed of the original filename and the indicated class. The filename stored as
    item.cropped_file.
    """
    # original image full path
    filepath = os.path.join(basedir, item['path'])

    # get file extension
    filebase, extension = os.path.splitext(os.path.basename(filepath))

    newfile = "{}/{}_{}-{}{}".format(
            slugify(cclass),
            filebase,
            slugify(cclass),
            index,
            extension)

    newfile_path = os.path.join(outputdir, newfile)
    bboxstr = "{2}x{3}+{0}+{1}".format(*[int(i) for i in item['bbox']])
    command = "convert {} -crop {} {}".format(filepath, bboxstr, newfile_path)
    if verbose:
        print command
    os.system(command)
    item['cropped_image'] = newfile


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--json_input_file",
                        help="The filename (including path, full or relative) "
                             "of the json file that specifies the input to the "
                             "classifier.",
                        type=argparse.FileType('r'))
    parser.add_argument("--workflow_out",
                        help="Filename (including path, full or relative) "
                             "of the output json file in the Sherlock workflow "
                             "specification.", required=True,
                        type=argparse.FileType('w'))
    parser.add_argument("--input_directory",
                        help="Folder (including path, full or relative) "
                             "in which houses the original images Sherlock workflow"
                             , required=True,
                        type=str)
    parser.add_argument("--cropped_folder",
                        help="Folder (including path, full or relative) "
                             "in which to export the cropped images"
                             , required=True,
                        type=str)
    parser.add_argument("-p", "--probability",
                        help="Threshold value for probabilities based on which "
                             "images are cropped ",
                        type=float, default=0.5)
    parser.add_argument("--specialised",
                        help="Crop images after classifiaction "
                             "instead of after object detection ",
                        action="store_true", default=0)
    parser.add_argument("-v", "--verbose", help="Verbose mode.", action="store_true", default=0)

    args = parser.parse_args()

    verbose = args.verbose
    specialised = args.specialised

    data = json.load(args.json_input_file)

    if not os.path.isdir(args.cropped_folder):
        os.mkdir(args.cropped_folder)

    if not specialised:
        for index, cclass in data['classes'].items():
            if len(data['classes'][cclass]) > 0:
                class_crop_folder = os.path.join(args.cropped_folder, slugify(cclass))
                if not os.path.isdir(class_crop_folder):
                    os.mkdir(class_crop_folder)
                for item in data['classes'][cclass]:
                    if item['probability'] > args.probability:
                        crop(item, cclass, index, args.input_directory, args.cropped_folder)
    else:
        if 'person' in data['classes'].keys():
            face_crop_folder = os.path.join(args.cropped_folder, slugify(cclass))
            if not os.path.isdir(face_crop_folder):
                os.mkdir(face_crop_folder)
            for index, person in data['classes']['person'].items():
                if 'face' in person:
                    crop(person['face'], 'face', index, args.input_directory, args.cropped_folder)

    if verbose:
        print(json.dumps(data, indent=4))

    json.dump(data, args.workflow_out, indent=4, sort_keys=True)
