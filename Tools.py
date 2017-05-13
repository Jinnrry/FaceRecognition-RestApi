# -*- coding: utf-8 -*-
import numpy as np
import pickle
import skimage
import redis
caffe_root = '/home/jiangwei/bin/caffe-master/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import sklearn.metrics.pairwise as pw

#我把GPU加速注释掉了,所以没有GPU加速,速度有点慢
#caffe.set_mode_gpu()


#加载caffe模型
global net
net=caffe.Classifier('vgg/deploy.prototxt','vgg/vgg_face.caffemodel',caffe.TEST)


#提取特征数组
def get_feature(path1):
    global net
    #加载图片
    X=read_image(path1)
    test_num=np.shape(X)[0]
    #X  作为 模型的输入
    out = net.forward_all(blobs=['fc7'],data = X)
    # print out.keys()

    #fc7是模型的输出,也就是特征值
    feature1 = np.float64(out["fc7"])

    feature1=np.reshape(feature1,(test_num,4096))
    #加载注册图片
    return feature1



def read_image(im1):

    averageImg = [129.1863,104.7624,93.5940]
    X=np.empty((1,3,224,224))
    # word=filelist.split('\n')
    # filename=word[0]
    # im1=skimage.io.imread(filename,as_grey=False)
    #归一化
    image =skimage.transform.resize(im1,(224, 224))*255
    X[0,0,:,:]=image[:,:,0]-averageImg[0]
    X[0,1,:,:]=image[:,:,1]-averageImg[1]
    X[0,2,:,:]=image[:,:,2]-averageImg[2]
    return X


#将数据存入redis数据库
def saveData(name,img):
    info = get_feature(img)
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.lpush(name,pickle.dumps(info))