#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

from EigenfacesModel import EigenfacesModel
from FreeyFaceDetection import FreeyFaceDetection


class FreezyFaceDR():

    def __init__(self, fdd, efm):
        self.face_detector = fdd
        self.model, self.types = efm.loadModel()

    def drSingleFrame(self, frame, type):
        bboxes = self.face_detector.detectFaceOpenCVDnn(frame)
        # print(frame.shape)
        if len(bboxes) == 0:
            print("没有检查到人脸")
        else:
            print("检查到人脸。。。。")

        if type == 0:
            return bboxes
        elif type == 1:
            results = []
            # for循环遍历数据
            for box,eyes in bboxes:
                face = frame[box[1]:box[3], box[0]:box[2]]
                face = cv2.resize(face, dsize=(200, 200))
                gray = cv2.cvtColor(face, code=cv2.COLOR_BGR2GRAY)
                # 开始对比
                print("~~~~" * 20)
                result = self.model.predict(gray)
                print('Label:%s,confidence:%.2f' % (result[0], result[1]))
                name = self.types[result[0]]
                print('该预测人脸是：', name)
                if result[1] > 5000:
                    name = "Other"
                print('该人脸是：', name)
                results.append((box,eyes,name))
            return results


def showSingleFrame(frame, scale=1):
    # SingleFrame Example ==============================================
    frame = cv2.resize(frame, (int(frame.shape[1] * scale),int(frame.shape[0] * scale)), interpolation=cv2.INTER_LINEAR)
    results = ffdr.drSingleFrame(frame,type)
    #print(results)
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    if len(results) == 0:
        print("没有检查到人脸")
    else:
        print("检查到人脸。。。。")
    if type == 0:
        for box,eyes in results:
            img = cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (171, 207, 49), int(round(frameHeight / 240)), 8)
            face_img = img[box[1]:box[3], box[0]:box[2]]
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face_img, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
    elif type == 1:
        for box,eyes,text in results:
            img = cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (171, 207, 49), int(round(frameHeight / 240)), 8)
            # face_img = img[box[1]:box[3], box[0]:box[2]]
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (ex+box[0], ey+box[1]), (ex+box[0] + ew, ey+box[1] + eh), (0, 255, 0), 1)
            cv2.putText(frame, text, (box[0], box[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (171, 207, 49), 1, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    # SingleFrame Example ==============================================

if __name__ == '__main__':

    efm = EigenfacesModel(m_path='./models')
    video_capture = cv2.VideoCapture(
        './test/face.jpg')
    face_detector = FreeyFaceDetection()
    type = 1
    ffdr = FreezyFaceDR(face_detector, efm)
    # 图片
    frame = cv2.imread('./test/face.jpg')
    showSingleFrame(frame)
    cv2.waitKey(0)
    # 视频
    # while True:
    #     flag, frame = video_capture.read()
    #     if flag:
    #         showSingleFrame(frame, 0.5)
    #         cv2.waitKey(1)
    #     else:
    #         break

    cv2.destroyAllWindows()
