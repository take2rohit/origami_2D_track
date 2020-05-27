import numpy as np
import csv

pts_magnet = np.load('saved_files/tumbling/magnet.npy')

with open('saved_files/tumbling/magnet.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow( ['point 1','point 2'] )
    for i in range(0, len(pts_magnet), 2):
        writer.writerow([pts_magnet[i], pts_magnet[i+1]])
