import cv2 as cv


# 第五周练习1-3
def filtermat():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("无法读取视频")
        return
    ret, frame = cap.read()
    if ret:
        # 中值滤波
        median_mat = cv.medianBlur(frame, 3)
        # 均值滤波
        blur_mat = cv.blur(frame, (3, 3))
        # 高斯滤波
        guass_mat = cv.GaussianBlur(frame, (3, 3), 1, 0)
        
        # 显示图片
        cv.imshow("median", median_mat)
        cv.imshow("blur", blur_mat)
        cv.imshow("guass", guass_mat)
        cv.waitKey(0)


# 第五周；练习4边缘提取
def sobel_extraction():
    
    # 读取摄像头
    capture=cv.VideoCapture(0)
    if not capture.isOpened():
        print("打开摄像头失败")
        return
    
    # 读取当前帧照片
    ret, frame = capture.read()
    
    # 利用sobel算子进行边缘提取
    sobel_mat = cv.Sobel(frame, -1, 1, 0, 5)
    cv.imshow("sobel", sobel_mat)
    
    
# 第五周练习5 磨皮程序
def convolution_app():
    cap = cv.VideoCapture(0)
    
    # 肤色h
    i_minh = 0
    i_maxh = 20
    
    # 颜色饱和度s
    i_mins = 43
    i_maxs = 255
    
    # 颜色亮度v
    i_minv = 55
    i_maxv = 255
    
    # 读取当前帧图片
    ret, frame = cap.read()
    
    # 转化为HSV图片
    hsvmat = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # 筛选目标区域
    mask_mat = cv.inRange(hsvmat, (i_minh, i_mins, i_minv), (i_maxh, i_maxs, i_maxv))
    
    # 对原图进行高斯滤波
    guass_mat = cv.GaussianBlur(frame, (5, 5), 3, 0)
    
    # 滤波后图像与目标区域进行与操作，筛选出磨皮后的人脸
    img1_mat = cv.bitwise_and(guass_mat, guass_mat, mask = mask_mat)
    
    # 对目标区域进行反色
    mask_mat = 255 - mask_mat
    
    # 在原图上留出目标区域地方（为磨皮后的人脸腾地方）
    img2_mat = cv.bitwise_and(frame, frame, mask = mask_mat)
    
    # 将磨皮后的人脸放到原人像上
    object_mat = cv.add(img1_mat, img2_mat)
    
    # 显示图片
    cv.imshow("frame", frame)
    cv.imshow("img1_mat", img1_mat)
    cv.imshow("img2_mat", img2_mat)
    cv.imshow("mask", mask_mat)
    cv.imshow("ob", object_mat)
