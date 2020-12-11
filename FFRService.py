#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
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
        return self.formatJsonFaces(responses,type)


    def getFaceDRResultsByBase64(self,imageBase64,type):
        responses = []
        frame = base64_to_frame(imageBase64)
        results = self.ffdr.drSingleFrame(frame,type)
        responses.append(results)

        return self.formatJsonFaces(responses,type)

    def getFaceDRResultsByFile(self,file,type):
        responses = []
        file_bytes = file.read()
        #print(file_bytes)
        image = cv2.imdecode(np.asarray(bytearray(file_bytes),dtype='uint8'), cv2.IMREAD_COLOR)
        # cv2.imshow("a",image)
        # cv2.waitKey(0)
        results = self.ffdr.drSingleFrame(image,type)
        responses.append(results)

        return self.formatJsonFaces(responses,type)

    def getFaceDRResultsByFiles(self,files,type):
        responses = []
        for file in files:
            file_bytes = file.read()
            #print(file_bytes)
            image = cv2.imdecode(np.asarray(bytearray(file_bytes),dtype='uint8'), cv2.IMREAD_COLOR)
            # cv2.imshow("a",image)
            # cv2.waitKey(0)
            results = self.ffdr.drSingleFrame(image,type)
            responses.append(results)

        return self.formatJsonFaces(responses,type)


    def formatJsonFaces(self,results,type):
        faces = []
        for frame in results:
            #print(frame)
            if type == 1:
                for box,eyes,name in frame:
                    json_eyes = []
                    for (ex, ey, ew, eh) in eyes:
                        json_eyes.append({'ex':ex+box[0],'ey':ey+box[1],'ew':ew,'eh':eh})
                    faces.append({"face_box": {'x1':box[0],'y1':box[1],'x2':box[2],'y2':box[3]},'eyes':json_eyes,'name':name})
            else:
                for box,eyes in frame:
                    json_eyes = []
                    for (ex, ey, ew, eh) in eyes:
                        json_eyes.append({'ex':ex+box[0],'ey':ey+box[1],'ew':ew,'eh':eh})
                    faces.append({"face_box": {'x1':box[0],'y1':box[1],'x2':box[2],'y2':box[3]},'eyes':json_eyes})
        return faces
