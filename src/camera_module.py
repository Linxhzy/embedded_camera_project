import cv2
import os
import time
class CameraCapture:
    def __init__(self,save_dir="dataset/images",camera_id=0):
        self.save_dir = save_dir
        self.camera_id = camera_id
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir,exit_ok=True)
            print(f"[初始化]创建保存目录：{self.save_dir}")
    def capture_single_image(self):
        #单次拍照并保存
        cap = None
        try:
            cap=cv2.VideoCapture(self.camera_id,cv2.CAP_V4L2)
            if not cap.isOpened():
                return False,"打开摄像头失败"
            #连续读5帧，防止3刚打开摄像头拍摄效果不好
            # 强制设置分辨率
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            # 强制使用 MJPG 格式
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
                
            for i in range(10):
                cap.read()
            time.sleep(0.5)
            #抓取1帧
            ret,frame=cap.read()
            if ret:
                #以时间命名
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename=os.path.join(self.save_dir,f"capture_{timestamp}.jpg")
                #保存图片
                cv2.imwrite(filename,frame)
                return True,filename
            else:
                return False,"读取失败"

        except Exception as e:
            print(f"抓拍异常{str(e)}")
            return False
        finally:
            if cap is not None:
                cap.release()
