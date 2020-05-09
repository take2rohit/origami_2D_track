import time
import cv2
import numpy as np
# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations

OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}

# initialize OpenCV's special multi-object tracker
trackers = cv2.MultiTracker_create()
algo = 'csrt'
cv2.namedWindow('mask',cv2.WINDOW_NORMAL)
# cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)

# otherwise, grab a reference to the video file

vs = cv2.VideoCapture('/home/rohit/projects/gamitrack/videos/tumble_crop.mp4')
_,frame = vs.read()
mask = np.zeros_like(frame)
mask_clear = np.zeros_like(frame)
mask_clear = 255-mask_clear

p1 , p2, p3 = [], [], []
c=0
frame_no = 0
col_r = 25

while True:
	frame_no+=1
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	_,frame = vs.read()
	frame = cv2.flip(frame, 0)
	frame = cv2.flip(frame, 1)
	# check to see if we have reached the end of the stream
	

	# resize the frame (so we can process it faster)

	# grab the updated bounding box coordinates (if any) for each
	# object that is being tracked
	
	(success, boxes) = trackers.update(frame)
	if len(boxes) == 3:
		c+=1
		for i, box in enumerate(boxes):
			(x, y, w, h) = [int(v) for v in box]
			# cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
			coordinate = (x+w//2,y+h//2)
			# cv2.circle(mask,coordinate, 3, (0,255,255),thickness=3)
			cv2.circle(frame,coordinate, 3, (0,255,255),thickness=3)
			# frame = cv2.bitwise_or(mask,frame)
			
			if i == 0:
				p1.append(coordinate)
			elif i == 1:
				p2.append(coordinate)
			elif i == 2:
				p3.append(coordinate)
		
		if c>2 and frame_no%20 == 0:
			
			col_r+= 5
			p1_c = np.array(p1)
			p2_c = np.array(p2)
			p3_c = np.array(p3)

			for box in boxes:

				p1_x, p1_y = p1_c[-1,0], p1_c[-1,1]
				p2_x, p2_y = p2_c[-1,0], p2_c[-1,1]
				p3_x, p3_y = p3_c[-1,0], p3_c[-1,1]

				x_single = [p1_x,p2_x,p3_x]
				y_single = [p1_y,p2_y,p3_y]
				fit = np.polyfit(x_single,y_single,2)

				t = np.arange(x_single[0],x_single[2],0.5)
				y_fit = fit[0] * t**2  + fit[1] * t +  fit[2]

				for x,y in zip(t,y_fit):

					cv2.circle(frame,(int(x),int(y)), 3, (0,255,255),thickness=3)
					cv2.circle(mask,(int(x),int(y)), 3, (255,0,col_r),thickness=1)
					cv2.circle(mask_clear,(int(x),int(y)), 3, (0,0,0),thickness=1)



	for box in boxes:
		(x, y, w, h) = [int(v) for v in box]
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

	frame = cv2.bitwise_and(frame,mask_clear)
	frame = cv2.bitwise_or(mask,frame)
			
	# show the output frame
	cv2.imshow("Frame", frame)
	cv2.imshow("mask", mask)
	key = cv2.waitKey(0) & 0xFF
	print(frame_no)

	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		box = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)

		# create a new object tracker for the bounding box and add it
		# to our multi-object tracker
		tracker = OPENCV_OBJECT_TRACKERS[algo]()
		trackers.add(tracker, frame, box)

	# if the `q` key was pressed, break from the loop
	elif key == ord("q"):
		break

# np.save('p1.npy', np.array(p1))
# np.save('p2.npy', np.array(p2))
# np.save('p3.npy', np.array(p3)) 
# print('saved')
vs.release()
cv2.destroyAllWindows()