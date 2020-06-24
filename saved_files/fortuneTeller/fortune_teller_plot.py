import matplotlib.pyplot as plt
import numpy as np
import cv2

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

flap = np.load('saved_files/fortuneTeller/fortuneTeller.npy')
frame_no = 0

cap = cv2.VideoCapture('clipped_video/fortune_teller.mp4')
for pts in flap:

    _,frame = cap.read()
    cv2.circle(frame,tuple(pts), 6,(255,0,0),-1 )
    cv2.rectangle(frame, tuple(pts-32), tuple(pts+32),(0,0,255),thickness=4)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(100) & 0xff
    if key  == ord("q"):
        break