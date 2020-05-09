import numpy as np
import cv2
p1 = []
p2 = []
p3 = []

global points
points = []
def draw_circle(event,x,y,flags,param):
	global mouseX,mouseY
	if event == cv2.EVENT_LBUTTONDBLCLK:
		cv2.circle(frame,(x,y),5,(255,0,0),-1)
		mouseX,mouseY = x,y
		points.append([x,y])
		print(x,y)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
cap = cv2.VideoCapture('/home/rohit/projects/gamitrack/videos/tumble_crop.mp4')
frame_no = 0

while 1:
	frame_no += 1
	_,frame = cap.read()
	frame = cv2.flip(frame, 0)
	frame = cv2.flip(frame, 1)

	if frame_no > 65:
		# cv2.imshow('image',frame)
			
		key = cv2.waitKey(0) & 0xff
		
		if key  == ord("q"):
			break
		# if event == cv2.EVENT_LBUTTONDBLCLK:
			
		elif key == ord('a'):
			print(mouseX,mouseY)
	cv2.imshow('image',frame)
	# print(points)
	print(frame_no)
	print(len(points)/2)

# np.save('origami_custom_track.npy', np.array(points))
# np.save('magnet_origami_custom_track.npy', np.array(points))
print('Tracking saved')