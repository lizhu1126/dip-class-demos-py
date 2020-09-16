import cv2 as cv
import numpy as np
import math


# 第十二周练习1：实现背景差分
def bgsub_demo():
    capture = cv.VideoCapture(0)
    if capture.isOpened() is None:
        print("fail to open")
        return -1
    cnt = 0
    while True:
        ret, frame = capture.read()
        grymat = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        if cnt == 0:
            # 获取背景图像
            bgmat = grymat.copy()
        else:
            submat = cv.absdiff(grymat, bgmat)
            
            # 差分结果二值化
            ret, bny_submat = cv.threshold(submat, 100, 255, cv.THRESH_BINARY)
            cv.imshow("b_submat", bny_submat)
            cv.imshow("submat", submat)
            cv.waitKey(30)
        cnt = cnt + 1
    return 0


# 第十二周练习2：实现高斯建模及背景差分
num_photo = 50


# 定义计算方差及均值的函数
def calgussianbackground(srcmats, meanmat, varmat):
    # 遍历一个像素点在每张图片上的大小
    height = srcmats[0].shape[0]
    width = srcmats[0].shape[1]
    for i in range(height):
        for j in range(width):
            num_sum = 0
            var = 0
            # 求均值
            for k in range(num_photo):
                num_sum = num_sum + srcmats[k][i, j]
            meanmat[i, j] = int(num_sum / num_photo)
            # 求方差
            for m in range(num_photo):
                var = var + float(math.pow(abs(srcmats[m][i, j] - meanmat[i, j]), 2))
            varmat[i, j] = var / num_photo


# 二值化
def gaussianthreshold(srcmat, meanmat, varmat, weight, dstmat):
    height = srcmat.shape[0]
    width = srcmat.shape[1]
    # 遍历像素
    for i in range(height):
        for j in range(width):
            dif = abs(srcmat[i, j] - meanmat[i, j])
            th = int(weight * varmat[i, j])
            if dif > th:
                dstmat[i, j] = 255
            else:
                dstmat[i, j] = 0


# 高斯分布背景差分
def bgsubgaussian_demo():
    # 读取摄像头
    capture = cv.VideoCapture(0)
    if capture.isOpened() is None:
        print("打开失败")
        return
    cnt = 0
    # 建立存图像数组
    ret, frame = capture.read()
    gry_mat = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    srcmats = [gry_mat] * num_photo
    calmodel = True
    while True:
        # 开始存图
        ret, frame = capture.read()
        gry_mat = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        if cnt < num_photo:
            srcmats[cnt] = gry_mat
            if cnt == 0:
                print("----reading frame----")
            else:
                print("-", end = "")
        else:
            if calmodel:
                print("calculating background models")
                # 计算均值方差
                meanmat = gry_mat.copy()
                varmat = np.ones([gry_mat.shape[0], gry_mat.shape[1]], np.float32)
                calgussianbackground(srcmats, meanmat, varmat)
            calmodel = False
            dstmat = np.zeros([gry_mat.shape[0], gry_mat.shape[1]], np.uint8)
            # 筛选结果
            gaussianthreshold(gry_mat, meanmat, varmat, 2, dstmat)
            cv.imshow("result", dstmat)
            cv.imshow("frame", gry_mat)
            cv.waitKey(30)
        cnt = cnt + 1
