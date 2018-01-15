基于Vgg神经网络的人脸识别系统

需要环境：
opencv
caffe
redis

test_main.py文件是用来测试识别率的，我测试结果是接近95%的识别率，不过只有2个人的数据对比

识别结果：
<img src="result/r1.png"> <br>
<img src="result/r2.png"> <br>
<img src="result/r3.png"> <br>


文件说明：
test.py是用来测试神经网络是否能正常运行的，也是程序的核心功能测试（人脸相识度对比）
test_main.py是用来测试网络识别率的
main.py写了一个人脸识别的命令台程序


项目数据储存方面设计有点问题,是将注册后的人脸模型存在redis数据库中的,识别的时候需要遍历数据库所有数据去检测人脸属于谁,
如果样本过大的话系统运行速度肯定很慢。如果你看到这里有什么好的算法或者建议特别希望能留言。非常感谢



### 2018年1月15日更新：

将核心功能（人脸相似度对比）封装成了一个REST API，这部分功能在faceCompared目录中。

另外，经过测试，在进行人脸相识度对比的时候，使用FC7层的数据进行对比，精确度会更高，在REST API项目中已经修改，测试项目中就懒得修改了



 本文中介绍的人脸识别系统是基于这两篇论文：

[《Very deep convolutional networks for large-scale image recognition》](http://xueshu.baidu.com/s?wd=paperuri%3A%282801f41808e377a1897a3887b6758c59%29&filter=sc_long_sign&tn=SE_xueshusource_2kduw22v&sc_vurl=http%3A%2F%2Farxiv.org%2Fabs%2F1409.1556&ie=utf-8)

[《Deep Face Recognition》](http://www.robots.ox.ac.uk/~vedaldi/assets/pubs/parkhi15deep.pdf)
