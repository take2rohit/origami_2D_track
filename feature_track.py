import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture('videos/pull_slinky.MOV')
cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)


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
tracker_name = "csrt"
tracker = OPENCV_OBJECT_TRACKERS[tracker_name]()

def get_iou(bb1, bb2):
	
	assert bb1['x1'] < bb1['x2']
	assert bb1['y1'] < bb1['y2']
	assert bb2['x1'] < bb2['x2']
	assert bb2['y1'] < bb2['y2']

	x_left = max(bb1['x1'], bb2['x1'])
	y_top = max(bb1['y1'], bb2['y1'])
	x_right = min(bb1['x2'], bb2['x2'])
	y_bottom = min(bb1['y2'], bb2['y2'])

	if x_right < x_left or y_bottom < y_top:
		return 0.0

	intersection_area = (x_right - x_left) * (y_bottom - y_top)


	bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
	bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

	iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
	assert iou >= 0.0
	assert iou <= 1.0
	return iou

def checkallboxes(bb):
	length_list = len(bb)

	bb_copy = bb.copy()
	for i in range(length_list):
			for j in range(i+1, length_list):
				try:
					iou = get_iou(bb_copy[i], bb_copy[j])
					if iou != 0:
						bb_copy.remove(bb_copy[j])
						length_list -= 1

				except Exception as e:
					pass
	return bb_copy

def boxes_to_track(frame, no_of_features=10, bbox_size=20):
	frame_copy = frame.copy()
	gray = cv2.cvtColor(frame_copy,cv2.COLOR_BGR2GRAY)

	corners = cv2.goodFeaturesToTrack(gray,no_of_features,0.01,10)
	corners = np.int0(corners)
	bboxes = []
	for i in corners:
		x,y = i.ravel()
		bbox = {'x1':x-bbox_size//2,'x2':x+bbox_size//2, 'y1':y-bbox_size//2, 'y2':y+bbox_size//2}
		bboxes.append(bbox)

	bbox_cleaned = checkallboxes(bboxes)
	boxes_mod = []

	for box in bbox_cleaned:
		w,h = box['x2'] - box['x1'],  box['y2']-box['y1']
		box_mod = (box['x1'],  box['y1'], w, h)
		boxes_mod.append(box_mod)

	return boxes_mod

if __name__ == '__main__':

	ret,frame = cap.read()
	boxes_calc = boxes_to_track(frame,no_of_features=50)
	frame_no = 0 
	while True:
		
		if frame_no < len(boxes_calc):
			(success, boxes) = trackers.update(frame)

			box = boxes_calc[frame_no]
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
			cv2.circle(frame,(x+w//2,y+w//2), 3,(255,0,0),thickness=3)
		
			tracker = OPENCV_OBJECT_TRACKERS[tracker_name]()
			trackers.add(tracker, frame, box)
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
		
		else:
			ret,frame = cap.read()	
			(success, boxes) = trackers.update(frame)
			for box in boxes:
				(x, y, w, h) = [int(v) for v in box]
				cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

			# save this frame as video
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
			if key == ord("q"):
				break


		frame_no+=1

	cap.release()	
	cv2.destroyAllWindows()