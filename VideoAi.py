import os
import time

from imutils.video import VideoStream,FPS
import asyncio
import numpy as np
import argparse
import imutils
import cv2
from telebot import TeleBot

ap = argparse.ArgumentParser()
ap.add_argument('-p','--prototxt',required=True, help='path to Caffe deploy')
ap.add_argument('-m','--model',required=True,help='compiled model')
ap.add_argument('-c','--confidence',type=float,default=0.2,help='minimum probability')
args = vars(ap.parse_args())

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


print('loading model....')
net = cv2.dnn.readNetFromCaffe(args['prototxt'],args['model'])
print('loading complete')


def start(message, bot: TeleBot):
    print(message)
    bot.send_message(chat_id=message.chat.id, text='Stream loading...')
    print('start videostream...')
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()
    bot.send_message(chat_id=message.chat.id, text='Stream starting')
    while True:
        frame = vs.read()
        frame = imutils.resize(frame,width=700)
        (h,w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame,(700,700)),0.007843,(700,700),127.5)

        net.setInput(blob)
        detections = net.forward()

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0,0,i,2]
            if confidence > args['confidence']:
                idx = int(detections[0,0,i,1])
                box = detections[0,0,i,3:7] * np.array([w,h,w,h])
                (startX, startY,endX,endY) = box.astype('int')
                label = '{}: {:.2f}%'.format(CLASSES[idx],confidence*100)

                if CLASSES[idx] =='person':
                    cv2.imwrite('face_detection.img', frame)
                    img = open('face_detection.img', 'rb')
                    bot.send_photo(chat_id=message.chat.id, photo=img)
                    img.close
                    os.remove('face_detection.img')

                cv2.rectangle(frame,(startX,startY),(endX,endY),COLORS[idx],2)
                y = startY - 15 if startY -15 >15 else startY
                cv2.putText(frame,label, (startX,y), cv2.FONT_HERSHEY_TRIPLEX,0.5,COLORS[idx],2)

        cv2.imshow('Frame',frame)
        if message == 'stop':
            break

        fps.update()
    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()


#for start command
#python VideoAi.py -p MobileNetSSD_deploy.prototxt.txt -m MobileNetSSD_deploy.caffemodel
