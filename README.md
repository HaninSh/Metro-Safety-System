# Metro Safety System

### Project Overview
This project is part of the Digital Egypt Pioneers Initiatives (DEPI) graduation project within the Microsoft Machine Learning course. The "Metro Safety System" is designed to enhance the safety of subway passengers by monitoring platform activity in real-time. The system analyzes video streams from subway surveillance cameras, detecting both people on the platform and the safety yellow line. 

When a person touches or crosses the yellow line, the system triggers an alert to notify security personnel. This enables them to quickly review the situation and take immediate action to prevent potential accidents. By providing real-time awareness of dangerous scenarios, the system aims to reduce accidents and suicides, creating a safer environment for all passengers.

---

## Datasets Used

We trained our model using two datasets from Roboflow:

1. **Station Platform and Detecting Braille Blocks 2**  
   - **Link:** [Station Platform Dataset](https://universe.roboflow.com/hakujou/station-platform-and-detecting-braille-blocks-2/browse?queryText=&pageSize=200&startingIndex=0&browseQuery=true)  
   - Contains four classes: railway track, braille blocks, platform, and stop braille blocks.  
   - For our project, we focused on the `railway track` and `stop braille blocks` classes to define the safety zone boundaries.

2. **Person Dataset**  
   - **Link:** [Person Dataset](https://universe.roboflow.com/abner/person-hgivm/browse?queryText=&pageSize=50&startingIndex=50&browseQuery=true)  
   - Contains a single class: `person`.  
   - This dataset is essential for detecting individuals on the subway platform, ensuring accurate monitoring of human activity.

---

## Methodology

We utilized two YOLO v8m models after testing various models and sizes to achieve the best accuracy:

1. **Yellow Line Detection Model**  
   - Detects the yellow line specifying the danger zone on the platform.  
   - Also detects the railway tracks.

2. **Person Detection Model**  
   - Trained on a well-annotated person dataset to handle complex scenarios accurately.

After obtaining predictions from the models, the following processes are applied:

- **Yellow Line**: We use a hybrid algorithm combining color segmentation, masking, and edge detection within the bounding box area to determine the exact location of the yellow line. This returns the start and end points of the line.
  
- **Railway**: This annotation is used to:
  - Detect if a train is present at the station.
  - Identify the platform's position to specify which side of the station is dangerous.

- **Person**: Person detection is critical due to complex scenarios. We apply thresholds and algorithms to accurately identify the foot position of individuals for high accuracy.

---

## Key Features

- Handles most cases, aiming to save lives.
- Supports large masking ranges covering almost every metro platform line color with auto-completion using the start and end points of the line.
- The project generates multiple types of alerts:
  - **Red annotations** around persons detected in the danger zone.
  - **Counter updates** per frame for people detected in the danger zone.
  - **Flashing red alert** if someone crosses the line.

---

## Sample Output

<div align="center">
    <video width="600" controls>
        <source src="[https://your-username.github.io/your-repo-name/assets/video.mp4" type="video/mp4](https://github.com/HaninSh/Metro-Safety-System/tree/main/assests)">
        Your browser does not support the video tag.
    </video>
</div>

