基于神经网络的人脸识别Rest API

需要环境：
opencv
caffe
django
.....

识别结果：
<img src="result/r1.png"> <br>
<img src="result/r2.png"> <br>
<img src="result/r3.png"> <br>


文件说明：
model 文件夹存放的是一些模型文件
RestServer是核心代码

项目将人脸识别与人脸定位的功能封装成了REST API，将RestServer运行起来以后就可以通过REST API的方式访问调用

运行方法：进入RestServer文件夹，打开main.py文件，修改成你本机的路径，然后在RestServer目录下运行python manage.py runserver 没有报错即可

API调用方法：

http://你的ip/compared  调用方法：post   这是人脸对比接口地址，需要2个post参数：face1 和 face2 数据为你的两张人脸图片

成功返回类似：{"status":true,"data":"0.950035393407","msg":"成功","runtime": 1.6822376251220703"  }   status调用是否成功，data为两张人脸的相似度（大约78%可判断为同一个人），msg为说明，runtime为识别执行时间

http://你的ip/locate    调用方法：post   这是人脸定位接口地址，需要一个post参数：pic 数据为你需要定位人脸的图片

成功返回类似：[{ "x":277 ,"y":276 ,"height":301,"width":301 } ,{ "x":862 ,"y":329 ,"height":220,"width":220 } ,{ "x":1099 ,"y":609 ,"height":50,"width":50 } ]

返回中每有一个数组就表示检测到一张人脸 X，Y表示人脸左上角坐标，height width表示高度和宽度

部署说明：

如果你需要用于生产项目使用，该项目一定要用apache2或者ngnix发布，上面提供的运行方法仅供测试使用。具体部署访问请参考django项目部署


最后！！

欢迎提出意见，如果改进优化了这个项目请也提交我一份代码，邮箱地址 ok@xjiangwei.cn