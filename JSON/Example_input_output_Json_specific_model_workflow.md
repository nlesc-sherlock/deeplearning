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
            "animal" : [
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

The output JSON is an enriched version of the input JSON with a classifier results for each BBox/
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
                    "classification": [
                    {
                        "classifier": "car/model/name",                  # added by car model classifier
                        "tags": [
                            {   
                            "name": "Ford Fiesta",
                            "probability": 0.7
                            },
                            {
                            "name": "Opel Astra",
                            "probability": 0.3                        
                            }
                        ],
                    },
                    {
                        "classifier": "car/color/name",                 # added by car color classifier
                        "tags": [
                            {   
                            "name": "white",
                            "probability": 0.6
                            },
                            {
                            "name": "gray",
                            "probability": 0.4
                            }
                        ],
                    }
                    ]
                },
                {
                    "path" : "path/to/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "path/to/another/cropped/image", # from cropper
                    "classification: : [
                    ...
                    ]
                    
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
                        "classification": [
                             {
                            "classifier": "face/gender",                    # added by face gender classifier
                            "tags": [
                                {   
                                "name": "female",                           # the current docker exports "f"!
                                "probability": 0.65
                                },
                                {
                                "name": "male",                             # the current docker exports "m"!
                                "probability": 0.35                        
                                }
                            ],
                            },
                            {
                            "classifier": "face/age",                      # added by face age classifier
                                "tags": [
                                    {   
                                    "name": "25 32",
                                    "probability": 0.65
                                    },
                                    {
                                    "name": "38 44",
                                    "probability": 0.35
                                    }
                                ],
                            }
                        }
                 }
                ]
            "animal" : [           
                {
                    "path" : "path/to/yet/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "path/to/yet/another/cropped/image"          # from cropper
                    "classification": [
                    {
                        "classifier": "object class",                             # added by general 1000 classifier
                        "tags": [
                            {   
                            "name": "dog",
                            "probability": 0.9
                            },
                            {
                            "name": "Gaerman sheperd",
                            "probability": 0.1                        
                            }
                        ],
                    }
                    ]
                }
            ]            
        }
    }
}
'''
```
