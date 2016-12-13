Each spesific classification model takes a JSON input and enriches it to produce an output JSON file. Below are the examples of those input/output files.

General remarks:
* For the Bounding Boxes, the (x,y)  coordinates refer to the top left corner of the bounding box.
* The JSON wrapper should look at a part of the JSON at a spesific _class (string)_ e.g. {"car","face"}. Also it should consider otputting classificaiton probabilities anly above a desired _threshold (number)_,  e.g. "0.8". 

The input JSON example:
```
{
    "files" : [                                                          # from CWL input
        "/path/to/image",
        "/path/to/another/image",
        "path/to/yet/another/image",
        ...
    ],
    {
        "classes":{                                                      # from object detector (Yolo/SSD)
            "car" : [
            {
                    "path" : "/path/to/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "/path/to/cropped/image"           # from cropper
                },
                {
                    "path" : "path/to/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "path/to/another/cropped/image"    # from cropper
                }
            ],
            "person" : [
                {
                    "path" : "path/to/yet/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "path/to/yet/another/cropped/image"    # from cropper
                    "face" :                                                # from face detector
                    { 
                        "path" : "path/to/yet/another/cropped/image",
                        "bbox" : [x, y, w, h],                              # in relation to the cropped person!
                        "probability": <float>,
                        "cropped_image" : "path/to/yet/another/cropped/face/image"     # from cropper
                    }
                }
            ]
            "dog" : [
                {
                    "path" : "path/to/yet/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "path/to/yet/another/cropped/image"    # from cropper
                }
            ]            
        }
    }
}
'''
```

The output JSON enriches the input JSON with a classifier results for each BBox/
cropped_image:

```
{
    "files" : [                                                          # from CWL input
        "/path/to/image",
        "/path/to/another/image",
        "path/to/yet/another/image",
        ...
    ],
    {
        "classes":{                                                      # from object detector (Yolo/SSD)
            "car" : [
            {
                    "path" : "/path/to/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "/path/to/cropped/image"            # from cropper
                },
                {
                    "path" : "path/to/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "path/to/another/cropped/image"    # from cropper
                }
            ],
            "person" : [
                {
                    "path" : "path/to/yet/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "path/to/yet/another/cropped/image"    # from cropper
                    "face" :                                                # from face detector
                    { 
                        "path" : "path/to/yet/another/cropped/image",
                        "bbox" : [x, y, w, h],                              # in relation to the cropped person!
                        "probability": <float>,
                        "cropped_image" : "path/to/yet/another/cropped/face/image"    # from cropper
                    }
                }
            ]
            "dog" : [           
                {
                    "path" : "path/to/yet/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "path/to/yet/another/cropped/image"            # from cropper
                }
            ]            
        }
    }
}
'''
```
