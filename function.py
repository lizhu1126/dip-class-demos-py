import cv2 as cv
import numpy as np


# 第6周练习1 canny算子
def canny_extraction():
    
    # 打开摄像头
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("打开摄像头失败")
        return
    # 读取当前帧图片
    ret, frame = cap.read()
    
    # 由sobel算子得到x,y方向上的梯度
    dx = cv.Sobel(frame, cv.CV_16S, 1, 0)
    dy = cv.Sobel(frame, cv.CV_16S, 0, 1)
    # 边缘提取
    canny1_mat = cv.Canny(dx, dy, 20, 60)
    
    # 转化为灰度图并进行边缘提取
    gry_mat = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    canny2_mat = cv.Canny(gry_mat, 20, 60)
    
    # 显示效果图
    cv.imshow("canny1", canny1_mat)
    cv.imshow("canny2", canny2_mat)
    cv.waitKey(30)
    
    
# 第6周练习2、3、4 旋转、缩放以及仿射变换 投影变换
def warpaffine():
    # 读取照片
    srcmat = cv.imread("d:/lena.jpg")
    if srcmat is None:
        print("读取照片失败")
    
    # 旋转以及缩放
    
    # 初始化旋转角度以及缩放尺度
    angle = -10.0
    scale = 1
    center = (srcmat.shape[1] * 0.5, srcmat.shape[0] * 0.5)
    
    # 获得变换矩阵
    affine_matrix_zoom = cv.getRotationMatrix2D(center, angle, scale)
    # 利用仿射变换函数
    dstmat = cv.warpAffine(srcmat, affine_matrix_zoom, (srcmat.shape[0], srcmat.shape[1]))

    # 仿射变换
    # 变换前后分别对应的3个坐标
    src_pt = np.float32([[200, 200], [250, 200], [200, 100]])
    warp_pt = np.float32([[300, 100], [300, 50], [200, 100]])
    # 获得变换矩阵
    affine_matrix = cv.getAffineTransform(src_pt, warp_pt)
    # 仿射变换
    affine_mat = cv.warpAffine(srcmat, affine_matrix, (srcmat.shape[0], srcmat.shape[1]))

    # 投影变换

    # 变换前后4点坐标
    pst1 = np.float32([[150, 150], [150, 300], [350, 300], [350, 150]])
    pst2 = np.float32([[200, 150], [200, 300], [340, 270], [340, 180]])
    # 生成投影变换矩阵
    perspective_matrix = cv.getPerspectiveTransform(pst1, pst2)
    # 投影变换
    perspective_mat = cv.warpPerspective(srcmat, perspective_matrix, (srcmat.shape[0], srcmat.shape[1]))

    cv.imshow("srcmat", srcmat)
    cv.imshow("dstmat", dstmat)
    cv.imshow("affine_mat", affine_mat)
    cv.imshow("perspective_Mat", perspective_mat)


# 第6周练习5 图像矫正
def img_correct():
    # 读取图片
    srcmat = cv.imread("d:/lena_rot.jpg")
    
    # 将图片转化为灰度图
    gry_mat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    
    # 读取图片的长和宽
    height = srcmat.shape[0]
    width = srcmat.shape[1]
    
    # 找原图的四个顶点
    for j in range(width):
        if gry_mat[0, j] < 250:
            pt_0 = [j, 0]
            j = width
    
    for j in range(width - 1, -1, -1):
        if gry_mat[height - 1, j] < 250:
            pt_3 = [j, height - 1]
            j = -1
    
    for i in range(height - 1, -1, -1):
        if gry_mat[i, 0] < 250:
            pt_2 = [0, i]
            i = -1
    
    for i in range(0, height):
        if gry_mat[i, width - 1] < 250:
            pt_1 = [width-1, i]
            i = height
    pst1 = np.float32([pt_0, pt_1, pt_2, pt_3])
    
    # 矫正后图的四个顶点
    pst2 = np.float32([[0, 0], [width - 1, 0], [0, height - 1], [width - 1, height - 1]])
    # 获得变换矩阵
    matrix = cv.getPerspectiveTransform(pst1, pst2)
    # 进行投影变换
    correct_mat = cv.warpPerspective(srcmat, matrix, (srcmat.shape[0], srcmat.shape[1]))
    
    # 显示图片
    cv.imshow("srcmat", srcmat)
    cv.imshow("correct", correct_mat)
