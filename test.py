# -*- coding: utf-8 -*-
#想要加中文注释就必须将字符编码格式设置为utf8
#作者:郭开
#运行之前请把python和caffe 的环境配置好
import numpy as np
import os
import os.path
import skimage

caffe_root = '/home/jiangwei/bin/caffe-master/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
import sklearn.metrics.pairwise as pw


#我把GPU加速注释掉了,所以没有GPU加速,速度有点慢,你要在学校有条件找个有GeForce显卡的电脑
#caffe.set_mode_gpu()


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

    #fc7是模型的输出,也就是特征值
    feature1 = np.float64(out["pool5"])

    feature1=np.reshape(feature1,(test_num,25088))
    #加载注册图片
    X=read_image(path2)
    #X  作为 模型的输入
    out = net.forward_all(blobs=['pool5'],data=X)
    #fc7是模型的输出,也就是特征值
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
    thershold=0.47
    # 加载注册图片与验证图片
    # 注意:人脸图像必须是N*N的!!!如果图片的高和宽不一样,进行归一化的时候会对图片进行拉伸,影响识别效果
    reg_path="faces/jw1.jpeg"
    rec_path="faces/jw9.jpeg"

    #计算注册图片与验证图片的相似度
    result=compar_pic(reg_path,rec_path)
    print "%s和%s两张图片的相似度是:%f\n\n"%(reg_path,rec_path,result)
    if result>=thershold:
        print '是同一个人!!!!\n\n'
    else:
        print '不是同一个人!!!!\n\n'