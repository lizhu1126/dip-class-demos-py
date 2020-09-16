import cv2 as cv
import hog
import numpy as np


# 第十三周练习一，利用HOG图片相似度函数完成物体追踪
def hog_template():
    # 读取模板以及待匹配图片
    template = cv.imread("d:/template.png")
    srcmat = cv.imread("d:/img.png")
    # 获取模板以及待匹配图片宽高
    height = srcmat.shape[0]
    width = srcmat.shape[1]
    h = template.shape[0]
    w = template.shape[1]
    dis = [0] * ((height - h) * (width - w))
    min_dis = 1000000
    a = (0, 0)
    # 分别以每个像素点为为初始点，比较两个区域相似度
    for i in range(height - h + 1):
        for j in range(width - w + 1):
            testmat = srcmat[i:h + i, j:w + j]
            dis = hog.compareimage(testmat, template)
            if min_dis > dis:
                a = (j, i)
                min_dis = dis
    # 圈出相似度最高的区域
    cv.rectangle(srcmat, a, (a[0] + w, a[1] + h), (255, 0, 0))
    cv.imshow("rec", srcmat)
    cv.waitKey(0)


# 第十三周练习二  模板匹配调用
def templatematching_demo():
    # 选择方法
    matchmethod = 0
    # 打开摄像头
    capture = cv.VideoCapture(0)
    # 判断摄像头是否打开
    if capture.isOpened() is None:
        print("faile to open")
    cnt = 0
    while True:
        ret, frame = capture.read()
        cv.imshow("frame", frame)
        if cnt == 0:
            # 选择感兴趣区域
            r = cv.selectROI("frame", frame)
            x, y, width, height = r
            # 确定模板图片
            tempmat = frame[y:y + height, x:x + width]
            refmat = tempmat.copy()
        # 进行模板匹配得到存储结果的矩阵
        resultmat = cv.matchTemplate(frame, refmat, matchmethod)
        # 进行归一化
        resultmat = cv.normalize(resultmat, resultmat)
        # 取出模板匹配的结果
        minval, maxval, minloc, maxloc = cv.minMaxLoc(resultmat)
        
        # 根据模板匹配方法的不同选择最佳结果
        if matchmethod == cv.TM_SQDIFF or matchmethod == cv.TM_SQDIFF_NORMED:
            matchloc = minloc
        
        else:
            matchloc = maxloc
        dismat = frame.copy()
        # 根据匹配到的结果，用矩形画出区域
        cv.rectangle(dismat, matchloc, (matchloc[0] + refmat.shape[1], matchloc[1] + refmat.shape[0]), (0, 0, 0), 2, 8,
                     0)
        cnt = cnt + 1
        # 显示结果
        cv.imshow("template", refmat)
        cv.imshow("dispMat", dismat)
        cv.waitKey(30)
