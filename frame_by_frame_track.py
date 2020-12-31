import numpy as np
import cv2
import pandas as pd

def nothing(x):
    pass

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

def draw_circle(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		c = int(frame_points[frame_no]%points_to_track)
		keypoints[frame_no,c,0] = x
		keypoints[frame_no,c,1] = y
		frame_points[frame_no] += 1

def header(points_to_track, frame_count, frame_skip):
	head = []
	index = []
	for i in range (points_to_track):
		head.append('x'+ str(i+1))
		head.append('y'+ str(i+1))
	for i in range (frame_count):
		index.append('frame_'+ str(i*frame_skip+1))
	return head, index

cv2.setMouseCallback('image', draw_circle)
cap = cv2.VideoCapture('clipped_video/omega.mp4')
frame_no = 0
points_to_track = 5
fps = 10
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_skip = int(cap.get(cv2.CAP_PROP_FPS)/fps)
frame_count = int(length/frame_skip)
cv2.createTrackbar('Frame','image',0,frame_count-1,nothing)
frame_no = 1
keypoints = np.zeros((frame_count,points_to_track,2))
frame_points = np.zeros(frame_count)

while 1:
		cv2.setTrackbarPos('Frame', 'image', frame_no)
		cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no*int(cap.get(cv2.CAP_PROP_FPS)/fps))
		_,frame = cap.read()
		for i in range(points_to_track):
			cv2.circle(frame,(int(keypoints[frame_no,i,0]),int(keypoints[frame_no,i,1])),4,(255,0,0),-1)
		
		cv2.imshow('image',frame)
		key = cv2.waitKey(1) & 0xff
		frame_no = cv2.getTrackbarPos('Frame','image')
		
		if key == 100:	#press 'd' for next frame
			frame_no = cv2.getTrackbarPos('Frame','image') + 1

		if key == 97:	#press 'a' for prev frame
			frame_no = cv2.getTrackbarPos('Frame','image') - 1

		if key == ord("q"):	#press 'q' to save data as a csv file
			keypoints = np.reshape(keypoints,(frame_count,2*points_to_track))[1:]
			header, index = header(points_to_track, frame_count-1, frame_skip)
			df = pd.DataFrame(keypoints, index=index, columns=header)
			df.to_csv('saved_files/keypoints.csv', index=True, header=True, sep=',')
			print('Tracking saved')      
			break
		

	