# -*- coding: utf-8 -*-

import numpy as np
import os
import os.path
import skimage

caffe_root = '/home/jiangwei/bin/caffe-master/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import sklearn.metrics.pairwise as pw


#GPU加速
caffe.set_mode_gpu()


#加载caffe模型
global net
net=caffe.Classifier('vgg/deploy.prototxt','vgg/vgg_face.caffemodel',caffe.TEST)

def compar_pic(path1,path2):
    global net
    #加载验证图片
    X=read_image(path1)
    test_num=np.shape(X)[0]
    #X  作为 模型的输入
    out = net.forward_all(blobs=['pool5'],data = X)
    # print out.keys()

    feature1 = np.float64(out["pool5"])

    feature1=np.reshape(feature1,(test_num,25088))
    #加载注册图片
    X=read_image(path2)
    #X  作为 模型的输入
    out = net.forward_all(blobs=['pool5'],data=X)
    feature2 = np.float64(out['pool5'])
    feature2=np.reshape(feature2,(test_num,25088))
    #求两个特征向量的cos值,并作为是否相似的依据
    predicts=pw.cosine_similarity(feature1, feature2)
    return  predicts



def read_image(filelist):

    averageImg = [129.1863,104.7624,93.5940]
    X=np.empty((1,3,224,224))
    word=filelist.split('\n')
    filename=word[0]
    im1=skimage.io.imread(filename,as_grey=False)
    #归一化
    image =skimage.transform.resize(im1,(224, 224))*255
    X[0,0,:,:]=image[:,:,0]-averageImg[0]
    X[0,1,:,:]=image[:,:,1]-averageImg[1]
    X[0,2,:,:]=image[:,:,2]-averageImg[2]
    return X


if __name__ == '__main__':

    #设置阈值,大于阈值是同一个人,反之
    #阈值取0.47的情况下识别率是0.864366449
    #阈值取0.48的情况下识别率是0.860797144557
    #阈值取0.46的时候识别率   0.860797144557
    thershold=0.46
    flag=0
    all=0
    error=[]
    B=0
    S=0
    for parent, dirnames, filenames in os.walk("faces"):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:
            im1="faces/"+filename
            im1type= im1[6]
            for parent2, dirnames2, filenames2 in os.walk("faces"):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
                for filename2 in filenames2:
                    im2="faces/"+filename2
                    im2type=im2[6]
                    all+=1
                    co=compar_pic(im1, im2)
                    if co>=thershold and im1type==im2type :  #识别正确
                        flag+=1
                    elif co<thershold and im2type!=im1type :  #识别正确
                        flag+=1
                    elif co<thershold and im1type == im2type : #阈值大了
                        S+=1
                    elif co>=thershold and im1type != im2type : #阈值小了
                        B+=1
                    print im1
                    print im2
                    print "flag:"+str(flag)
                    print "all:"+str(all)
                    print float(flag)/float(all)
                    print "B:"+str(B)    #因阈值偏小导致识别错误的次数,此值偏大说明阈值应到调大
                    print "S:"+str(S)    #因阈值偏大导致识别错误的次数,此值偏大说明阈值应当调小
                    print "--------------"

    print error



