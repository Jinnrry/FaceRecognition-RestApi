# -*- coding: utf-8 -*-
import skimage
import numpy as np
import caffe
import cv2
import pickle
import sklearn.metrics.pairwise as pw

import redis

import Tools

#GPU加速
caffe.set_mode_gpu()

def getFaceArray(img):
    #注意,haarcascade_frontalface_default.xml文件需要使用绝对路径
    face_cascade=cv2.CascadeClassifier("/home/jiangwei/下载/faceRead/haarcascade_frontalface_default.xml")
    if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
            gray = img  #if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)#1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
    result = []
    for (x,y,width,height) in faces:
            result.append((x,y,x+width,y+height))

    return result
    # if(len(result)>0):
    #     # for r in result:
    #         # img2=cv2.rectangle(img, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 3)
    #         # img3=img[r[1]:r[3], r[0]:r[2]]  # 得到视频中的人脸，使用识别
    #
    #     return result
    #
    # return []

#识别人脸是谁
def readFace(feature):

    r=redis.Redis("localhost")
    keys= r.keys("*")
    for key in keys :
        db_feature =pickle.loads( r.lindex(key,0) )
        comple=pw.cosine_similarity(db_feature,feature)
        if(comple>0.46) :  #是同一个人
            return key
    for key in keys :
        if(r.llen(key))>1 :
            db_feature =pickle.loads( r.lindex(key,1) )
            comple=pw.cosine_similarity(db_feature,feature)
            if(comple>0.46) :  #是同一个人
                return key
    return 'unknow'





#识别图片中的人脸
def photoRead(filename):
    frame = cv2.imread(filename)

    FaceArray = getFaceArray(frame)

    for r in FaceArray:
        img2 = cv2.rectangle(frame, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 3)
        img3 = frame[r[1]:r[3], r[0]:r[2]]  # 得到视频中的人脸，使用识别
        feature = Tools.get_feature(img3)
        name = readFace(feature)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img2 = cv2.putText(img2, name, (r[1], r[3]), font, 1, (255, 255, 255), 2)


    cv2.imshow('frame', frame)
    cv2.waitKey(0)



def start():
    cap = cv2.VideoCapture(0)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        FaceArray=getFaceArray(frame)
        img2=frame
        for r in FaceArray :
            img2=cv2.rectangle(frame, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 3)
            img3 = frame[r[1]:r[3], r[0]:r[2]]  # 得到视频中的人脸，使用识别
            feature=Tools.get_feature(img3)
            name=readFace(feature)
            font=cv2.FONT_HERSHEY_SIMPLEX
            img2= cv2.putText(img2,name,(r[1],r[3]), font, 1,(255,255,255),2)

        cv2.imshow('frame',img2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


