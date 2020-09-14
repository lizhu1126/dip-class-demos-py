import cv2 as cv
import function

t1 = cv.getTickCount()
n = 10000
ifprint = True
function.pickprime(n, ifprint)
t2 = cv.getTickCount()
time_pickprime = (t2 - t1) / cv.getTickFrequency()
print("time:%s ms" % (time_pickprime*1000))
t3 = cv.getTickCount()
function.eratossieve(n, ifprint)
t4 = cv.getTickCount()
time_eratossieve = (t4 - t3) / cv.getTickFrequency()
print("time:%s ms" % (time_eratossieve*1000))
