# -*- coding: utf-8 -*-
import cv2
import Signup
import Read
print "1.使用视频注册"
print "2.视频识别"
print "3.使用图片注册"
print "4.识别图片中的人脸"
pick=input("请选择操作:")

if(pick == 1):
    Signup.start()

if pick ==2 :
    Read.start()

if pick==3 :
    Signup.photoSignup("2017-05-13-175444.jpg")

if pick==4 :
    Read.photoRead("2017-05-13-210502.jpg")