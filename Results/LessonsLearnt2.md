# Lessons learnt from Sprint 2: 1-3 December 2015

- updated the other 2 team members of what we have done on the first sprint.  
  - We looked at the age and gender use case. 
  - We learned to install the iptyhon notebook for caffe and use it to classify some images.  
- Installed DIGITS on the das super, DIGITS is the graphical user interface for Caffe with NVIDIA Cuda support.  
  - We quickly decided to add more than one running DIGITS node so we could parellalize.  
  - We started several training jobs on das with DIGITS to find out what training methods are best for this type of network.  
  - DIGITS cannot load pre-trained models. It is useful for training your own networks (and getting them out) though.  
- Training a neural network requires several parameters, we learned that:  
  - Increasing the number of epochs gives the network more time to train, but it costs more time (duh).  
  - The learning rate should not be highr than 0.01, since that is not useful for training.  
  - The learning rate should decrease over time, to let the netowork fine-tune. The manner in which this happens does not matter too much for the quality of the resulting network. Using a sigmoid curve gave us good results in decent time.  
- Quite a few data preparation tasks were performed.  
  - Bash scripting to rename and squash direcory structures.  
  - Bash scripting to scrape google images for testing purposes.  
  - Perl script to scrape a car sales website for pre-classified images.  
  - Python script to scrape an auction site for more pre-classified car images.  
- Built a docker container to classify images given an arbitrary DIGITS trained model.  

- And we all relearned lots of shell commands ....  
