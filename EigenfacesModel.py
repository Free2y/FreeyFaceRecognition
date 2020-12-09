#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np
import pickle


class EigenfacesModel:

    def __init__(self, t_path='./data/t_faces', m_path='./models'):
        self.t_path = t_path
        self.m_path = m_path

    def loadFacesTrainData(self):
        dirs = os.listdir(self.t_path)
        print(dirs)
        train_data = []
        train_data_detail = []
        train_label = []
        type = 0
        for dir in dirs:
            for parentdir, dirname, filenames in os.walk(os.path.join(self.t_path, dir)):
                # print(parentdir,dirname,filenames)
                for filename in filenames:
                    image = cv2.imread(os.path.join(self.t_path, dir, filename))
                    image = cv2.resize(image, dsize=(200, 200))
                    gray = cv2.cvtColor(image, code=cv2.COLOR_BGR2GRAY)
                    # print("读取",gray.shape)
                    if len(str(image)) != 0:
                        # print("加入。。。。")
                        train_data.append(gray)
                        train_label.append(type)
                        train_data_detail.append(filename)
            type += 1
        return [train_data, train_label, train_data_detail, dirs]

    def trainModel(self):
        train_data, train_label, train_data_detail, dirs = self.loadFacesTrainData()
        print("dirs=", dirs)

        # asarray都可以将结构数据转化为ndarray
        X = np.asarray(train_data)
        Y = np.asarray(train_label)
        names = np.asarray(train_data_detail)
        # 产生一个随机数 -
        index = [i for i in range(0, len(X))]
        # 现场修改序列，改变自身内容。（类似洗牌，打乱顺序）
        np.random.shuffle(index)
        print("***********", index)
        # 打乱顺序 :相同规则打乱
        X = X[index]
        Y = Y[index]
        N = names[index]
        # 训练数据
        print("训练数据为：", len(X), len(Y))
        X_train = X[:-5]
        Y_train = Y[:-5]
        # 算法Eigen 特征的意思
        # 主成分分析（PCA）——Eigenfaces（特征脸）——函数：cv2.face.EigenFaceRecognizer_create
        model = cv2.face.EigenFaceRecognizer_create()
        print(model)
        print("算法学习", len(X_train), len(Y_train))
        model.train(X_train, Y_train)
        print("已经学会了数据。。。。")
        # 测试数据
        X_test, Y_test, N_test = X[-5:], Y[-5:], N[-5:]

        # 开始验证
        index = 0
        for data in X_test:
            # print(data)
            result = model.predict(data)
            print("=================")
            print(result)
            print(N_test[index], dirs[result[0]])
            index += 1
        return model, dirs

    def saveModel(self):
        model, types = self.trainModel()
        with open(self.m_path + '/freezyfd_model_v1.pkl', 'wb') as file:
            pickle.dump(types, file)
        model.write(self.m_path + '/freezyfd_model_v1.xml')

    def loadModel(self):
        if os.path.exists(self.m_path + '/freezyfd_model_v1.pkl') and os.path.exists(
                self.m_path + '/freezyfd_model_v1.xml'):
            with open(self.m_path + '/freezyfd_model_v1.pkl', 'rb') as file:
                types = pickle.load(file)
            model = cv2.face.EigenFaceRecognizer_create()
            model.read(self.m_path + '/freezyfd_model_v1.xml')
            return model, types
        else:
            print('此路径没有符合模型')


if __name__ == '__main__':
    EigenfacesModel().saveModel()
