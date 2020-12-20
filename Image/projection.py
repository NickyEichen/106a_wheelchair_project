import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg

num_channels_rgb = 3
num_channels_depth = 1

#assume rgb_img and depth_img are flattened
def project_points(rgb_img: np.ndarray, depth_img: np.ndarray, img_width: int, img_height:int, k: np.ndarray, reshape=False):
    if reshape:
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
        x_left,y_left = box[0], box[1]
        x_right,y_right = box[2], box[3]
        obstacles.append(p_cloud[x_left:x_right, y_left:y_right]) 
    return obstacles

def depth_detect(boxes: list, depth: np.ndarray, treshold = 5):
    #each bounding box is a numpy array of 4 points (2d)
    obstacles = []
    for box in boxes:
        x_left,y_left = box[0], box[1]
        x_right,y_right = box[2], box[3]

        loc = depth[x_left:x_right, y_left:y_right]

        obstacles.append([loc.mean(), loc.std(), loc.max(), loc.min(), loc.min() < treshold]) # using absolute here because of sim sensor reliability
    return obstacles

def ImPlot2D3D(img, rgb, cmap=plt.cm.jet):

    Z = img[::1, ::1]

    fig = plt.figure(figsize=(14, 7))

    # 2D Plot
    ax1 = fig.add_subplot(1, 3, 1)
    im = ax1.imshow(Z, cmap=cmap)
    ax1.set_title('2D')
    ax1.grid(False)

    # 3D Plot
    ax2 = fig.add_subplot(1, 3, 2, projection='3d')
    X, Y = np.mgrid[:Z.shape[0], :Z.shape[1]]
    ax2.plot_surface(X, Y, Z, cmap=cmap)
    ax2.set_title('3D')

    ax3 = fig.add_subplot(1, 3, 3)
    ax3.imshow(rgb)
    ax3.set_title('rgb')

    plt.show()

if __name__ == '__main__':
    rgb_img_loc = 'imgs/front_seg/front_60_seg.png'
    depth_img_loc = 'camera_data/front_depth_motion_60.raw'
    w,h = 672,384
    shape = (h,w,4)


    img = mpimg.imread(rgb_img_loc)

    dt = np.dtype(('f4', 4))
    data = np.fromfile(depth_img_loc, dt, h*w).reshape(shape)[:,:,0]
    data[data > 10] = 10

    plt.hist(data.flatten())
    plt.show()

    ImPlot2D3D(data, img)