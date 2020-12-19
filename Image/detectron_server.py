# -*- coding: utf-8 -*-

# install dependencies: 
import torch, torchvision
print(torch.__version__, torch.cuda.is_available())

# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random
from collections import defaultdict

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import pickle
from projection import *

import pytorch_util as ptu
import cv2


ptu.set_gpu_mode(True)
ptu.set_device(0)

#setup Mask RCNN
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))

custom = True # use of custom model mask RCNN Model
if custom:
    f = open('../../../temp/checkpoint_800.pkl', 'rb')
    cfg.MODEL.WEIGHTS = pickle.load(f)
else:
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")

predictor = DefaultPredictor(cfg)

def predict(im, reverse = True):
    if reverse: im = im[:, ::-1] # Needs BGR images
    panoptic_seg, segments_info = predictor(im)["panoptic_seg"]
    v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1)
    return v.draw_panoptic_seg_predictions(panoptic_seg.to("cpu"), segments_info).get_image(), panoptic_seg, segments_info


### SOCKET IO CLIENT
import socketio
sio = socketio.Client()

states = defaultdict(lambda: None)

@sio.event
def connect():
    sio.emit("subscribe", ["/right/RGBD_Image", "/left/RGBD_Image", "/front/RGBD_Image", "/back/RGBD_Image", "Process_CMD"])
    print('Connected successfully')

@sio.event
def connect_error():
    print('Failed to connect :(')

@sio.event
def disconnect():
    print('Connection Lost')


def extract_img(img_bytes, shape_curr, channels=4):
    h,w = shape_curr

    dt = np.dtype(('f4', 4))

    img = np.frombuffer(img_bytes, dtype=dt).reshape((h,w,channels))
    if channels == 4:
        img = img[:,:,:3] # remove alpha
    return img


@sio.on('/right/RGBD_Image')
def right_cam(data):
    shape = data['height'], data['width']

    rgb = extract_img(data['rgb'], shape)
    depth = extract_img(data['depth'], shape, 1)

    states['right'] = predict(rgb) #tuple
    states['right_rgb'] = rgb
    states['right_depth'] = depth
    states['right_k'] = data['intrinsic_mat'].reshape((3,3))

@sio.on('/left/RGBD_Image')
def right_cam(data):
    shape = data['height'], data['width']

    rgb = extract_img(data['rgb'], shape)
    depth = extract_img(data['depth'], shape, 1)

    states['left'] = predict(rgb) #tuple
    states['left_rgb'] = rgb
    states['left_depth'] = depth
    states['left_k'] = data['intrinsic_mat'].reshape((3,3))

@sio.on('/front/RGBD_Image')
def right_cam(data):
    shape = data['height'], data['width']

    rgb = extract_img(data['rgb'], shape)
    depth = extract_img(data['depth'], shape, 1)

    states['front'] = predict(rgb) #tuple
    states['front_rgb'] = rgb
    states['front_depth'] = depth
    states['front_k'] = data['intrinsic_mat'].reshape((3,3))


@sio.on('/back/RGBD_Image')
def right_cam(data):
    shape = data['height'], data['width']

    rgb = extract_img(data['rgb'], shape)
    depth = extract_img(data['depth'], shape, 1)

    states['back'] = predict(rgb) #tuple
    states['back_rgb'] = rgb
    states['back_depth'] = depth
    states['back_k'] = data['intrinsic_mat'].reshape((3,3))


@sio.on('/Process_CMD') # flag for when all images updated
def process(data):
    keys = ['left', 'right', 'front', 'back']
    proj_points = []
    waypoint_emitted = False

    for key in keys:
        rgb, depth, k, seg = states[key + 'rgb'], states[key + '_depth'], states[key + '_k'], states[key]
        pts = project_points(rgb, depth, rgb.shape[0], rgb.shape[1], k, reshape = False)
        proj_points.append(pts)

        if data['waypoint'] and not waypoint_emitted:
            if 'truck' in seg[-1]['labels']:
                seg_num = seg[-1]['labels'].index('truck')
                points = gather_pointcloud_boxes(seg[1][seg_num], pts)[0]
                rgb = points[:, :3]
                locs = points[:, 3:]

                wp = (locs[:, 0].mean(), locs[:, 1].min(), locs[:, 2].mean()) #xyz

                sio.emit('/waypoint', wp)
                waypoint_emitted = True
        else:
            obstacles_depth_info = depth_detect(seg[1], depth, treshold = data['tresh']) 
            close =  any([i[-1] for i in obstacles_depth_info])
            sio.emit('/obstacle', close)
    
    sio.emit('/parsed', states)



