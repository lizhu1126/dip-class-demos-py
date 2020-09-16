import cv2 as cv
import math


# 防止像素越界
def saturate(n):
    if n > 255:
        return 255
    else:
        return n


def gamma(grymat):
    # 建立查询表
    lut = [0.0] * 256
    y = 0.45
    for i in range(256):
        lut[i] = saturate(math.pow(float(i) / 255, y) * 255)
    height = grymat.shape[0]
    width = grymat.shape[1]
    for i in range(height):
        for j in range(width):
            grymat[i, j] = lut[grymat[i, j]]


# 十一周练习1
def gamma_face():
    # 读取图片
    srcmat = cv.imread("d:/face.jpg")
    # 转化为灰度图
    grymat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    gamma(grymat)
    cv.imshow("grymat", grymat)
    cv.imshow("srcmat", srcmat)
    cv.waitKey(0)


# 第十一周练习2 直方图均衡函数
def equalize():
    # 读取图片
    srcmat = cv.imread("d:/face.jpg")
    # 通道分离
    b_image, g_image, r_image = cv.split(srcmat)
    # 分别对每个分离后的通道进行均衡化
    b_equa = cv.equalizeHist(b_image)
    g_equa = cv.equalizeHist(g_image)
    r_equa = cv.equalizeHist(r_image)
    # 合并图像
    equamat = cv.merge([b_equa, g_equa, r_equa])
    # 显示图像
    cv.imshow("result", equamat)
    cv.waitKey(0)


# 第十一周练习3
def gammacorrection():
    # 读取图片
    srcmat = cv.imread("d:/gtest.jpg")
    # 通道分离
    b_gamma, g_gamma, r_gamma = cv.split(srcmat)
    # 分别对每个分离后的通道进行均衡化
    gamma(b_gamma)
    gamma(g_gamma)
    gamma(r_gamma)
    # 合并图像
    gammamat = cv.merge([b_gamma, g_gamma, r_gamma])
    # 显示图像
    cv.imshow("result", gammamat)
    cv.waitKey(0)
