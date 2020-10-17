import cv2
import numpy as np
import OpenGL.GL as gl
import pangolin
from CLASSES import GET_IMG_PTS, GET_OBJ_PTS, GET_POSE
from params import K, W, H
import time

class odom:
    def __init__(self, K, W, H, cam0, cam1, vis2d_check, vis3d_check, posevis_check):
        # cam params
        self.K = K
        self.W = W
        self.H = H
        # cams
        self.cam0 = cam0
        self.cam0.set(cv2.CAP_PROP_EXPOSURE, 40) # decrease motion blur
        self.cam1 = cam1
        self.cam1.set(cv2.CAP_PROP_EXPOSURE, 40) # decrease motion blur
        # foos
        self.GET_IMG_PTS = GET_IMG_PTS()
        self.GET_OBJ_PTS = GET_OBJ_PTS(self.K)
        self.GET_POSE = GET_POSE()
        # checks
        self.cpose = bool(posevis_check)
        self.c2d = bool(vis2d_check)
        self.c3d = bool(vis3d_check)

    def doshit(self, f0, f1):
        pts0, pts1 = self.GET_IMG_PTS.calc_fs(f0, f1)
        out = self.GET_OBJ_PTS.triangulate(pts0, pts1)
        #pose = self.GET_POSE.calc_pose()
        pose = [55, 55, 55] # dummy till fix
        if self.c2d:
            self.GET_IMG_PTS.draw2d(zip(pts0, pts1), f0, f1)

        if self.c3d:
            self.GET_OBJ_PTS.draw3d(out, pose, self.cpose)
        
    def feed_doshit(self): 
        while True:
            c0, f0 = self.cam0.read()
            c1, f1 = self.cam1.read()
            f0 = cv2.resize(f0, (self.W, self.H))
            f1 = cv2.resize(f1, (self.W, self.H))
            if c0 and c1:
                self.doshit(f0, f1)
                #cv2.imshow('f0', f0)
                #cv2.imshow('f1', f1)
                #cv2.waitKey(1)
       
if __name__ == "__main__":
    cam0, cam1 = cv2.VideoCapture(2), cv2.VideoCapture(4)
    c = odom(K, W, H, cam0, cam1, 1, 1, 1)
    c.feed_doshit()
                

