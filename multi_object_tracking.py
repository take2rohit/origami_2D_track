import imutils
import time
import cv2
import numpy as np

OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,  
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}
 
trackers = cv2.MultiTracker_create()
cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)

kernel = np.ones((23,23),np.uint8)
tracker_name = "csrt"
cap = cv2.VideoCapture('/home/rohit/Downloads/IMG_5147.MOV')


def hand_segment(frame):
	frame_copy = frame.copy()
	frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# frame = cv2.inRange(frame_HSV, (0, 100, 127), (16, 153, 166))
	H_low, S_low, V_low = 10, 20, 35
	H_high, S_high, V_high = 25, 25, 48
	frame = cv2.inRange(frame_HSV, (int(H_low//2), int(S_low*2.55), int(V_low*2.55)), 
		(int(H_high//2), int(S_high*2.55), int(V_high*2.55)))

	frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
	_, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2 .CHAIN_APPROX_SIMPLE)
	
	if len(contours) > 0 : 
		max_area = 0
		for c in contours:
			rect = cv2.minAreaRect(c)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			area = cv2.contourArea(np.array(box))
			if area > max_area:
				max_area = area
				max_area_cnt = [box]
			
		return max_area_cnt
	
	else:
		return None


# if __name__ == '__main__':
# frame = cv2.imread('/home/rohit/Pictures/vlcsnap-2020-04-30-18h36m16s605.png')

ret,frame = cap.read()
mask = np.zeros_like(frame)
print(mask.shape)
magnet_coordinates, origami_coordinates = [],[]
while True:

	ret,frame = cap.read()
	
	if frame is None:
		break
	frame = cv2.flip(frame, 0)
	frame = cv2.flip(frame, 1)
	frame_copy = frame.copy()
	# max_area_cnt = hand_segment(frame)

	# if max_area_cnt is not None:
	# 	cv2.drawContours(frame,max_area_cnt,0,(0,0,255),3)
	
	(success, boxes) = trackers.update(frame)

	if len(boxes) == 2:
		for i, box in enumerate(boxes):
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (255, 0, 0), 2)
			coordinate = (x+w//2,y+h//2)
			cv2.circle(mask,coordinate, 3, (0,255,255),thickness=3)
			cv2.circle(frame_copy,coordinate, 3, (0,255,255),thickness=3)
			frame_copy = cv2.bitwise_or(mask,frame_copy)
			
			if i == 1:
				origami_coordinates.append(coordinate)
			elif i == 0:
				magnet_coordinates.append(coordinate)


	cv2.imshow("Frame", frame_copy)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("s"):

		box = cv2.selectROI("Frame", frame_copy, fromCenter=False,
			showCrosshair=True)
		tracker = OPENCV_OBJECT_TRACKERS[tracker_name]()

		trackers.add(tracker, frame, box)
	elif key == ord("q"):
		break
# np.save('origami_coordinates.npy', np.array(origami_coordinates))
# np.save('magnet_coordinates.npy', np.array(magnet_coordinates))
print('coordinates saved!')
cap.release()	
cv2.destroyAllWindows()