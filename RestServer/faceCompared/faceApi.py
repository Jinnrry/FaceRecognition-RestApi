# -*- coding: utf-8 -*-
import os
import sys
from config import config
root=config.Config.root
caffe_root=config.Config.caffe_root
sys.path.insert(0, caffe_root + 'python')
import random
import skimage
import numpy as np
import caffe
import sklearn.metrics.pairwise as pw
import time
import cv2
from django.http import HttpResponse
# GPU加速
caffe.set_device(0)
caffe.set_mode_gpu()

# 加载caffe模型
global net
try:

    net = caffe.Net(root + 'model/vgg/deploy.prototxt'
                       , root + 'model/vgg/VGG_FACE.caffemodel'
                       , caffe.TEST)
except:
    print("请先下载VGG FACE神经网络模型，详情请看model/vgg/README.md")
    exit();


# 提取特征数组
def get_feature(path1):
    global net
    # 加载图片
    X = read_image(path1)
    test_num = np.shape(X)[0]

    # X  作为 模型的输入
    out = net.forward(data=X)
    # print out.keys()


    feature1 = np.float64(out["fc7"])
    feature1 = np.reshape(feature1, (test_num, 4096))
    # 加载注册图片
    return feature1


# 保存上传文件
def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

#图片预处理
def read_image(filename):
    averageImg = [129.1863, 104.7624, 93.5940]
    X = np.empty((1, 3, 224, 224))
    im1 = skimage.io.imread(filename, as_grey=False)
    # 归一化
    image = skimage.transform.resize(im1, (224, 224)) * 255
    X[0, 0, :, :] = image[:, :, 0] - averageImg[0]
    X[0, 1, :, :] = image[:, :, 1] - averageImg[1]
    X[0, 2, :, :] = image[:, :, 2] - averageImg[2]
    return X


# api返回函数
def compared(request):
    if request.method == 'POST':
        if len(request.FILES) != 2:
            return HttpResponse('{"status":false,"data":"","msg":"图片参数错误！"}')
        starttime = time.time()
        name1 = str(random.randint(10000, 99999)) + str(time.time())  # 随机名字
        name2 = str(random.randint(10000, 99999)) + str(time.time())

        handle_uploaded_file(request.FILES['face1'], str(name1))
        handle_uploaded_file(request.FILES['face2'], str(name2))

        tz1 = get_feature(root + "RestServer/upload/" + str(name1))

        tz2 = get_feature(root + "RestServer/upload/" + str(name2))

        comparedValue = pw.cosine_similarity(tz1, tz2)[0][0]

        os.remove(root + "RestServer/upload/" + str(name1))
        os.remove(root + "RestServer/upload/" + str(name2))
        endtime = time.time()
        Runtime=endtime-starttime
        return HttpResponse('{"status":true,"data":"' + str(comparedValue) + '","msg":"成功","runtime": ' + str(Runtime) + '  }')
    else:
        return HttpResponse('{"status":false,"data":"","msg":"请求不合法"}')
    return HttpResponse('{"status":false,"data":"","msg":"未知错误"}')

def comparedByFaceID(request):
    if request.method=='POST':
        if request.POST['faceID1']  and request.POST['faceID2'] :
            tz1=request.POST['faceID1'][2:-2]
            tz2=request.POST['faceID2'][2:-2]
            tz1=[tz1.split(",")]
            tz2=[tz2.split(",")]
            faceID1=np.float64(tz1)
            faceID2=np.float64(tz2)
            com=pw.cosine_similarity(faceID1, faceID2)[0][0]
            return HttpResponse('{"status":true,"data":'+str(com)+',"msg":"成功！"}')
    return HttpResponse('{"status":false,"data":"","msg":"失败！"}')

def faceid(request):
    if request.method == 'POST':
        if len(request.FILES) != 1:
            return HttpResponse('{"status":false,"data":"","msg":"图片参数错误！"}')
        starttime = time.time()
        name = str(random.randint(10000, 99999)) + str(time.time())  # 随机名字
        handle_uploaded_file(request.FILES['pic'], str(name))
        tz = get_feature(root + "RestServer/upload/" + str(name))
        endtime = time.time()
        Runtime=endtime-starttime
        return HttpResponse('{"status":true,"data":' + str(tz.tolist()) + ',"msg":"成功","runtime": '+ str(Runtime) +'  }')
    else:
        return HttpResponse('{"status":false,"data":"","msg":"请求不合法"}')
    return HttpResponse('{"status":false,"data":"","msg":"未知错误"}')



#获取图片中人脸的位置
def detectFaces(image_name):
    starttime=time.time()
    img = cv2.imread(image_name)
    face_cascade = cv2.CascadeClassifier(root+"model/haarcascade_frontalface_default.xml")
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img #if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)#1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
    result = "["

    for (x,y,width,height) in faces:
        result+=  '{ "x":'+ str(x) +' ,"y":'+ str(y) +' ,"height":'+ str(height)+',"width":'+ str(width)+' } ' +','

    endtime=time.time()

    result=result[:-1]+']'

    return '{"status":true, "data":'+ result +' ,"msg":"成功","runtime":'+ str(endtime-starttime)+'}'

#api返回函数
def locate(request):
    if request.method == 'POST':
        if len(request.FILES) != 1:
            return HttpResponse('{"status":false,"data":"","msg":"图片参数错误！"}')
        name = str(random.randint(10000, 99999)) + str(time.time())  # 随机保存图片的名字
        handle_uploaded_file(request.FILES['pic'], str(name))
        returnData= HttpResponse(detectFaces(root+"RestServer/upload/"+name))
        os.remove(root + "RestServer/upload/" + str(name))

        return returnData