import json

import cv2
import requests

from tools.mat_base64_cov import img_to_base64,frame_to_base64

def showFrame(frame,raw_out,type):

    #print(results)
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    for results in raw_out:
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

if __name__ == '__main__':
    type = 0
    fd_url = 'http://127.0.0.1:5678/api/face_detection'
    fr_url = 'http://127.0.0.1:5678/api/face_recognition'
    if type == 0:
        url = fd_url
    elif type == 1:
        url = fr_url
    # img_b64 = img_to_base64('./face.jpg')
    # res = requests.post(url=url,data={'imgbase64':img_b64})
    # print(res.text)
    # result = json.loads(res.json())
    # raw_data = result['data']
    # print(raw_data)
    # raw_out = raw_data['raw_out']
    # if len(raw_out) == 0:
    #     print("没有检查到人脸")
    # else:
    #     print("检查到人脸。。。。")
    #
    # frame = cv2.imread('./face.jpg')
    # showFrame(frame,raw_out,type)
    # cv2.waitKey(0)
    video_capture = cv2.VideoCapture(
        'https://hmfsimg.chci.cn/hmfs/v/dzbbbk/NTE3MzEwNjgwMzE1MTg3Mg==.mp4')

    # 视频
    while True:
        flag, frame = video_capture.read()
        if flag:
            img_b64 = frame_to_base64(frame)
            res = requests.post(url=url,data={'imgbase64':img_b64})
            result = json.loads(res.json())
            raw_data = result['data']
            raw_out = raw_data['raw_out']
            print(raw_data['speed_time'])

            showFrame(frame,raw_out,type)
            cv2.waitKey(1)
        else:
            break

    cv2.destroyAllWindows()

