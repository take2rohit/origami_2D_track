import numpy as np
import cv2
p1 = []
p2 = []
p3 = []

global points
points = []
cv2.namedWindow('image',cv2.WINDOW_NORMAL)

def draw_circle(event,x,y,flags,param):
	global mouseX,mouseY
	if event == cv2.EVENT_LBUTTONDBLCLK:
		cv2.circle(frame,(x,y),4,(255,0,0),-1)
		mouseX,mouseY = x,y
		points.append([x,y])
		print(x,y)
cv2.setMouseCallback('image',draw_circle)
cap = cv2.VideoCapture('clipped_video/tumble_crop.mp4')
frame_no = 0
while 1:
	try:
		frame_no += 1
		_,frame = cap.read()
		key = cv2.waitKey(0) & 0xff
		frame = cv2.putText(frame, str(len(points)/3), (100, 100) , cv2.FONT_HERSHEY_SIMPLEX , 4, (255, 0, 0),5) 
		cv2.imshow('image',frame)
		print("frame: ", frame_no) 
		
		if key  == ord("q"):
			# np.save('saved_files/tumbling/origami.npy', np.array(points))
			# np.save('saved_files/tumbling/magnet.npy', np.array(points))
			break

	except Exception as e:
		np.save('saved_files/tumbling/origami.npy', np.array(points))
		# np.save('saved_files/tumbling/magnet.npy', np.array(points))
		break
print('Tracking saved')         