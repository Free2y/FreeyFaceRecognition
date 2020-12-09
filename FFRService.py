#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

from EigenfacesModel import EigenfacesModel
from FreeyFaceDetection import FreeyFaceDetection
from FreeyFaceRecognize import FreezyFaceDR


class FFRService:

    def __init__(self):
        efm = EigenfacesModel(m_path='./models')
        face_detector = FreeyFaceDetection()
        self.ffdr = FreezyFaceDR(face_detector, efm)

    def getFaceDetectionResults(self,frames):
        video_capture = cv2.VideoCapture(frames)
        responses = []
        type = 0
        while True:
            flag, frame = video_capture.read()
            if flag:
                results = self.ffdr.drSingleFrame(frame,type)
                responses.append(results)
            else:
                break
        return responses

    def getFaceRecognitionResults(self,frames):
        video_capture = cv2.VideoCapture(frames)
        responses = []
        type = 1
        while True:
            flag, frame = video_capture.read()
            if flag:
                results = self.ffdr.drSingleFrame(frame,type)
                responses.append(results)
            else:
                break
        return responses

