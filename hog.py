import cv2 as cv
import math
import numpy as np


# 手动实现HOG
def calhog(src, hist, nangle, cellsize):
    # 判断读取的尺寸是否正确
    if cellsize > src.shape[0] or cellsize > src.shape[1]:
        return -1
    # 参数设置
    nx = int(src.shape[1] / cellsize)
    ny = int(src.shape[0] / cellsize)
    binangle = 360 / nangle
    
    # 计算梯度及角度
    gx = cv.Sobel(src, cv.CV_32F, 1, 0)
    gy = cv.Sobel(src, cv.CV_32F, 0, 1)
    mag, angle = cv.cartToPolar(gx, gy)
    # 提取一个cell的梯度及长度
    for i in range(nx):
        for j in range(ny):
            roimag = mag[i * cellsize:(i + 1) * cellsize, j * cellsize:(j + 1) * cellsize]
            roiang = angle[i * cellsize:(i + 1) * cellsize, j * cellsize:(j + 1) * cellsize]
            h_head = (i * nx + j) * nangle
            for m in range(roimag.shape[0]):
                for n in range(roimag.shape[1]):
                    pos = int(roiang[m, n] / binangle)
                    hist[h_head + pos] = roimag[m, n] + hist[h_head + pos]
    return 0


# 计算直方图距离
def norml2(hist1, hist2, size):
    d_sum = 0
    for i in range(size):
        d_sum = d_sum + (hist1[i] - hist2[i]) * (hist1[i] - hist2[i])
    d_sum = math.sqrt(d_sum)
    return d_sum


# 比较三张图片
def compareimage(src1,src2):
    # 转化为灰度图
    ref_gry = cv.cvtColor(src1, cv.COLOR_BGR2GRAY)
    pl_gry = cv.cvtColor(src2, cv.COLOR_BGR2GRAY)
    
    # 参数设置
    nangle = 8
    blocksize = 16
    nx = int(ref_gry.shape[1] / blocksize)
    ny = int(ref_gry.shape[0] / blocksize)
    bins = nx * ny * nangle
    
    # 新建数组
    ref_hist = [0] * bins
    pl_hist = [0] * bins
    
    recode = calhog(ref_gry, ref_hist, nangle, blocksize)
    recode = calhog(pl_gry, pl_hist, nangle, blocksize)
    
    # 计算直方图距离
    dis1 = norml2(ref_hist, pl_hist, bins)
   
    
   # print(f"distance between reference and img1:{dis1}")
    return dis1
    
