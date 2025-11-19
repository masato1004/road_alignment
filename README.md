# Vanishing Point Detection for Road Alignment
## Method
- Crop needed area as road, like bottom half
- Smoothing image to denoise
- Edge detection using canny method
- Line detectino using hough method
- Pick the two lines that are most likely road boundaries
- Calculate crossing point of the two lines as the vanishing point

## Process Example
### Detected Edge
![edges_straight](https://github.com/user-attachments/assets/32689def-430e-4eae-9672-39da2d8ff690)
![edges_straight2](https://github.com/user-attachments/assets/93976d98-0f99-47a7-8263-9f0f540c9b11)
![edges_curve](https://github.com/user-attachments/assets/3a2c0876-6089-4f9b-a136-fe9f70379c31)
![edges_small_curve](https://github.com/user-attachments/assets/d4a857ea-185e-4b84-b583-2843668ca4db)

### Detected Road Boundaries and Vanishing Point
![vp_straight](https://github.com/user-attachments/assets/d75021dc-976e-4abb-9d62-bd2e3dfdc36c)
![vp_straight2](https://github.com/user-attachments/assets/1be41ab1-0bea-43a8-adf7-13b939e13a06)
![vp_curve](https://github.com/user-attachments/assets/acf5d181-ee55-456c-84f1-6a2a3a065e30)
![vp_small_curve](https://github.com/user-attachments/assets/0a9d0f6d-0972-42ca-8c48-528480ab5165)
