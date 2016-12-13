Each spesific classification model takes a JSON input and adds to it to produce an output JSON file. Below are the examples of those.

General remarks:

For the Bounding Boxes, the (x,y)  coordinates refer to the top left corner of the bounding box.

In addition, the JSON wrapper script takes two more arguments: <class (string)> and
<threshold (number)>, e.g. {"car","face"} and "0.8". The class string is the class keys of interest in the input JSON file and the threshold is the minimum class probability above which the class probabilities should be reported in the output JSON file.

The input JSON example:
```
{
    "files" : [
        "/path/to/image",
        "/and/another/image"
    ],
    {
        "classes":{
            "car" : [
                {
                    "path" : "/path/to/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "/path/to/cropped/image"
                },
                {
                    "path" : "/and/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "/another/cropped/image"
                }
            ],
            "person" : [
                {
                    "path" : "/yet/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "/yet/another/cropped/image"
                }
            ]
            "dog" : [
                {
                    "path" : "/yet/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "/yet/another/cropped/image"
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
    "files" : [
        "/path/to/image",
        "/and/another/image"
    ],
    {
        "classes":{
            "car" : [
                {
                    "path" : "/path/to/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "/path/to/cropped/image",
                    "classification": [
                        {
                            "classifier": "car/model/name",
                            "tag": [
                                {
                                    "name": "Ford Fiesta",
                                    "probability": <float>
                                },
                                {
                                    "name": "Opel Astra",
                                    "pobability": <float>
                                }
                            ],
                        },                        
                        {
                            "classifier": "car/color/name",
                            "tag": [
                                {
                                    "name": "white",
                                    "probability": <float>
                                },
                                {
                                    "name": "gray",
                                    "pobability": <float>
                                }
                            ],
                        },                                           
                    ]
                },
                {
                    "path" : "/and/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "/another/cropped/image",
                     "classification": [
                     {
                        "classifier": "gender/model/name",
                        "tags": [
                            {"name": "f",
                             "probability": <float>
                            },
                            {"name": "m",
                             "pobability": <float>
                            }
                        ]
                     },
                     {
                        "classifier": "age/model/name",
                        "tags": [
                            {"name": "25 32",
                             "probability": <float>
                            }
                        ]
                     }   
                    ]
                }
            ],
            "person" : [
                {
                    "path" : "/yet/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "/yet/another/cropped/image",                    
                    "classification": [
                    {
                        "classifier": "gender/model/name",
                        "tags": [
                            {"name": "f",
                             "probability": <float>
                            },
                            {"name": "m",
                             "pobability": <float>
                            }
                        ]
                     },
                     {
                        "classifier": "age/model/name",
                        "tags": [
                            {"name": "25 32",
                             "probability": <float>
                            }
                        ]
                     }   
                    ]
                }
            ]
            "dog" : [
                {
                    "path" : "/yet/another/image",
                    "probability" : <float>,
                    "bbox" : [x, y, w, h],
                    "cropped_image": "/yet/another/cropped/image"
                }
            ]
        }
    }
}
```
