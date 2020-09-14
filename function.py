import cv2 as cv
import numpy as np
import math


def spin_correct():
    srcmat = cv.imread("d:/lena.jpg")
    if srcmat is None:
        print("fail to read")
        return
    angle = -10.0
    scale = 1
    
    center = (int(srcmat.shape[1] *0.5), int(srcmat.shape[0] *0.5))
    rot = cv.getRotationMatrix2D(center, angle, scale)
    cos = np.abs(rot[0, 0])
    sin = np.abs(rot[0, 1])
    width = int((srcmat.shape[0] * sin) + (srcmat.shape[1] * cos))
    height = int((srcmat.shape[0] * cos) + (srcmat.shape[1] * sin))
    rot[0, 2] += (width / 2) - (srcmat.shape[1]//2)
    rot[1, 2] += (height / 2) - (srcmat.shape[0]//2)
    warpmat = cv.warpAffine(srcmat, rot, (width, height))
    cv.imshow("warpmat", warpmat)
    cv.waitKey(0)


def saturate(data):
    if data < 0:
        data = 0
    elif data > 255:
        data = 255
    else:
        data = data
    
    return data


def houghdemo():
    srcmat = cv.imread("d:/img.png")
    if srcmat is None:
        print("failed to read image")
        return
    
    dx = cv.Sobel(srcmat, cv.CV_16S, 1, 0)
    dy = cv.Sobel(srcmat, cv.CV_16S, 0, 2)
    # 边缘提取
    canny_mat = cv.Canny(dx, dy, 60, 180)
    cv.imshow("canny_mat", canny_mat)
    lines = cv.HoughLines(canny_mat, 1, np.pi / 180, 55)
    
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))
        cv.line(srcmat, pt1, pt2, (255, 0, 0),1)
    cv.imshow("srcmat",srcmat)
    cv.waitKey(0)
    
    
def houghsp_demo():
    srcmat=cv.imread("d:/img.png")
    if srcmat is None:
        print(" failed to read ")
        return

    # 转化为灰度图
    grymat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    # 边缘检测
    canny_mat = cv.Canny(grymat, 30, 200)
    # canny_mat=cv.Sobel(grymat, cv.CV_8UC1, 0, 1)
    # dx = cv.Sobel(srcmat, cv.CV_16S, 2, 0)
    # dy = cv.Sobel(srcmat, cv.CV_16S, 0, 1)
    # # 边缘提取
    # canny_mat = cv.Canny(dx, dy, 60, 120)
    lines = cv.HoughLinesP(canny_mat,1, np.pi / 180, 18, 10, 10)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(srcmat, (x1, y1), (x2, y2), (255, 0, 255),2,8,0)
    cv.imshow("src", srcmat)
    cv.imshow("canny_mat", canny_mat)
    cv.waitKey(0)
    
    
