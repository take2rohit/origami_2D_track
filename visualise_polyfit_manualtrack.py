import numpy as np
import cv2

frame_no = 0
pts = np.load('origami_custom_track.npy')

p1 = []
p2 = []
p3 = []

for i in range(0, len(pts), 3):
	p1.append(pts[i])    
	p2.append(pts[i+1])
	p3.append(pts[i+2])

cap = cv2.VideoCapture('/home/rohit/projects/gamitrack/videos/tumble_crop.mp4')
cv2.namedWindow('image',cv2.WINDOW_NORMAL)


while 1:

	frame_no += 1
	_,frame = cap.read()
	frame = cv2.flip(frame, 0)
	frame = cv2.flip(frame, 1)

	if 63 < frame_no <65 :
		
		for (x1,y1),(x2,y2),(x3,y3) in zip(p1,p2,p3):

			_,frame = cap.read()
			frame = cv2.flip(frame, 0)
			frame = cv2.flip(frame, 1)    
			if x3 < x1:
				((x1,y1),(x3,y3)) = ((x3,y3), (x1,y1))

			if x3 < x2:
				((x2,y2),(x3,y3)) = ((x3,y3), (x2,y2))
			x_single = [x1,x2,x3]
			y_single = [y1,y2,y3]
			print(x_single,y_single)
			
			deg = 2
			fit = np.polyfit(x_single,y_single,deg)
			t = np.arange(x_single[0],x_single[2],0.5)

			if deg == 2:
				y_fit = fit[0] * t**2  + fit[1] * t +  fit[2]
			if deg == 1:
				y_fit = fit[0] * t + fit[1]

			for x,y in zip(t,y_fit):
				cv2.circle(frame,(int(x),int(y)), 3, (0,255,255),thickness=3)
				# cv2.circle(mask,(int(x),int(y)), 3, (255,0,col_r),thickness=1)
				# cv2.circle(mask_clear,(int(x),int(y)), 3, (0,0,0),thickness=1)
			cv2.circle(frame,(x1,y1),5,(255,0,0),-1)   
			cv2.circle(frame,(x2,y2),5,(0,255,0),-1)   
			cv2.circle(frame,(x3,y3),5,(0,0,255),-1)        
			cv2.imshow('image',frame)
			key = cv2.waitKey(0) & 0xff
		
	elif frame_no >65:
		break

cap.release()
cv2.destroyAllWindows()