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
# GPU加速
caffe.set_device(0)
caffe.set_mode_gpu()


#加载均值文件
mean_filename=root+'model/mean.binaryproto'
proto_data = open(mean_filename, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean  = caffe.io.blobproto_to_array(a)[0]

#年龄检测神经网络
age_net_model_file=root+'model/age_net.caffemodel'
age_net_pretrained=root+'model/deploy_age.prototxt'
net = caffe.Net(age_net_pretrained,age_net_model_file,caffe.TEST)

# 图像预处理
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', mean)
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2,1,0))

age_list=['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']

def getAge(img):
    input_image = caffe.io.load_image(img)
    net.blobs['data'].data[...] = transformer.preprocess('data', input_image)
    out = net.forward()
    out_prob = out['prob'][0]
    index = out_prob.argmax()
    return age_list[index]


# 保存上传文件
def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


# api返回函数
def age(request):
    if request.method == 'POST':
        if len(request.FILES) != 1:
            return HttpResponse('{"status":false,"data":"","msg":"图片参数错误！"}')
        starttime = time.time()
        name1 = str(random.randint(10000, 99999)) + str(time.time())  # 随机名字
        handle_uploaded_file(request.FILES['pic'], str(name1))

        age= getAge(root + "RestServer/upload/" + str(name1))

        os.remove(root + "RestServer/upload/" + str(name1))
        endtime = time.time()
        Runtime = endtime - starttime
        return HttpResponse('{"status":true,"data":"' + age + '","msg":"成功","runtime": ' + str(Runtime) + '"  }')
    else:
        return HttpResponse('{"status":false,"data":"","msg":"请求不合法"}')
    return HttpResponse('{"status":false,"data":"","msg":"未知错误"}')