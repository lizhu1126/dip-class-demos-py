import cv2 as cv
import numpy as np


# 制作mask函数
def creatmaskbykmeans(src, mask):
    # 读取图片大小
    width = src.shape[1]
    height = src.shape[0]
    pixnum = width * height
    # 设置参数
    clustercount = 2
    # 准备图片
    sampdata = src.reshape((pixnum, 3))
    km_data = sampdata.astype(np.float32)
    criteria = (cv.TermCriteria_EPS + cv.TermCriteria_COUNT, 10, 0.1)
    ompactness, labels, centers = cv.kmeans(km_data, clustercount, None, criteria, clustercount,
                                            flags = cv.KMEANS_PP_CENTERS)
    print(labels)
    print(centers)
    # 制作mask
    fg = [0, 255]
    for row in range(height):
        for col in range(width):
            mask[row, col] = fg[labels[row * width + col][0]]


def segcolor():
    # 读取视频
    src = cv.imread("d:/movie.png")
    # 初始化
    mask = np.ones([src.shape[0], src.shape[1]], np.uint8)
    # 调用函数
    creatmaskbykmeans(src, mask)
    cv.imshow("src", src)
    cv.imshow("mask", mask)
    cv.waitKey(0)
