# Anti-UAV Hybrid Tracker : YOLOv5 + SiamFC with GMC

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-Red)
![OpenCV](https://img.shields.io/badge/OpenCV-Green)
![Challenge](https://img.shields.io/badge/CVPR%202025-Anti--UAV%20Workshop-orange)

This repository contains an Infrared (IR) based small Unmanned Aerial Vehicle (UAV) tracking pipeline, specifically developed for the **CVPR 2025 Anti-UAV Workshop & Challenge (Track 1 : Single UAV Tracking)** dataset.

Inspired by the core logic of the paper *"A Simple Detector with Frame Dynamics is a Strong Tracker"*, this project integrates a globl object detector (YOLO) with a local tracker (SiamFC). 
It maximizes tracking robustness against extremely small drones by applying **Optical Flow-based Global Motion Compensation (GMC)** and **Motion Mask-based Trajectory Constraint Filtering (TC-Filtering)**.

## Key Features
* **Hybrid Tracking Pipeline** : Invokes **YOLOv5** for global detection when the target is initially searched or lost, and utilizes the lightweigth **SiamFC** for high-speed local tracking during continuous frames.
* **Optical Flow-based GMC** : Utilizes 'Lucas-Kanade Optical Flow' and the 'RANSAC' algorithm to track background feature points and derive a 2D Affine transformation matrix. This mathematically cancels out severe camera shake (ego-motion).
* **Robust TC-Filtering** : Extracts purely moving objects by thresholding the difference image between the GMC-warped previous frame and the current frame. It calculates the area ratio of moving pixels within the predicted bounding box to filter out fake targets. (background noise) and seamlessly trigger YOLO re-detection.

## Repository Structure

```text
.
├── Baseline_code/          # SiamFC model weights (model.pth) and core tracker modules
├── video_To_be_Improved    # Results that should be improved
├── video_good              # Good Results
├── README.md               
├── TC_Filtering.py         # Main execution script with TC-Filtering
├── detection_siamfc.py     # 
├── siamfc.py               # Results that should be improved
├── test_detection_tracking # Main execution script without TC-Filtering
├── test_siamfc.py          # 
```

## Results
* **Baseline (YOLO + SiamFC)** : Experienced drifting where the tracking box gets stuck on the screen edges by mistaking background noise for the drone, and easily lost the target during severe camera shaking.
https://github.com/user-attachments/assets/efd3c908-65b7-406c-84c6-1fd5ea0380cb
https://github.com/user-attachments/assets/65babfa3-9e6d-4e62-b33d-93bb5ddb204d
https://github.com/user-attachments/assets/68895e29-780d-4033-b205-c5f78f4dd765

* **Ours (+ GMC & TC-Filtering)** : Effectively compensates for severe video shaking and robustly ignores stationary false positives. (e.g., Buildings, Clouds, and Trees) in the background. This approach significantly improved tracking success rates and Intersection over Union (IoU) scores.

https://github.com/user-attachments/assets/dacfaab7-75d1-47d7-b4a1-bac3fca97281
https://github.com/user-attachments/assets/e693f604-12d9-450a-bda6-b8ab3f2bcb99

## References
* [CVPR 2025 Anti-UAV Workshop & Challenge](https://anti-uav.github.io/)
* Paper : *"A Simple Detector with Frame Dynamics is a Strong Tracker"*
* Codebase adapted from SiamFC and YOLOv5 official repositories.
