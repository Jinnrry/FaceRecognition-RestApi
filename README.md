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


 本文中介绍的人脸识别系统是基于这两篇论文：

《Very deep convolutional networks for large-scale image recognition》(http://xueshu.baidu.com/s?wd=paperuri%3A%282801f41808e377a1897a3887b6758c59%29&filter=sc_long_sign&tn=SE_xueshusource_2kduw22v&sc_vurl=http%3A%2F%2Farxiv.org%2Fabs%2F1409.1556&ie=utf-8)

《Deep Face Recognition》(http://www.robots.ox.ac.uk/~vedaldi/assets/pubs/parkhi15deep.pdf)
