import cv2
import numpy as np
import OpenGL.GL as gl
import pangolin
from params import OBJ_PTS_THCK, GOODIES_TH, R, t, IMG_PTS_NUM, FE_MIN_DIST, FE_QUALITY, GOOD_PTS_TH, IMSHOW_SIZE, K, DIST_COEFFS

# NEED TO FIX GET_POSE for odometry
class GET_POSE:
    def __init__(self):
        # remain commented till fix pose
        self.trajectories = []
        self.C = np.array([0, 0, 0]).reshape(3,1)
        self.holder = None

    def calc_pose(self,):
        self.C = -R.T * t
        print(self.C)
        self.trajectories.append(self.C[:3, 3])
        return self.trajectories

class GET_IMG_PTS:
    def __init__(self):
        self.orb = cv2.ORB_create(IMG_PTS_NUM, scaleFactor = None)
        self.fast = cv2.FastFeatureDetector_create()
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

    def calc_fs(self, f0, f1):
        # LEFT FRAME
        pts0 = cv2.goodFeaturesToTrack(np.mean(f0, axis = 2).astype(np.uint8), IMG_PTS_NUM, qualityLevel = FE_QUALITY, minDistance = FE_MIN_DIST)
        kps0 = [cv2.KeyPoint(x = f0[0][0], y = f0[0][1], _size = 20) for f0 in pts0]
        #kps0 = self.fast.detect(f0, None)
        kps0, des0 = self.orb.compute(f0, kps0)
        # RIGHT FRAME
        pts1 = cv2.goodFeaturesToTrack(np.mean(f1, axis = 2).astype(np.uint8), IMG_PTS_NUM, qualityLevel = FE_QUALITY, minDistance = FE_MIN_DIST)
        kps1 = [cv2.KeyPoint(x = f1[0][0], y = f1[0][1], _size = 20) for f1 in pts1]
        #kps1 = self.fast.detect(f1, None)
        kps1, des1 = self.orb.compute(f1, kps1)
        matches_stereo = self.matcher.knnMatch(des0, des1, k = 2)
        # INIT MATCH HOLDERS
        ret_stereo = []
        # MATCH LEFT AND RIGHT FRAMES
        for m, n in matches_stereo:
            if m.distance < GOOD_PTS_TH * n.distance:
                kp0 = kps0[m.queryIdx].pt
                kp1 = kps1[m.trainIdx].pt
                ret_stereo.append((kp0, kp1))
        ret_stereo = np.array(ret_stereo)
        return ret_stereo[:, 0], ret_stereo[:, 1]

    def draw2d(self, matches, f0, f1):
        for pt0, pt1 in matches:
            u0, v0 = int(pt0[0]), int(pt0[1])
            u1, v1 = int(pt1[0]), int(pt1[1])
            cv2.circle(f0, (u0, v0), 1, (0,0,255), 2)
            #cv2.line(f1, (u0, v0), (u1, v1), (0,255,0), 2)
            cv2.circle(f1, (u1, v1), 1, (255, 0, 0), 2)
        f0, f1 = cv2.resize(f0, IMSHOW_SIZE), cv2.resize(f1, IMSHOW_SIZE)
        cv2.imshow('LEFT_VIEW', f0)
        cv2.imshow('RIGHT_VIEW', f1)
        cv2.waitKey(1)

class GET_OBJ_PTS:
    def __init__(self, K):
        self.K = K
        self.K_inverse = np.linalg.inv(self.K)
        # plot 3d
        self.window = pangolin.CreateWindowAndBind('3D SPACE', 1200, 800)
        gl.glEnable(gl.GL_DEPTH_TEST)
        # Define Projection and initial ModelView matrix
        self.scam = pangolin.OpenGlRenderState(
        pangolin.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.2, 100),
        pangolin.ModelViewLookAt(1, -1, -4, 1, 1, 1, pangolin.AxisDirection.AxisZ))
        self.handler = pangolin.Handler3D(self.scam)
        # Create Interactive View in window
        self.dcam = pangolin.CreateDisplay()
        self.dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0/480.0)
        self.dcam.SetHandler(self.handler)
        
    def fill1(self, x):
        return np.concatenate([x, np.ones((x.shape[0], 1))], axis = 1)

    def normalize(self, pts):
        return np.dot(self.K_inverse, self.fill1(pts).T).T[:, 0:2]

    def triangulate(self, pts0, pts1):
        proj_mat0 = np.zeros((3,4))
        proj_mat0[:, :3] = np.eye(3)
        proj_mat1 = np.concatenate([R, t.reshape(3, 1)], axis = 1)
        pts0, pts1 = self.normalize(pts0), self.normalize(pts1) 
        pts4d = cv2.triangulatePoints(proj_mat0, proj_mat1, pts0.T, pts1.T).T
        pts4d /= pts4d[:, 3:]
        goodZs = pts4d[:, 2] < 0
        out = pts4d[goodZs]
        out = np.delete(pts4d, 3, 1)
        return out
        
    def draw3d(self, out, cam_loc, vis_pose_check):
        # object points
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(1, 1, 1, 0)
        self.dcam.Activate(self.scam)
        # WORLD
        gl.glPointSize(3)
        gl.glColor3f(1.0, 0, 0)
        pangolin.DrawPoints(out)
        #POSE
        if vis_pose_check:
            for cam_loc1 in cam_loc:
                # cam pose
                gl.glColor3f(0, 1.0, 0)
                pose = np.identity(4)
                pose[:3, 3] = cam_loc1  #loc
                pangolin.DrawCamera(pose, 0.6, 0.4, 0.8)
        pangolin.FinishFrame()

