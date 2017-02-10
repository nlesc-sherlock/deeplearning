
NV_DOCKER = nvidia-docker

repo = nlescsherlockdl

.SILENT:
.PHONY: all

all: ssd.coco-wrapper

caffe-nv: caffe-nv/Dockerfile
	cd caffe-nv && $(NV_DOCKER) build -q-t $(repo)/$@ .

ssd.caffe-nv: object_detect_ssdnet/caffe-nv-ssd/Dockerfile
	cd object_detect_ssdnet/caffe-nv-ssd && $(NV_DOCKER) build -q -t $(repo)/$(subst .,:,$(@)) . > /dev/null

ssd.coco: object_detect_ssdnet/coco/Dockerfile ssd.caffe-nv
	cd object_detect_ssdnet/coco && $(NV_DOCKER) build -q -t $(repo)/$(subst .,:,$(@)) . > /dev/null

ssd.coco-wrapper: object_detect_ssdnet/coco-wrapper/Dockerfile ssd.coco
	cd object_detect_ssdnet/coco-wrapper && $(NV_DOCKER) build -q -t $(repo)/$(subst .,:,$(@)) . > /dev/null

