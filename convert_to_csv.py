import numpy as np
import csv

pts_origami = np.load('saved_files/inchworm_forward/magnet.npy')

with open('saved_files/inchworm_forward/magnet.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow( ['point 1','point 2','point 3'] )
    for i in range(0, len(pts_origami), 3):
        writer.writerow([pts_origami[i], pts_origami[i+1], pts_origami[i+2]])

