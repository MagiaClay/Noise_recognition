# URL地址 base1: http://10.83.9.150:19935/HAIKANG/192.168.6.56/hls.m3u8
# URL地址 base2: http://10.83.9.150:19935/HAIKANG/192.168.6.59/hls.m3u8
# 此脚本用于接受URL视频流并保存为图片
import threading
import os
import cv2


class ThreadedCamera(threading.Thread):
    def __init__(self, source, save_path):  # 此处为默认打开0号相机，可以更新为URL流式I/O处理
        threading.Thread.__init__(self)  # 对父类的构造方法
        self.capture = cv2.VideoCapture(source)  # 此处会打开摄像头，初始化

        # self.thread = Thread(target=self.update, args=())  # 构造函数生成一个子线程，更新update函数
        self.daemon = False  # 默认为False，表示是一个前台线程，作用为当前所有前台线程都执行完毕时程序才推出，True则为后台线程，主线程结束后，所有线程也更这结束
        # self.thread.start()
        self.status = False  # 是否是到视频结尾，True表示视频正在经行，False表示视频已经结束
        self.frame = None  # 当前视频帧
        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def run(self):
        print(f'Thread {self.name} start！')
        self.update()

    def __del__(self): # 析构函数，在程序以外推出后释放内存
        self.stop_read()
        print(f'Thread {self.name} release！')

    # 该函数用于执行线程更新函数
    def update(self):
        index = 0
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
                # TODO: 帧处理，间隔经行帧采样，并保存到指定路径
                if self.frame is not None:
                    # cv2.imshow("window", frame)  # 在窗口上显示每一帧
                    if index % 25 == 0:  # 每四帧经行一次抽取
                        cv2.imwrite(os.path.join(self.save_path, f"{str(index // 24 + 1)}_59.jpg"), self.frame)  # 将图像保存到指定位置,记得更换URL
                        print(f'{os.path.join(self.save_path, f"{str(index // 24 + 1)}_59.jpg")} has saved')
                    index += 1
                if not self.status:
                    break  # 视频读到结尾则结束

    def isOpened(self):
        return True if self.capture.isOpened() else False

    # 获得当前frame
    def read(self):
        if self.status:
            return self.frame
        return None

    def stop_read(self):
        self.capture.release()  # 释放资源的函数

    def get(self, fps):
        return self.capture.get(fps)  # 获得当前读取帧数


if __name__ == '__main__':
    thread = ThreadedCamera('http://10.83.9.150:19935/HAIKANG/192.168.6.59/hls.m3u8',
                            r'D:\AI_fileCollected\Datasets\Helmet_evalue\Images_59/')  # 打开视频流
    thread.start()  # 启动线程，主线程结束后进程才结束
