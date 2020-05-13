# Origami 2D Tracking 

## Video Demo
Various tracking results can be found [here](https://drive.google.com/drive/u/1/folders/1GapJK3oWHEMn0Bm4omrbM7fQUOPg2TjE)

## How to use this repo

### Manual Tracking
- `frame_by_frame_track.py` file helps you to track points in frame by frame. (Modifications required for magnet and origami by chaning number of points to track)

### Automatic Tracking
- Fails in high speed motion and 
- `multi_object_tracking.py` draw bounding box across 2 points in consecutive frame to start traking and saving into file. It also draws previous points
- `feature_track.py` automatically find top n features to track and tracks the position of each corners
- `optical_flow_tracking.py` Use good features to track points automatically using optical flow algorithm. No manual feature selection in required
- `skeleton_track.py` tracks multiple point and draws a fitted quadratic curve using 3 points

### Visualize tacking
- `visualise_circlefit_manualtrack.py` helps you to visualise the tracked points by fitting a circle
- `visualise_polyfit_manualtrack.py` helps you to visualise the tracked points by fitting a quadratic polynomial
- `trajectory_plotter.py` plots trajectory of magnet as well as origami using matplotlib

## Repository info
- This repo has mutliple algorithm to track the origami 
- Algorithms implemented
    1. csrt
    2. kcf
    3. boosting
    4. mil
    5. tld
    6. medianflow
    7. mosse 
    8. Optical Flow

## Contributer
- Rohit Lal  [(website)](https://take2rohit.github.io/)