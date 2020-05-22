import numpy as np
import cv2
from math import sqrt

def findCircle(x1, y1, x2, y2, x3, y3) : 
	x12 = x1 - x2  
	x13 = x1 - x3  

	y12 = y1 - y2  
	y13 = y1 - y3  

	y31 = y3 - y1  
	y21 = y2 - y1  

	x31 = x3 - x1  
	x21 = x2 - x1  

	# x1^2 - x3^2  
	sx13 = pow(x1, 2) - pow(x3, 2)  

	# y1^2 - y3^2  
	sy13 = pow(y1, 2) - pow(y3, 2)  

	sx21 = pow(x2, 2) - pow(x1, 2)  
	sy21 = pow(y2, 2) - pow(y1, 2)  

	f = (((sx13) * (x12) + (sy13) * 
			(x12) + (sx21) * (x13) + 
			(sy21) * (x13)) // (2 * 
			((y31) * (x12) - (y21) * (x13)))) 
				
	g = (((sx13) * (y12) + (sy13) * (y12) + 
			(sx21) * (y13) + (sy21) * (y13)) // 
			(2 * ((x31) * (y12) - (x21) * (y13))))  

	c = (-pow(x1, 2) - pow(y1, 2) - 
			2 * g * x1 - 2 * f * y1)  

	# eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0  
	# where centre is (h = -g, k = -f) and  
	# radius r as r^2 = h^2 + k^2 - c  
	h = -g  
	k = -f  

	sqr_of_r = h * h + k * k - c  

	# r is the radius  
	r = round(sqrt(sqr_of_r), 5)  
	return (h,k), r 

frame_in = np.zeros((1080,1920,3),dtype=np.uint8)
mask_white = 255 - np.zeros_like(frame_in)

def arc_arrow_draw(frame_in,x1,y1,x2,y2,x3,y3,m_x1,m_y1,m_x2,m_y2,h,k, r,val):
	x_range = np.arange(x1,x3,0.1)
	y_range = np.zeros_like(x_range)
	for x in x_range:
		y = k - np.sqrt(r**2 - (x-h)**2)
		cv2.circle(frame_in,(int(x),int(y)), 2, (255,0,val),thickness=-1)
		cv2.arrowedLine(frame_in,(m_x1,m_y1),(m_x2,m_y2), (255,0,val),2)
		cv2.circle(mask_white,(int(x),int(y)), 2, (0,0,0),thickness=-1)
		cv2.arrowedLine(mask_white,(m_x1,m_y1),(m_x2,m_y2), (0,0,0),2)
	return frame_in, mask_white
	

pts_origami = np.load('saved_files/inchworm_forward/origami.npy')
pts_magnet = np.load('saved_files/inchworm_forward/magnet.npy')
# print(pts_magnet.shape, pts_origami.shape)
p1_origami = []
p2_origami = []
p3_origami = []

p1_magnet = []
p2_magnet = []

for i in range(0, len(pts_origami), 3):
	p1_origami.append(pts_origami[i])    
	p2_origami.append(pts_origami[i+1])
	p3_origami.append(pts_origami[i+2])

for i in range(0, len(pts_magnet), 2):
	p1_magnet.append(pts_magnet[i])    
	p2_magnet.append(pts_magnet[i+1])

cap = cv2.VideoCapture('clipped_video/inchworm_forward_2.mp4')
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.namedWindow('traj',cv2.WINDOW_NORMAL)

frame_no, val = 0, 0
blank = np.zeros_like(frame_in)
while 1:

	
	for (x1,y1),(x2,y2),(x3,y3),(m_x1,m_y1), (m_x2,m_y2) in zip(p1_origami,p2_origami,p3_origami,p1_magnet,p2_magnet):
		
		_,frame = cap.read()  
		(h,k), r = findCircle(x1, y1, x2, y2, x3, y3)

		# cv2.circle(frame,(int(h),int(k)), int(r), (255,0,0),thickness=2)
		# cv2.circle(frame,(int(h),int(k)), 10, (0,0,255),thickness=-1)
		# cv2.arrowedLine(frame,(m_x1,m_y1), (m_x2,m_y2), (0,255,255),2)
		# cv2.imshow('image',frame)
 
		mask_col, mask_white = arc_arrow_draw(blank, x1,y1,x2,y2,x3,y3,m_x1,m_y1,m_x2,m_y2,h,k,r,val)
		
		mask = cv2.bitwise_and(mask_white,frame )
		traj = cv2.bitwise_or(mask, mask_col)

		# mask_coloured = cv2.bitwise_or(mask_coloured,mask_col.copy())
		cv2.imshow("traj", traj)
		val+=15
		key = cv2.waitKey(0) & 0xff

cap.release()
cv2.destroyAllWindows()