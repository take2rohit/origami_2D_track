from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import numpy as np

def clipper(l,thresh):
    k = []
    for item in l:
        if item < thresh:
            k.append(thresh)
        else:
            k.append(item)
    return k

magnet = np.load('/home/rohit/projects/gamitrack/magnet_coordinates.npy')
origami = np.load('/home/rohit/projects/gamitrack/origami_coordinates.npy')


magnet_x,magnet_y = magnet[:,0],magnet[:,1]
origami_x,origami_y = origami[:,0],origami[:,1]

magnet_y = clipper(magnet_y,820)

magnet_y_filter = gaussian_filter(magnet_y, sigma=1)
magnet_x_filter = gaussian_filter(magnet_x, sigma=1)
origami_x_filter= gaussian_filter(origami_x, sigma=1)

fps = 30
t_interval = 1/fps
t = [t_interval*i for i in range(0, len(origami_x_filter),1)]
    
# print('##########')
# print((magnet_x_filter))

# plt.subplot(2,1,1)
# plt.title("Magnet movement (Filtered)")
# plt.xlabel('Time (in sec)')
# plt.ylabel('Magnet y-coordinate wrt camera image')
# plt.plot(t,magnet_y_filter)

# plt.subplot(2,1,2)
# plt.title("Origami movement (Filtered)")
# plt.xlabel('Time (in sec)')
# plt.ylabel('Origami x-coordinate wrt camera image')
# plt.plot(t,origami_x_filter)
np.diff()
fit = np.polyfit(t,magnet_x_filter,1)
linear_fitted_magnet_x_filter = fit[1] + fit[0] * np.array(t)
# plt.subplot(2,1,2)
# plt.title("Magnet movement (Filtered)")
# plt.xlabel('Time (in sec)')
# plt.ylabel('Magnet x-coordinate wrt camera image')
# plt.plot(t,linear_fitted_magnet_x_filter,label='Best fit line')
# plt.plot(t,magnet_x_filter,label='Magnet x-coordinate')
# plt.legend()
# plt.plot(t)

plt.title("Trajectory with filters")
plt.xlabel('x-coordinate wrt camera image')
plt.ylabel('y-coordinate wrt camera image')
plt.plot(linear_fitted_magnet_x_filter, -magnet_y_filter, label='magnet trajectory')
plt.plot(linear_fitted_magnet_x_filter,  -origami_y, label='origami trajectory')
plt.legend()
# for i,j in zip(magnet_x_filter,magnet_y) :
#     print(i,j)
    


plt.show()  