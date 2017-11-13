We aim at describing and running the following workflow in Common Workflow Language ([CWL](http://www.commonwl.org/draft-3/UserGuide.html#First_example)) 

* Perform global classification using imagenet1000 model
* Crop the images for a selected group of classes
* Apply dedicated models to further refine the classification of those, e.g. car models, faces (refined to gender, age, etc.)

To run a CWL workflow install a CWL runner, e.g. a reference implementation in python can be installed with:
```sh
pip install cwlref-runner
```
Further dependencies:
```sh
sudo apt-get install imagemagick
```

Then run the workflow by:
```sh
sudo cwl-runner workflow.cwl image.yml
```

## Pipeline workflow

Install (mini)conda if you don't have it, because conda is just awesome. And also ipython for the same reason.

```sh
conda install ipython
```

Install CWL Python stuff:
```sh
pip install cwlref-runner
```

**The following only works on our dl-secundus VM, should be made more general!**

Install Berend's cwltool version (and first remove existing one):
```sh
pip uninstall cwltool
cd /data/berend/git/cwltool/
pip install --ignore-installed -U .
```

Add the bin directory to your path if you hadn't before. E.g. if you use pip without conda:
```sh
export PATH="$HOME/.local/bin:$PATH"
```
If you use conda, the directory was probably already added to your path automatically.

Run the pipeline with some input directory `$DIRWITHIMAGES` which contains image files:
```sh
cd deeplearning/CWLworkflow
DIRWITHIMAGES=/data/berend_data/train2014
cwltool pipeline.cwl --directory_in $DIRWITHIMAGES
```
