#Deep learning for computer vision tasks

Deep Machine Learning has been declared the new frontier in artificial intelligence research in 2010, [I. Arel et al, "Research frontier: Deep machine learning- a new frontier in artificial intelligence research "](http://web.eecs.utk.edu/~itamar/Papers/CIM2010.pdf). It is important that in NLeSc we have knowledge and experience with the latest research in data analytics, where deep learning is currently the trend. 

## Convolutional Neural Networks
The Convolutional Neural Networks (CNN) are a type of deep learning networks, [Y. Bengio, "Learning deep architechures for AI"](http://www.iro.umontreal.ca/~bengioy/papers/ftml.pdf). CNNs are a family of multi-layer neural networks particularly designed for use on two-dimensional data, such as images. For a quick introduction to CNNs, please refer to section 2.3 of the [“Large-scale Computer Vision” overview](https://nlesc.sharepoint.com/sites/mlpr/Shared%20Documents/overview.pdf). For a more elaborate introduction, please refer to the online book [“Neural Networks and Deep Learning”](http://neuralnetworksanddeeplearning.com/index.html) and to the vast resources on [deeplearning.net](http://deaplearning.net). 

## Sherlock
In the context of project Sherlock we look at some of the questions asked by the digital forensic investigators, for example: *“Can we automatically and quickly find a (red) Ferrari in the images on a suspect’s disk?”*, *“Can we automatically and quickly find the persons (identity/ age/ gender) in the image data?”*, etc. Tacking such questions, which are image classification tasks, with deep learning seems very promising. For a flavor of what CNNs can achieve in image classification, try this very interesting Berkeley Vision lab [online demo](http://demo.caffe.berkeleyvision.org/). 

The first sprint of project Sherlock has the following goals:

1.	Learn <sup>[$](#footnote1)</sup> about deep learning and CNNs and their application in CV tasks
2.	Verify weather CNNs are suitable for CV tasks found in digital forensics

## Use cases
To achieve these goals, the team will work on some use cases:

* Car model classification
* Person gender & age classification

A pre-trained CNNs for these use cases are made [available](http://caffe.berkeleyvision.org/model_zoo.html) by researchers. We are going to use these models for learning and experimenting.

### Car model classification
A large image **dataset** of different car models "CompCars" have been assembled and presented in the following extended CVPR 2015 **paper** ["A Large-Scale Car Dataset for Fine-Grained Categorization and Verification"](http://www.cv-foundation.org/openaccess/content_cvpr_2015/app/2B_069_ext.pdf). An autorised copy of the dataset is available at [OneDrive](https://nlesc-my.sharepoint.com/personal/e_ranguelova_esciencecenter_nl/_layouts/15/onedrive.aspx#id=%2Fpersonal%2Fe_ranguelova_esciencecenter_nl%2FDocuments%2FSherlock%2FDeepLearning4ComputerVision%2FDatasets%2FCompCars).

### Person gender & age classification
A diverse image **dataset** of photos of persons under very  challenging conditions have been introduced in the [Adience benchmark](http://www.openu.ac.il/home/hassner/Adience/data.html#agegender). CNNs have been used to claffify these data in the following CVPR 2015 workshop **paper** ["Age and Gender Classification using Convolutional Neural Networks"](http://www.openu.ac.il/home/hassner/projects/cnn_agegender/CNN_AgeGenderEstimation.pdf). A copy of the dataset is available at [OneDrive](https://nlesc-my.sharepoint.com/personal/e_ranguelova_esciencecenter_nl/_layouts/15/onedrive.aspx#id=%2Fpersonal%2Fe_ranguelova_esciencecenter_nl%2FDocuments%2FSherlock%2FDeepLearning4ComputerVision%2FDatasets%2FAdienceFaces).

## Sprint steps
We will try to achieve the goals following number of steps (*steps in italic are conditional time permiting*):

1.	Learning about basics of Deep learning and CNNs
2.	Follow tutorial(s) on deep leaning for image classification using [Caffe](http://caffe.berkeleyvision.org/). Caffe is a deep learning framework developed by the Berkeley Vision and Learning Center.
3.	Use CNNs pre-trained on [ImageNet](http://www.image-net.org/) and fine-tuned on car and person’s datasets (available at [Caffe Model Zoo](https://github.com/BVLC/caffe/wiki/Model-Zoo) ) to get classification results as reported in the papers.
4.	Learn about fine-tuning pertained CNNs for a specific CV task. 
5.	Learn about training CNNs. 
6.	*Learn about using [Keras](http://keras.io/) with Caffe models.*
7.	*Designing CNNs architectures.*
8.	Software in git and lessons learned report.

## Startup guide
To prepare for the sprint, please follow the preparation steps in the [startup guide](https://github.com/NLeSC/Sherlock/blob/master/topics/deeplearning/startupguide.md).

<a name="footnote1">$</a>: Team leader also needs to learn the theory and tools.

### References
All the papers listed below are available also at [OneDrive](https://nlesc-my.sharepoint.com/personal/e_ranguelova_esciencecenter_nl/Documents/Forms/All.aspx#InplviewHashaca49138-2f09-41f3-8065-eadee2b27c93=RootFolder%3D%252Fpersonal%252Fe%255Franguelova%255Fesciencecenter%255Fnl%252FDocuments%252FSherlock%252FDeepLearning4ComputerVision%252FPapers).
*   I. Arel, D. C. Rose and T. P. Karnowski., "Research frontier: Deep machine learning- a new frontier in artificial intelligence research," Computer Intalligence Magazine, pp. 13-18, 2010. 
*   Y. Bengio, "Learning deep archiechures for AI," Foundations and Trends Machine Learning, vol. 2, no. 1, pp. 1-127, 2009. 
* 	L. Yang, P. Luo, C. C. Loy and X. Tang, "A Large-Scale Car Dataset for Fine-Grained Categorization and Verification", in Computer Vision and Pattern Recognition (CVPR), Boston, 2015. 
*	G. Levi and T. Hassner, "Age and Gender Classification using Convolutional Neural Networks", in IEEE Workshop on Analysis and Modeling of Faces and Gestures (AMFG), at the IEEE Conf. on Computer Vision and Pattern Recognition (CVPR), Boston, 2015. 
