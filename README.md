Group A (Carl, Tony, Manuel)
Auto-labeler:  
Task 1: everyone is able to run through the auto-labeling tool
Dataset: 
March 28, 2026  (Successfully running the auto-labeling)
Carl & Manuel: able to view all the frames in the auto-labeling tool
Tony: some frames not loading and the other frames load fine. The same error as Carl found in the Oct 17, 2025 dataset.
Oct 17, 2025: error while open the files
Propose: It might be the ROI not provided

Task 2: Add a feature for the auto-labeling tool to add a bounding box for the reference point
Location of the bounding box should be determined by drag and drop
Size should be adjustable
The object will be named as reference object, and color for the reference object (golden?) should be different from the vehicle types and other objects
const CLASS_COLORS: Record<string, string> = {
	Sedan: '#2563eb', (blue)
	SUV: '#16a34a', (green)
	Van: '#f59e0b', (yellow)
	Truck: '#dc2626', (red)
	Bus: '#7c3aed', (violet)
	Cycle: '#0ea5e9', (sky blue)
	Vehicle: '#111827', (black)
	Unknown: '#6b7280', (gray)
};
(This is already implemented) Remove a bounding box: click to remove the bounding box for the reference object
Task 3: click a button, the same reference object will be added to all frames. 
Task 4: Click on the reference object bounding box to remove it from all frames in the current dataset.
Task 5: Write a script to label the same reference object for every frame across the whole dataset
Save the frames + any data from the frames (Can be found in VeloView). 


Group B (Matthew, Leonid, Alfonzo)
Task 1 (from last week): Research for algorithms to measure the distance (this could be math equations) between reference points and labeled cars in the frames. Share your research results: exact algorithms, and explain the algorithm to the team 
Leonid: Distance Measurement Algorithm Research

Research Google Doc: https://docs.google.com/document/d/1aZQ0jmuUhA2dNfcxM9o7HkFeU2rqx1LBbIrj25Qg2Qw/edit?usp=sharing](https://docs.google.com/document/d/1aZQ0jmuUhA2dNfcxM9o7HkFeU2rqx1LBbIrj25Qg2Qw/edit?usp=sharing

I researched 2D and 3D Euclidean distance formulas for calculating distances between reference objects and labeled vehicles in LiDAR frames. I also looked into how we could use the XYZ coordinates from the auto-labeling tool and identified possible issues with bounding-box accuracy and keeping reference points consistent across frames.

Next, I plan to test the formulas using actual LiDAR data and work with Group B on integrating the distance calculations into the project.

Task 2 (Alfonso): Write script to measure the distance between all the vehicles and the reference object
Select one reference object (manual choose values): make sure it is within the frame
Find out locations for all vehicles in the frame
Calculate and then output the values as shown in the following format
Frame Output format:
{frame_id: id
    reference_object_id: id,
    reference_object_location: 
    reference_object_size:
    vehicle_count: x,
    Vehicle: {
	Vehicle_id: some_id,
	Vehicle_type: sedan, 
      Vehicle_location_on_frame: xyz,
      Vehicle_bounding_box_size: xyz,
      Vehicle_distance_from_reference_object: some distance in (meters),
      Vehicle_confidence: 0-1,
      Vehicle_lane: Lane Label
    }
}



Task 3 (Matthew): Write script to calculate the speed of each vehicle between frames
Subtask 1: Ask ChatGPT for some sample data: 26 values
Subtask 2: Refer to distance of the same vehicle in two frames
Use the distance between the vehicle and the reference, subtract to know the movement of the vehicle
Time between the two frames: camera frequency (Ouster Lidar camera: 10Hz) 10 frames per second => time is 0.1 second
Speed: Distance/time 
Subtask 3: Use the dataset provided in the tutorial (March 2026) and run the labeling tool to add bounding boxes and extract location, dimension, and yaw for each vehicle in each frame, and exported the output files ()
Plan:
Subtask 4: Use the information extracted from the previous step (subtask 3), calculate the distance between frames for each vehicle
Challenge: how to identity the same vehicle in 2 frames
Calculate the distance of this vehicle between these 2 frames
Subtask 5: to calculate the speed of the vehicle every 1second (to keep consistent with the web application), then we can calculate every 5 seconds (double check with Shonan)
Task 4: Measure the distance between the vehicles and the lanes on the road (we can use the auto-labeler tool to add lane references)
https://arxiv.org/html/2504.08540v2 (2D lane detection)
Matlab built-in tool for lane detection: https://www.mathworks.com/help/driving/ug/lane-detection-in-lidar-data-using-deep-learning.html
This information could help us to identify which line the vehicle is in and find out the number of vehicles on each lane in the current frame
Task 5: LLM model read JSON file
congestion of traffic: density, vehicle type distribution, vehicle count


