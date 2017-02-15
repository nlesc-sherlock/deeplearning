import argparse
import json
import sys

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

    sc = subparsers.add_parser("json4viz", help="Return the json required for visualization")
    sc.add_argument('-o', '--output_json', type=argparse.FileType('w'), help="Image of interest", default=sys.stdout)
    sc.set_defaults(func=create_json4viz)

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

def create_json4viz(json_dict, args):
    images = {}
    for cl in json_dict['classes']:
        for image in json_dict['classes'][cl]:
            path=image['path']
            del image['path']
            image['object'] = cl
            if path in images:
                images[path].append(image)
            else:
                images[path]=[image]
    print json.dump(images, args.output_json, indent=4)
  
def main():
    # parse the input arguments
    parser= argument_parser()
    args = parser.parse_args()
    
    # load the input (pipeline output) json file
    json_dict = json.load(args.json_filename)
    
    args.func(json_dict, args) 
        
if __name__ == "__main__"    :
    main()

