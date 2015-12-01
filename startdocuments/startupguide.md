# Start  up guide

This guide gives you the necessary steps to prepare for the first Sherlock sprint for the team
working on the "Deep  learning for computer vision" topic. 

1. Read the [topic description document](https://github.com/NLeSC/Sherlock/blob/master/topics/deeplearning/deeplearning4computervision.md). If you are new to the field, it is also useful to look at the links for deep leanring and convolutional neural networks. Also, don't miss the link to the cool Berkeley Vision lab online demo!
2. Watch video introduciton(s):
  * *If you are new to Machine Learning (ML)*, watch this [gentle introduction to ML video] (https://www.youtube.com/watch?v=NOm1zA_Cats) (~ 15 mins. w/o the questions).
  * *If you are new to deep learning (for computer vision)* watch this [video lecture](https://www.youtube.com/watch?v=PlhFWT7vAEw) for Oxford CS students (~ 50 mins.).
3. Make sure you have Python working on your machine.
4. *(conditional) Chose a use case from the [topic description document](https://github.com/NLeSC/Sherlock/blob/master/topics/deeplearning/deeplearning4computervision.md).*
5. Read the paper(s) for the (*chosen*) use case(s): 
 * For the car categorisation use case follow the original link from the topic descritpion or get it from [OneDrive](https://nlesc-my.sharepoint.com/personal/e_ranguelova_esciencecenter_nl/Documents/Sherlock/DeepLearning4ComputerVision/Papers/CarCategorization.pdf). 
 * For the gender&age categorization use case follow the original link from the topic descritpion or get it from [OneDrive](https://nlesc-my.sharepoint.com/personal/e_ranguelova_esciencecenter_nl/Documents/Sherlock/DeepLearning4ComputerVision/Papers/CNN_AgeGenderEstimation.pdf).
6. Download the (*chosen*) use case dataset(s):
 * For the car categorisation use case: [OneDrive](https://nlesc-my.sharepoint.com/personal/e_ranguelova_esciencecenter_nl/Documents/Forms/All.aspx#InplviewHashaca49138-2f09-41f3-8065-eadee2b27c93=RootFolder%3D%252Fpersonal%252Fe%255Franguelova%255Fesciencecenter%255Fnl%252FDocuments%252FSherlock%252FDeepLearning4ComputerVision%252FDatasets%252FCompCars) and use the info from the Access file. Read the README file.
 * For the gender&age categorization use case: [OneDrive](https://nlesc-my.sharepoint.com/personal/e_ranguelova_esciencecenter_nl/Documents/Forms/All.aspx#InplviewHashaca49138-2f09-41f3-8065-eadee2b27c93=RootFolder%3D%252Fpersonal%252Fe%255Franguelova%255Fesciencecenter%255Fnl%252FDocuments%252FSherlock%252FDeepLearning4ComputerVision%252FDatasets%252FAdienceFaces). Read the README file.
7. Install Caffe following the [instructions](http://caffe.berkeleyvision.org/installation.html)
OR use the docker container with Caffe installed (CPU or GPU flavours). [CPU flavour](https://hub.docker.com/r/tleyden5iwx/caffe-cpu-master/). **The docker instructions are valid for a laptop with CPU only. To use Cafee on the DAS5 cluster see [caffe_install.txt](https://github.com/nlesc-sherlock/deeplearning/blob/master/startdocuments/caffe_install.txt)**: 
     * If you don't have docker installed use  `wget -qO- https://get.docker.com/ | sh`
     * If that doesn't work, try it again, and again. ( i had to run it without the "| sh" first)
     * Add user YOURUSERNAME to docker group so you don't have to use sudo for docker commands: `sudo usermod -aG docker YOURUSERNAME`; logout and relogin after to apply.
     * Make a docker file called Dockerfile, it should contain the following:  
       `FROM tleyden5iwx/caffe-cpu-master`  
       `RUN pip install jupyter`  
       `RUN /opt/caffe/scripts/download_model_binary.py /opt/caffe/models/bvlc_reference_caffenet`  
       `EXPOSE 8888`  
     * Start docker deamon: `sudo service docker start`
     * run `docker build -t caffejupyter .`
     * Go to your working directory, say deeplearning (our git hub repo): `cd deeplearning`
     * Define an alias `alias caffe-docker='sudo docker run -ti --rm  -v $PWD:/deeplearning -p 8888:8888 caffejupyter bash'`
     * Run `caffe-docker`
     * inside the docker, go the the appropriate directory (<caffe-root>/notebooks) and run `jupyter notebook --ip=0.0.0.0`
     * Outside the docker open a browser and go to `http://localhost:8888/notebooks/`
     
    This will start the docker VM and map your local Sherlock directory to a Sherlock directory within docker. **Beware: all files generated from within the Docker VM will be owned by root!**
    * These should work without error:
    
         `ipython`

         `import caffe`
         
    * Try the verification commands as described in https://hub.docker.com/r/tleyden5iwx/caffe-cpu-master (running the network takes ~ 15 mins.).
8. Download the (*chosen*) use case Caffe model(s) from the links given at [CaffeModelZoo](https://github.com/BVLC/caffe/wiki/Model-Zoo), namely:
  * For the car categorisation use case download the [GoogLeNet_cars model](https://gist.github.com/bogger/b90eb88e31cd745525ae). Read the README.
 *  For the gender&age categorization use case download the [Age and Gender CNNs] (https://gist.github.com/GilLevi/c9e99062283c719c03de). Read the README.
