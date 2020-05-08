import matplotlib.pyplot as plt
import numpy as np

p1 = np.load('p1.npy')
p2 = np.load('p2.npy')
p3 = np.load('p3.npy')

p1_x, p1_y = p1[:,0], p1[:,1]
p2_x, p2_y = p2[:,0], p2[:,1]
p3_x, p3_y = p3[:,0], p3[:,1]

col_b  = 0

start = 40
total_frame = len(p3_x)
step = 70

for i in range(start,total_frame,step):
    
    x_single = [p1_x[i],p2_x[i],p3_x[i]]
    y_single = [p1_y[i],p2_y[i],p3_y[i]]
    
    fit = np.polyfit(x_single,y_single,2)
    t = np.arange(x_single[0],x_single[2],0.01)

    y_fit = fit[0] * t**2  + fit[1] * t +  fit[2]
    plt.plot(t,-y_fit, color=[col_b,0,1 ])
    col_b = col_b + step/(total_frame-start)
    print(col_b)
plt.show()


