#Lessons learnt from Sprint 4: 10 - 12 May 2016

* Collecting images of cars (~700 models, 70 000 images) via the Bing API from Internet. The dataset is quite noisy.
* Using another solver can improve performance.

* Fine tuning of a CNN in DIGITS doesn't work smoothly, instead we train it directly in Caffe. For more info see the IPython notebook:
   * https://github.com/BVLC/caffe/tree/master/examples/finetune_flickr_style

* Visualizing a network using VisDeep toolbox:
    * Works nicely for the example model (caffenet-yos), gives a lot of insight.
    * Very hard to adapt to other model, ran into many issues (size of mean image, size of input images, missing parameters, everything undocumented).
         * https://github.com/BVLC/caffe/issues/290#issuecomment-62846228
         
* Docker is very useful for **deployment**, not for containerizing every random piece of software. Don't use it by default, use it mainly for server-like-thingies.
