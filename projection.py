import numpy as np

num_channels_rgb = 3
num_channels_depth = 1

#assume rgb_img and depth_img are flattened
def project_points(rgb_img: np.ndarray, depth_img: np.ndarray, img_width: int, img_height:int, k: np.ndarray):
    rgb_img = rgb_img.reshape((img_width, img_height,num_channels_rgb))
    depth_img = depth_img.reshape((img_width, img_height,num_channels_depth))
    k_inv = np.linalg.inv(k)
    p_cloud = np.zeros((img_width, img_height,num_channels_rgb*2))
    
    for i in range(img_height):
        for j in range(img_width):
            rgb = rgb_img[i,j]
            d = depth_img[i,j]

            uv_coord = np.array(float(i), float(j), 1.0)
            loc = d * np.dot((k_inv, uv_coord))
            
            p_cloud[i,j] = np.concatenate((rgb,loc))
    
    return p_cloud

def gather_pointcloud_boxes(boxes: list, p_cloud: np.ndarray):
    #each bounding box is a numpy array of 4 points (2d)
    obstacles = []
    for box in boxes:
        x_left,y_left = box[0, 0], box[1, 0]
        x_right,y_right = box[0, 3], box[1, 3]
        obstacles.append(p_cloud[x_left:x_right, y_left:y_right]) 
    return obstacles