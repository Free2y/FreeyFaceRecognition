# -*- coding:utf-8 -*-
import base64
import json
import time
from io import BytesIO

from PIL.Image import Image
from flask import Flask, request
from flask_restful import Api, reqparse, Resource
from gevent import pywsgi

from FFRService import FFRService
from np_encoder import NpEncoder
import logging

logger = logging.getLogger('FFRService.' +__name__)
request_time = {}
now_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
max_post_time = 100
white_ips = []

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('imgbase64')
parser.add_argument('img_uri')

class FaceRecognition(Resource):
    def __init__(self):
        pass

    def post(self):
        start_time = time.time()
        global now_time
        global request_time
        args = parser.parse_args()
        imgbase64 = args['imgbase64']
        img_uri = args['img_uri']
        # 限制接口使用次数
        # time_now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        # time_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        # if time_day != now_time:
        #     now_time = time_day
        #     request_time = {}
        # remote_ip_now = request.remote_addr
        # print(remote_ip_now)
        # if remote_ip_now not in request_time :
        #     request_time[remote_ip_now] = 1
        # elif request_time[remote_ip_now] > max_post_time -1 and remote_ip_now not in white_ips:
        #     return json.dumps({'code': 999, 'msg': '已经超出免费使用次数'}, cls=NpEncoder)
        # else:
        #     request_time[remote_ip_now] += 1

        if img_uri is not None or imgbase64 is not None:
            try:
                if img_uri is None:
                    raw_image = base64.b64decode(imgbase64.encode('utf8'))
                    frames = Image.open(BytesIO(raw_image))
                else:
                    frames = img_uri

                results = ffrService.getFaceRecognitionResults(frames)
                print(results)
                # log_info = {
                #     'ip': request.remote_addr,
                #     'return': results,
                #     'time': time_now
                # }
                # logger.info(json.dumps(log_info, cls=NpEncoder))
                return json.dumps(
                {'code': 200, 'msg': '成功',
                 'data': {'raw_out': results,
                          'speed_time': round(time.time() - start_time, 2)}},
                cls=NpEncoder)
            except Exception as ex:
                error_log = json.dumps({'code': 400, 'msg': '产生了一点错误，请检查日志', 'err': str(ex)}, cls=NpEncoder)
                logger.error(error_log, exc_info=True)
                return error_log
        else:
            return json.dumps({'code': 400, 'msg': '没有传入参数'}, cls=NpEncoder)


class FaceDetection(Resource):
    def __init__(self):
        pass

    def post(self):
        start_time = time.time()
        global now_time
        global request_time
        args = parser.parse_args()
        imgbase64 = args['imgbase64']
        img_uri = args['img_uri']
        # 限制接口使用次数
        # time_now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        # time_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        # if time_day != now_time:
        #     now_time = time_day
        #     request_time = {}
        # remote_ip_now = request.remote_addr
        # print(remote_ip_now)
        # if remote_ip_now not in request_time :
        #     request_time[remote_ip_now] = 1
        # elif request_time[remote_ip_now] > max_post_time -1 and remote_ip_now not in white_ips:
        #     return json.dumps({'code': 999, 'msg': '已经超出免费使用次数'}, cls=NpEncoder)
        # else:
        #     request_time[remote_ip_now] += 1

        if img_uri is not None or imgbase64 is not None:
            try:
                if img_uri is None:
                    raw_image = base64.b64decode(imgbase64.encode('utf8'))
                    frames = Image.open(BytesIO(raw_image))
                else:
                    frames = img_uri

                results = ffrService.getFaceRecognitionResults(frames)
                print(results)
                # log_info = {
                #     'ip': request.remote_addr,
                #     'return': results,
                #     'time': time_now
                # }
                # logger.info(json.dumps(log_info, cls=NpEncoder))
                return json.dumps(
                {'code': 200, 'msg': '成功',
                 'data': {'raw_out': results,
                          'speed_time': round(time.time() - start_time, 2)}},
                cls=NpEncoder)
            except Exception as ex:
                error_log = json.dumps({'code': 400, 'msg': '产生了一点错误，请检查日志', 'err': str(ex)}, cls=NpEncoder)
                logger.error(error_log, exc_info=True)
                return error_log
        else:
            return json.dumps({'code': 400, 'msg': '没有传入参数'}, cls=NpEncoder)

# 设置路由
api.add_resource(FaceRecognition, '/face_recognition')
api.add_resource(FaceDetection, '/face_detection')

if __name__ == '__main__':
    print('正在启动服务......')
    ffrService = FFRService()
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    print('服务已经启动')
    server.serve_forever()
