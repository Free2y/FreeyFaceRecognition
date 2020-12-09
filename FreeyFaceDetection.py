#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import cv2


class FreeyFaceDetection:
    # 加载人脸检测器
    modelFile = "./models/opencv_face_detector_uint8.pb"
    configFile = "./models/opencv_face_detector.pbtxt"
    net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
    conf_threshold = 0.7

    # def __init__(self,net,conf_threshold):
    #     self.net = net
    #     self.conf_threshold = conf_threshold

    def detectFaceOpenCVDnn(self, frame):

        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        # print(frameWidth,frameHeight)
        self.net.setInput(blob)
        detections = self.net.forward()
        # print(detections)
        bboxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                bboxes.append([x1, y1, x2, y2])

        return bboxes

    def faceDetectionOnce(self, img):
        bboxes = self.detectFaceOpenCVDnn(img)
        frameHeight = img.shape[0]
        if len(bboxes) == 0:
            print('抱歉，未检测到人脸')
        else:
            for i in bboxes:
                img = cv2.rectangle(img, (i[0], i[1]), (i[2], i[3]), (171, 207, 49), int(round(frameHeight / 240)), 8)
        print(bboxes)
        cv2.imshow("Face Detection Comparison", img)
        cv2.waitKey(0)


if __name__ == '__main__':
    ffd = FreeyFaceDetection()
    img = cv2.imread('./test/face.jpg')
    ffd.faceDetectionOnce(img)
