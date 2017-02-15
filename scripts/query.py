import argparse
import json
import matplotlib

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_filename', help="JSON file", type=argparse.FileType('r'))
    subparsers = parser.add_subparsers(title='Sub-commands')

    sc = subparsers.add_parser("classes", help="Return the list of detected classes")
    sc.set_defaults(func=list_classes)     

    sc = subparsers.add_parser("images", help="Return the list of scanned images")
    sc.set_defaults(func=list_images)     

    sc = subparsers.add_parser("class", help="Return the images containing a classes")
    sc.add_argument('type', type=str, help="Class of interest")
    sc.set_defaults(func=list_class)

    sc = subparsers.add_parser("image", help="Return the list of classes detected in an image")
    sc.add_argument('image', type=str, help="Image of interest")
    sc.set_defaults(func=list_image)

    return parser     
    
    
def list_classes(json_dict, args):
    print "Class          #objects"
    print "-----------------------"
    for cl in json_dict['classes']:
        print "{:20s}{:3d}".format(cl, len(json_dict['classes'][cl]))

def list_class(json_dict, args):
    print "Images containing: {:10s} Probability".format(args.type)
    print "-----------------------------------------"
    for image in json_dict['classes'][args.type]:
        print "{:30s}{:6.4f}".format(image['path'],image['probability']) 
        if 'classification' in image:
            for c in image['classification']:
                for tag in c['tags']:
                    print "     {:25s}{:6.4f}".format(tag['name'][:-1], tag['probability'])


def list_images(json_dict, args):
    print "Image                    #objects"
    print "---------------------------------"
    images = {}
    for cl in json_dict['classes']:
        for image in json_dict['classes'][cl]:
            if image['path'] in images:
                images[image['path']]+=1
            else:
                images[image['path']]=1
    for image in images:
        print "{:30s}{:3d}".format(image, images[image])

def list_image(json_dict, args):
    print "Classes in image: {:20s} Probability".format(args.image)
    for cl in json_dict['classes']:
        for image in json_dict['classes'][cl]:
            if args.image == image['path']:
                print "{:40s}{:6.4f}".format(cl, image['probability'])
                if 'classification' in image:
                    for c in image['classification']:
                        for tag in c['tags']:
                            print "     {:35s}{:6.4f}".format(tag['name'][:-1], tag['probability'])
  
def main():
    # parse the input arguments
    parser= argument_parser()
    args = parser.parse_args()
    
    # load the input (pipeline output) json file
    json_dict = json.load(args.json_filename)
    
    args.func(json_dict, args) 
        
if __name__ == "__main__"    :
    main()

