# -*- coding: utf-8 -*-
import pickle
import skimage
import cv2
import redis
import sklearn.metrics.pairwise as pw
import Tools

def getFaceImg(img):
    face_cascade=cv2.CascadeClassifier("/home/jiangwei/下载/faceRead/haarcascade_frontalface_default.xml")
    if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
            gray = img  #if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)#1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
    result = []
    for (x,y,width,height) in faces:
            result.append((x,y,x+width,y+height))

    print result
    if(len(result)>0):
        for r in result:
            img2=cv2.rectangle(img, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 3)
            img3=img[r[1]:r[3], r[0]:r[2]]  # 得到视频中的人脸，使用识别


        return [img3,img2]

    return []

#使用图片注册
def photoSignup(filename):
    nameid = raw_input("请输入用户名：\n")
    r = redis.Redis(host='localhost', port=6379, db=0)
    frame = skimage.io.imread(filename,as_grey=False)
    # show a frame
    face = getFaceImg(frame)
    if len(face) > 0:
        faceshow = face[1]
        # cv2.imshow("show",faceshow)    #这里设置是否显示图像情况
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        face = face[0]
    if len(face) > 1:  # 图像中存在人脸
        userdatalen = r.llen(nameid)
        if userdatalen >= 1000:  # 设置录入样本数
            return 0 # 数据录入结束
        if userdatalen > 0:  # 数据库中存在该用户id的人脸数据
            flag = True
            print userdatalen
            for i in xrange(userdatalen):  # 便利数据库每个模型
                model = pickle.loads(r.lindex(nameid, i))  # 数据库数据反序列化
                feature = Tools.get_feature(face)  # 获取脸型特征
                if pw.cosine_similarity(model, feature) > 0.9:  # 与数据库人脸匹配是同一人
                    flag = False  # 标记是否不添加进数据库
            if (flag):
                r.lpush(nameid, pickle.dumps(feature))  # 新数据入库
                print "录入模型成功"
        else:  # 数据库不存在该用户数据
            feature = Tools.get_feature(face)  # 获取脸型特征
            r.lpush(nameid, pickle.dumps(feature))  # 新数据入库
            print "录入模型成功"



def start():
    nameid=raw_input("请输入用户名：\n")
    r = redis.Redis(host='localhost', port=6379, db=0)

    cap = cv2.VideoCapture(0)

    while(1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        face=getFaceImg(frame)
        if len(face)>0:
            faceshow=face[1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(faceshow, "Move head", (100,100), font, 1, (255, 255, 255), 2)
            cv2.imshow("show",faceshow)    #这里设置是否显示图像情况
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            face=face[0]
        if len(face)>1 :  #图像中存在人脸
            userdatalen=r.llen(nameid)
            if userdatalen >=2:   #设置录入样本数
                break   # 数据录入结束
            if userdatalen >0 :   #数据库中存在该用户id的人脸数据
                flag=True
                print userdatalen
                for i in xrange(userdatalen):   #便利数据库每个模型
                    model=pickle.loads( r.lindex(nameid,i) )   #数据库数据反序列化
                    feature=Tools.get_feature(face)    #获取脸型特征
                    if pw.cosine_similarity(model,feature)>0.9 : #与数据库人脸匹配是同一人
                            flag=False   #标记是否不添加进数据库
                if  (flag) :
                    r.lpush(nameid,pickle.dumps(feature))  #新数据入库
            else: #数据库不存在该用户数据
                feature = Tools.get_feature(face)  # 获取脸型特征
                r.lpush(nameid, pickle.dumps(feature))  # 新数据入库

