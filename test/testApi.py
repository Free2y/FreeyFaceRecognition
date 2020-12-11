
import cv2
import requests

from tools.mat_base64_cov import img_to_base64,frame_to_base64

def showFrame(frame,faces,type=0):

    #print(results)
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    for face in faces:
        if type == 0:
            face_box = face['face_box']
            eyes = face['eyes']
            cv2.rectangle(frame, (face_box['x1'], face_box['y1']), (face_box['x2'], face_box['y2']), (171, 207, 49), int(round(frameHeight / 240)), 8)
            for eye in eyes:
                cv2.rectangle(frame, (eye['ex'], eye['ey']), (eye['ex'] + eye['ew'], eye['ey'] + eye['eh']), (0, 255, 0), 1)
        elif type == 1:
            face_box = face['face_box']
            eyes = face['eyes']
            name = face['name']
            cv2.rectangle(frame, (face_box['x1'], face_box['y1']), (face_box['x2'], face_box['y2']), (171, 207, 49), int(round(frameHeight / 240)), 8)
            for eye in eyes:
                cv2.rectangle(frame, (eye['ex'], eye['ey']), (eye['ex'] + eye['ew'], eye['ey'] + eye['eh']), (0, 255, 0), 1)
            cv2.putText(frame, name, (face_box['x1'], face_box['y1']-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (171, 207, 49), 1, cv2.LINE_AA)
        cv2.imshow('frame', frame)

if __name__ == '__main__':

    host = 'http://127.0.0.1'
    ser_url = host+':5678/api/fdrService/faceDRecognition'
    type = 1
    # frame = cv2.imread('./face.jpg')
    # img_b64 = img_to_base64('./face.jpg')
    # res = requests.post(url=ser_url,data={'imgbase64':img_b64})
    # r = res.json()
    # print(r)
    # result = r['result']
    # faces = result['faces']
    # print(result['speed_time'])
    # if len(faces) == 0:
    #     print("没有检查到人脸")
    # else:
    #     print("检查到人脸。。。。")
    # showFrame(frame,raw_out,type)
    # cv2.waitKey(0)
    video_capture = cv2.VideoCapture('https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=232249614,3151086243&fm=26&gp=0.jpg')
    while True:
        flag, frame = video_capture.read()
        if flag:
            res = requests.post(url=ser_url,data={'type':type,'img_uri':'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=232249614,3151086243&fm=26&gp=0.jpg'})
            print(res)
            r = res.json()
            print(r)
            result = r['result']
            faces = result['faces']
            print(result['speed_time'])

            showFrame(frame,faces,type)
            cv2.waitKey(0)
            # cv2.waitKey(1)
        else:
            break

    cv2.destroyAllWindows()

