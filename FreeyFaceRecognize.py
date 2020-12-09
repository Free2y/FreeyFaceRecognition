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
        print(frame.shape)
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        if len(bboxes) == 0:
            print("没有检查到人脸")
        else:
            print("检查到人脸。。。。")

        if type == 0:
            return bboxes
        elif type == 1:
            results = []
            # for循环遍历数据
            for i in bboxes:
                if 0 <= i[1] <= frameHeight and 0 <= i[3] <= frameHeight and 0 <= i[0] <= frameWidth and 0 <= i[
                    2] <= frameWidth:
                    face = frame[i[1]:i[3], i[0]:i[2]]
                    # cv2.imwrite('./face'+str(index)+'.jpg',face)
                    face = cv2.resize(face, dsize=(200, 200))
                    gray = cv2.cvtColor(face, code=cv2.COLOR_BGR2GRAY)
                    # 开始对比
                    print("~~~~" * 20)
                    result = self.model.predict(gray)
                    print('Label:%s,confidence:%.2f' % (result[0], result[1]))
                    text = self.types[result[0]]
                    print('该预测人脸是：', text)
                    if result[1] > 5000:
                        text = "Other"
                    print('该人脸是：', text)
                    results.append([i, text])
                else:
                    print('识别超出监测图片范围')
                    text = "out of range"
                    results.append([i, text])
            return results


def testSingleFrame(frame, scale=1):
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
        for i in results:
            cv2.rectangle(frame, (i[0], i[1]), (i[2], i[3]), (171, 207, 49), int(round(frameHeight / 240)), 8)
            face_img = frame[i[1]:i[3], i[0]:i[2]]
            for (ex, ey, ew, eh) in i[4]:
                cv2.rectangle(face_img, (ex, ey), (ex + ew, ey + eh), (171, 207, 49), 2)
    elif type == 1:
        for i, text in results:
            cv2.rectangle(frame, (i[0], i[1]), (i[2], i[3]), (171, 207, 49), int(round(frameHeight / 240)), 8)
            face_img = frame[i[1]:i[3], i[0]:i[2]]
            for (ex, ey, ew, eh) in i[4]:
                cv2.rectangle(face_img, (ex, ey), (ex + ew, ey + eh), (171, 207, 49), 2)
            cv2.putText(frame, text, (i[0], i[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (171, 207, 49), 1, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    # SingleFrame Example ==============================================

if __name__ == '__main__':

    efm = EigenfacesModel(m_path='./models')
    video_capture = cv2.VideoCapture(
        'https://hmfsimg.chci.cn/hmcs-pros/captureVisit/zd5m8yJc64fAkoc5rk4sYg66/original.mp4')
    face_detector = FreeyFaceDetection()
    type = 1
    ffdr = FreezyFaceDR(face_detector, efm)
    # 图片
    frame = cv2.imread('./test/face.jpg')
    testSingleFrame(frame)
    cv2.waitKey(0)
    # 视频
    # while True:
    #     flag, frame = video_capture.read()
    #     if flag:
    #         testSingleFrame(frame, 0.5)
    #         cv2.waitKey(1)
    #     else:
    #         break

    cv2.destroyAllWindows()
