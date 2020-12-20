## Vision Module

Using machine learning, we are able to segment the image for different obstacles which our image model detects. We distinguish waypoints in the case of detecting a ramp and send this information across a topic subscribed by the path planning module. 

## Files Present
1. `detectron_server.py` — Full SocketIO Client utilizing Mask RCNN Model + Depth Information
2. `projection.py` — Camera Intrinsics Utility functions
3. `canny.py` — Canny Edge Detector Implementation (followed medium tutorial) — baseline/comparison for semantic segmentation
4. `pytorch_util.py` — Functions used with Pytorch 
5. There are also other misc notebooks + loaders used for figure generation + experimentation