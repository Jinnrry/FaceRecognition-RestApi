# -*- coding: utf-8 -*-
import random
import sys

import os
from config import config
root=config.Config.root
caffe_root=config.Config.caffe_root
sys.path.insert(0, caffe_root + 'python')
import time
from django.http import HttpResponse
import caffe
import matplotlib.pyplot as plt
# GPU加速
caffe.set_device(0)
caffe.set_mode_gpu()

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


#加载均值文件
mean_filename=root+'model/mean.binaryproto'
proto_data = open(mean_filename, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean  = caffe.io.blobproto_to_array(a)[0]


#加载性别检测神经网络
gender_net_pretrained=root+'model/gender_net.caffemodel'
gender_net_model_file=root+'model/deploy_gender.prototxt'
gender_net = caffe.Classifier(gender_net_model_file, gender_net_pretrained,
                       mean=mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

gender_list=['Male','Female']

def getGender(img):
    input_image = caffe.io.load_image(img)
    print (input_image)
    prediction = gender_net.predict([input_image])
    return gender_list[prediction[0].argmax()]


# 保存上传文件
def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


# api返回函数
def gender(request):
    if request.method == 'POST':
        if len(request.FILES) != 1:
            return HttpResponse('{"status":false,"data":"","msg":"图片参数错误！"}')
        starttime = time.time()
        name1 = str(random.randint(10000, 99999)) + str(time.time())  # 随机名字
        handle_uploaded_file(request.FILES['pic'], str(name1))

        gender= getGender(root + "RestServer/upload/" + str(name1))

        os.remove(root + "RestServer/upload/" + str(name1))
        endtime = time.time()
        Runtime = endtime - starttime
        return HttpResponse('{"status":true,"data":"' + gender + '","msg":"成功","runtime": ' + str(Runtime) + '"  }')
    else:
        return HttpResponse('{"status":false,"data":"","msg":"请求不合法"}')
    return HttpResponse('{"status":false,"data":"","msg":"未知错误"}')