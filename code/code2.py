import cv2
import os
import time

def capture_image(frame, trigger_signal=None, save_dir="../dataset"):
    # ...（函数体保留你现在的，不用动）...
    pass

def main():
    # 【关键修改：完全照搬教程的初始化】
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(cv2.CAP_PROP_FPS, 10)
    
    # 教程里被挡住的两行大概率是下面这两句（这是解决 WSL 摄像头发绿的“神级代码”）：
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    # 如果你能找到教程那一行具体写了什么，复制进去最好；如果找不到，用上面这行 MJPG 绝对管用。

    print("摄像头已启动，按 's' 键拍照保存，按 'q' 或 'ESC' 退出...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame.")
            break

        cv2.imshow('Video Preview', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s'):
            print("触发抓拍...")
            capture_image(frame, save_dir="../dataset")
        elif key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
