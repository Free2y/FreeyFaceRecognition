#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2

from FreeyFaceDetection import FreeyFaceDetection


class GetAndSaveFace:

    def __init__(self, face_detection, inpath='./data/imgs', outpath='./data/t_faces'):
        self.face_detection = face_detection
        self.inpath = inpath
        self.outpath = outpath

    def saveFaceImg(self, img, file_path, filename):
        bboxes = self.face_detection.detectFaceOpenCVDnn(img)
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]
        if len(bboxes) == 0:
            print('抱歉，未检测到人脸')
        else:
            for box,eyes in bboxes:
                saveimg = img[box[1]:box[3], box[0]:box[2]]
                # cv2.imshow("Face Detection Comparison", saveimg)
                # cv2.waitKey(0)
                cv2.imwrite(os.path.join(file_path, filename), saveimg)

    def loadOriginImgs(self):
        dirs = os.listdir(self.inpath)
        print(dirs)
        for dir in dirs:
            file_path = self.outpath + "/%s" % str(dir)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            for parentdir, dirname, filenames in os.walk(os.path.join(self.inpath, dir)):
                print(parentdir, dirname, filenames)
                for filename in filenames:
                    image = cv2.imread(os.path.join(self.inpath, dir, filename))
                    self.saveFaceImg(image, file_path, filename)

    def run(self):
        print('start run from ' + self.inpath)
        self.loadOriginImgs()
        print('save end to ' + self.outpath)


if __name__ == '__main__':
    inpath = './data/imgs'
    outpath = './data/t_faces'
    ffd = FreeyFaceDetection()
    GetAndSaveFace(ffd, inpath, outpath).run()
