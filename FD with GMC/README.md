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
