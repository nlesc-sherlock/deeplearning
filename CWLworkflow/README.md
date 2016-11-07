We aim at describing and running the following workflow in Common Workflow Language ([CWL](http://www.commonwl.org/draft-3/UserGuide.html#First_example)) 

* Perform global classification using imagenet1000 model
* Crop the images for a selected group of classes
* Apply dedicates models to further refine the classification of those, e.g. car models, faces (refined to gender, age, etc.)

To run a CWL workflow install a CWL runner, e.g. a reference implementation in python can be installed with:
```
pip install cwlref-runner
```

Then run the workflow by:
```
sudo cwl-runner classify_image.cwl image.yml
```
