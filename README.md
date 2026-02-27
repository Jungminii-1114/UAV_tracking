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
├── Baseline_code/                    # SiamFC model weights (model.pth) and core tracker modules
├── FD with GMC/                      # Visualization result of GMC, TC-Filtering, Optical Flow and Frame Difference
├── Optical Flow Implementation       # Implementation of Optical Flow to understand
├── video_To_be_Improved              # Results that should be improved
├── video_good                        # Good Results
├── README.md
├── [TCF]test_detection_tracking.py   # Main execution script with TC-Filtering (Tested for all cases - AOA : 0.6067)
├── detection_siamfc.py               # 
├── siamfc.py                         # Results that should be improved
├── test_detection_tracking           # Main execution script without TC-Filtering
├── test_siamfc.py                    # 
```

## Results
### **Baseline (YOLO + SiamFC)** 
**Experienced drifting where the tracking box gets stuck on the screen edges by mistaking background noise for the drone, and easily lost the target during severe camera shaking.**

https://github.com/user-attachments/assets/649c4628-1e1b-4bf6-ae85-c77b0a93f544

https://github.com/user-attachments/assets/8ddf019d-5b9c-4213-8e47-0e0de03e68d6

https://github.com/user-attachments/assets/6702e709-b14e-4b82-a010-5f7f61f9d5b0



### **Ours (+ GMC & TC-Filtering)** 
**Effectively compensates for severe video shaking and robustly ignores stationary false positives. (e.g., Buildings, Clouds, and Trees) in the background. This approach significantly improved tracking success rates and Intersection over Union (IoU) scores.**



https://github.com/user-attachments/assets/84640e70-8324-477c-9a39-2ada8041aa45

https://github.com/user-attachments/assets/425be747-b90f-413e-bbb2-408cfae7c3a5

https://github.com/user-attachments/assets/36b498a1-9f09-4959-8ce3-61510dc68e4f


https://github.com/user-attachments/assets/0691a8ba-0130-4ac0-a9d7-4480440c5dde




## Visualization : TC-Filtering based on GMC (Residual Analysis)
This visualization demonstrates the core mechanism of our pipeline : **Global Motion Compensation (GMC) combined with Binarization Filtering**. It effectively isolates the target even in challenging scenarios with severe camera moving and thermal clutter.

![new12_train_newfix_frame50_debug](https://github.com/user-attachments/assets/1a4a1e8d-ab3d-4774-aa4d-ad1eeed7f129)

![46_1_frame50_debug](https://github.com/user-attachments/assets/eea44176-686d-4299-af86-7989be61ba6e)

The extracted debug image illustrates the following three stages, from left to right:

1. **Origianl (GrayScale)** : the raw recurrent frame where the tiny drone target is mixed with complex background noise.
2. **Raw Residual (Pre-thresholding)** : The absolute difference between the current frame and the affine-warped previous frame. The static background is mostly canceld out, leaving only the physically moving target and strong structural edges.
3. **Thresholded Residual (Post-thresholding)** : The final result after applying a fixed threhold. Minor background residual noise is masked out, cleanly isolating the target candidates with distinct movement as pure white.

### Description : Motion-Compensated Redisual Analysis
* **Optical Flow** : Tracks robust background feature points between consecutive frames **to accurately estimate the camera's ego-motion (panning and tilitng).**
* **Frame Difference** : Utilizes the estimated motion matrix to align (warp) the previous frame to the current frame's perspective, effectively neutralizing camera movement.
* **GMC** : Suubtracts the GMC-aligned background from the current frame. This eliminates static thermal clutter and isolates only the physically moving target (UAV, drone) as the distinct residual.


## References
* [CVPR 2025 Anti-UAV Workshop & Challenge](https://anti-uav.github.io/)
* Paper : *"A Simple Detector with Frame Dynamics is a Strong Tracker"*
* Codebase adapted from SiamFC and YOLOv5 official repositories.

## Appendix
* [Datasets for Implementing Optical Flow (Lucas-Kanade)](https://lmb.informatik.uni-freiburg.de/Publications/2011/Bro11a/)
