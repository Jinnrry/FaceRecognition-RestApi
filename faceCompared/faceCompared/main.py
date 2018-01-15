# -*- coding: utf-8 -*-
caffe_root = "d:\\caffe\\"

import sys
sys.path.insert(0, caffe_root + 'python')

import random
import skimage
import numpy as np
import os
import caffe
import sklearn.metrics.pairwise as pw
import time
from django.http import HttpResponse

root = "E:/faceapi/"

# GPU加速
caffe.set_device(0)
caffe.set_mode_gpu()

# 加载caffe模型
global net
net = caffe.Net(root + 'faceapi/faceCompared/faceCompared/deploy.prototxt'
                       , root + 'faceapi/faceCompared/faceCompared/model.caffemodel'
                       , caffe.TEST)


# 提取特征数组
def get_feature(path1):
    global net
    # 加载图片
    X = read_image(path1)
    test_num = np.shape(X)[0]
    starttime = time.time()
    # X  作为 模型的输入
    out = net.forward(data=X)
    # print out.keys()
    endtime = time.time()
    print ("前向传播时间：",(endtime - starttime))
    feature1 = np.float64(out["fc7"])
    feature1 = np.reshape(feature1, (test_num, 4096))
    # 加载注册图片
    return feature1


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

        name1 = str(random.randint(10000, 99999)) + str(time.time())  # 随机名字
        name2 = str(random.randint(10000, 99999)) + str(time.time())

        handle_uploaded_file(request.FILES['face1'], str(name1))
        handle_uploaded_file(request.FILES['face2'], str(name2))

        tz1 = get_feature(root + "faceapi/faceCompared/upload/" + str(name1))

        tz2 = get_feature(root + "faceapi/faceCompared/upload/" + str(name2))

        comparedValue = pw.cosine_similarity(tz1, tz2)[0][0]

        os.remove(root + "faceapi/faceCompared/upload/" + str(name1))
        os.remove(root + "faceapi/faceCompared/upload/" + str(name2))

        return HttpResponse('{"status":true,"data":"' + str(comparedValue) + '","msg":"成功"}')
    else:
        return HttpResponse('{"status":false,"data":"","msg":"请求不合法"}')
    return HttpResponse('{"status":false,"data":"","msg":"未知错误"}')


# 保存上传文件
def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
