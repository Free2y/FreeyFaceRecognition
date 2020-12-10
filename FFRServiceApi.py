# -*- coding:utf-8 -*-
import json
import os
import time

from flask import Flask, request
from flask_restful import Api, reqparse, Resource
from gevent import pywsgi

from FFRService import FFRService
from tools.np_encoder import NpEncoder
import logging

logger = logging.getLogger('FFRService.' + __name__)
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = './logs/'
if not os.path.exists(log_path):
    os.makedirs(log_path)
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)

request_time = {}
now_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
max_post_time = 100
white_ips = []

app = Flask(__name__)
app.config['RESTFUL_JSON'] = {'cls':NpEncoder,'ensure_ascii':False}
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('imgbase64')
parser.add_argument('img_uri')

def fromatJsonDumps(data):
    return json.dumps(data,cls=NpEncoder,ensure_ascii=False)

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
        type = 1
        # 限制接口使用次数
        time_now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        # time_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        # if time_day != now_time:
        #     now_time = time_day
        #     request_time = {}
        # remote_ip_now = request.remote_addr
        # print(remote_ip_now)
        # if remote_ip_now not in request_time :
        #     request_time[remote_ip_now] = 1
        # elif request_time[remote_ip_now] > max_post_time -1 and remote_ip_now not in white_ips:
        #     return {'code': 999, 'msg': '已经超出免费使用次数'}
        # else:
        #     request_time[remote_ip_now] += 1

        if img_uri is not None or imgbase64 is not None:
            try:
                if img_uri is None:
                    results = ffrService.getFaceDRResultsByBase64(imgbase64, type)
                else:
                    results = ffrService.getFaceDRResultsByUri(img_uri, type)
                #print(results)
                log_info = {
                    'ip': request.remote_addr,
                    'return': results,
                    'time': time_now
                }
                logger.info(fromatJsonDumps(log_info))
                return {'code': 0, 'message': '成功',
                     'result': {'raw_out': results,
                              'speed_time': round(time.time() - start_time, 2)}}
            except Exception as ex:
                error_log = {'code': -1, 'message': '产生了一点错误，请检查日志', 'result': str(ex)}
                logger.error(error_log, exc_info=True)
                return error_log
        else:
            return {'code': -1, 'message': '没有传入参数'}


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
        type = 0
        # 限制接口使用次数
        time_now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        # time_day = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        # if time_day != now_time:
        #     now_time = time_day
        #     request_time = {}
        # remote_ip_now = request.remote_addr
        # print(remote_ip_now)
        # if remote_ip_now not in request_time :
        #     request_time[remote_ip_now] = 1
        # elif request_time[remote_ip_now] > max_post_time -1 and remote_ip_now not in white_ips:
        #     return {'code': 999, 'msg': '已经超出免费使用次数'}
        # else:
        #     request_time[remote_ip_now] += 1

        if img_uri is not None or imgbase64 is not None:
            try:
                if img_uri is None:
                    results = ffrService.getFaceDRResultsByBase64(imgbase64, type)
                else:
                    results = ffrService.getFaceDRResultsByUri(img_uri, type)
                #print(results)
                log_info = {
                    'ip': request.remote_addr,
                    'return': results,
                    'time': time_now
                }
                logger.info(fromatJsonDumps(log_info))
                return {'code': 0, 'message': '成功',
                     'result': {'raw_out': results,
                              'speed_time': round(time.time() - start_time, 2)}}
            except Exception as ex:
                error_log = {'code': -1, 'message': '产生了一点错误，请检查日志', 'result': str(ex)}
                logger.error(error_log, exc_info=True)
                return error_log
        else:
            return {'code': -1, 'message': '没有传入参数'}


# 设置路由
api.add_resource(FaceRecognition, '/api/face_recognition')
api.add_resource(FaceDetection, '/api/face_detection')

if __name__ == '__main__':
    print('正在启动服务......')
    logger.info('正在启动服务......')
    ffrService = FFRService()
    server = pywsgi.WSGIServer(('0.0.0.0', 5678), app)
    print('服务已经启动')
    logger.info('服务已经启动')
    server.serve_forever()
