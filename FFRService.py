#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from tools.mat_base64_cov import base64_to_frame
from EigenfacesModel import EigenfacesModel
from FreeyFaceDetection import FreeyFaceDetection
from FreeyFaceRecognize import FreezyFaceDR


class FFRService:

    def __init__(self):
        efm = EigenfacesModel(m_path='./models')
        face_detector = FreeyFaceDetection()
        self.ffdr = FreezyFaceDR(face_detector, efm)

    def getFaceDRResultsByUri(self,frames,type):
        video_capture = cv2.VideoCapture(frames)
        responses = []
        while True:
            flag, frame = video_capture.read()
            if flag:
                results = self.ffdr.drSingleFrame(frame,type)
                responses.append(results)
            else:
                break
        return responses


    def getFaceDRResultsByBase64(self,imageBase64,type):
        responses = []
        frame = base64_to_frame(imageBase64)
        results = self.ffdr.drSingleFrame(frame,type)
        responses.append(results)

        return responses
