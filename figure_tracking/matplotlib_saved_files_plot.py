import numpy as np
import matplotlib.pyplot as plt 

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
	r = round(np.sqrt(sqr_of_r), 5)  
	return (h,k), r 


def arc_points_interpolate(p1,p2,p3,h,k, r):
	x1,x2,x3 = p1[0],p2[0],p3[0]
	xmin, xmax = min(x1,x2,x3), max(x1,x2,x3)
	x_range = np.arange(xmin, xmax,0.1)    
	x_rem = [x1,x2,x3]
	x_rem.remove(xmin)
	x_rem.remove(xmax)
	x_rem = x_rem[0]
	y_top,y_down = [],[]
	for pt in [p1,p2,p3]:
		if x_rem in pt:
			y_rem = pt[1]
	
	for x in x_range:
		y_top.append(k + np.sqrt(r**2 - (x-h)**2))
		y_down.append(k - np.sqrt(r**2 - (x-h)**2))
	
	y_top_dist,y_down_dist = np.average(np.abs(np.array(y_top)-y_rem)),np.average(np.abs(np.array(y_down)-y_rem))

	if y_top_dist<y_down_dist:
		y_sel = y_top
		# print('y_top')
	else:
		y_sel = y_down
		# print('y_down') 
	
	return x_range, y_sel
	

pts_origami = np.load('saved_files/omega/origami.npy')
pts_magnet = np.load('saved_files/rolling/magnet.npy')


p1_origami = []
p2_origami = []
p3_origami = []

p1_magnet,p2_magnet = [],[]

for i in range(0, len(pts_origami), 3):
	p1_origami.append(pts_origami[i])    
	p2_origami.append(pts_origami[i+1])
	p3_origami.append(pts_origami[i+2])

print(p2_origami)

for i in range(0, len(pts_magnet), 2):
	p1_magnet.append(pts_magnet[i])    
	p2_magnet.append(pts_magnet[i+1])

val = 0
inc = 1/len(p1_origami)
for p1,p2,p3 in zip(p1_origami,p2_origami,p3_origami):
    
    (h,k), r = findCircle(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
    x_range,y_sel = arc_points_interpolate(p1,p2,p3,h,k,r)
    plt.plot(x_range,-np.array(y_sel),color=[val,0,1])
    val+=inc

plt.show()