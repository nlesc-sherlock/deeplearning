export type DLOutputJsonData = {
    files: string[];
    images: ImageClassification[],
    classes: any;
}

export type ImageClassification = {
    name: string,
    width: number,
    height: number,
    objects: DetectedObject[]    
}

export type DetectedObject = {
    className: string,
    probability: Number,
    bbox: Number[],
    classification?: Classification[],
    detail?: DetailClassification    
}

export type DetailClassification = {
    name: string,
    bbox: Number[],
    classification: Classification[]
}

export type Classification = {
    classifier: string,
    classes: DetectedClass[]
}

export type DetectedClass = {
    name: string,
    probability: Number
}
