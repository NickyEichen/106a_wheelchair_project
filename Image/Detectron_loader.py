import random
import collections
import h5py
import numpy as np

# import some common libraries
import numpy as np
import os, json, cv2, random

import torch, torchvision
print(torch.__version__, torch.cuda.is_available())


# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.modeling import build_model

import pytorch_util as ptu

use_gpu, gpu_id = True, 0
ptu.set_gpu_mode(use_gpu, gpu_id)

os.environ['gpu_id'] = str(gpu_id)

max_num = 21808
dataset_loc = 'bdd_train.hdf5'
hfile = h5py.File(dataset_loc, 'r')

cfg = get_cfg()
# add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
# Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

model = build_model(cfg)

checkpointer = DetectionCheckpointer(model)
checkpointer.load(cfg.MODEL.WEIGHTS)

model.eval()
with torch.no_grad():
    for i in range(max_num):
        group = hfile['virtual/' + str(i)]
        obs_batch = group['observations'][()]

        obs_batch = ptu.from_numpy(obs_batch.transpose([0, 3, 1, 2]))
        
        import ipdb; ipdb.set_trace()

        imgs = [dict(image=obs_batch[i]) for i in range(obs_batch.shape[0])]
        outputs = model(imgs)

        classes = [out['instances'].pred_classes.cpu().numpy() for out in outputs]
        boxes = [out['instances'].pred_boxes.tensor.cpu().numpy() for out in outputs]
        areas = [out['instances'].pred_boxes.area().cpu().numpy() for out in outputs]

        print(classes)
        print(boxes)
        print(areas)