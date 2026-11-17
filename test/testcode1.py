import cv2
cap = cv2.VideoCapture(0)  # /dev/video0
cap.set(3,640)
cap.set(4,480)
cap.set(cv2.CAP_PROP_FPS,10)
#cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter.fourcc('Y','U','Y','V')) # 下面不行可以尝试这个
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter.fourcc('M','J','P','G'))
while(True):
    ret, frame = cap.read()
    if not ret:
        print("Failed to read the image.")
        break
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1)
cap.release()
