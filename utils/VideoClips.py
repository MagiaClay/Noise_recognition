import cv2
import os
from argparse import ArgumentParser
# 此脚本用于切分本地视频
parser = ArgumentParser()
parser.add_argument(
    '--input', type=str, default='', help='Image/Video file')
parser.add_argument(
    '--output', type=str, default='', help='Image/Video file')

args = parser.parse_args()


def split_video(kwrags=None):
    if not os.path.exists(kwrags.output):
        os.makedirs(kwrags.output)

    cap = cv2.VideoCapture(kwrags.input)
    files_num = len(os.listdir(kwrags.output))
    index = 0
    while cap.isOpened():
        ret, frame = cap.read() # 每一次读取帧数,ret是是否读取到文件结尾，
        files_num = len(os.listdir(kwrags.output))
        if frame is not None:
            cv2.imshow("window", frame) # 在窗口上显示每一帧
            if index % 5 == 0 :   # 每四帧经行一次抽取
                cv2.imwrite(os.path.join(kwrags.output, f"{str(files_num + 1)}.jpg"), frame)
            index += 1
        if cv2.waitKey(5) & 0xFF == 27: # 按下'esc'结束抽帧
            cap.release()
            cv2.destroyAllWindows()
            break
        if not ret:
            break # 视频读到结尾则结束


if __name__ == '__main__':
    split_video(kwrags=args)
