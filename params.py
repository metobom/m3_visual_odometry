import numpy as np
# CAM PARAMS
W, H = 1280, 720
K = np.load('cam_params/logitech_c310_cam_mat.npy')
DIST_COEFFS = np.load('cam_params/logitech_c310_dist_coeffs.npy')
R = np.load('cam_params/logitech_c310_rmat.npy')
t = np.load('cam_params/logitech_c310_tvec.npy')
# 3D PARAMS
GOODIES_TH = .005
OBJ_PTS_THCK = 3
# 2D PARAMS
IMG_PTS_NUM = 6000
FE_QUALITY = .001
FE_MIN_DIST = 0
GOOD_PTS_TH = .95
IMSHOW_SIZE = (640, 480)
