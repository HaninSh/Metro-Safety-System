from video_processing import download_video, detect_yellow_line_in_stopbraille_blocks, add_transparent_rectangle, get_foot_position, install_requirements, download_models
import os

def requirements_installed():
    # Check if a requirements marker file exists (or use any package check mechanism)
    return os.path.exists('requirements_installed.flag')

# Function to check if the models directory exists and contains the expected models
def models_downloaded():
    model_files = ['Models/People_detection_weights(best).pt', 'Models/Line_detection_weights (best).pt']
    return all(os.path.exists(model_file) for model_file in model_files)

# Install requirements only if they haven't been installed yet
if not requirements_installed():
    install_requirements('requirements.txt')
    # Create a flag file to indicate that requirements have been installed
    with open('requirements_installed.flag', 'w') as f:
        f.write("Installed")

# Download models only if they aren't already downloaded
# if not models_downloaded():
#     download_models()

import cv2
from ultralytics import YOLO
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
import gdown


# Main function
def main(link:str):
    video_url = link
    video_save_path = 'Input_video/downloaded_video.mp4'

    # Download the video before processing
    if download_video(video_url, video_save_path):
        print("Video downloaded successfully!")
    else:
        print("Failed to download the video.")
        return

    # Load the YOLO models: one for detecting the railway track, one for detecting people
    line_model = YOLO('Models/Line_detection_weights (best).pt')  # Model for detecting railway track
    person_model = YOLO('Models/People_detection_weights(best).pt')  # Model for detecting people

    # Open the video file
    video_path = video_save_path
    cap = cv2.VideoCapture(video_path)

    # Get video properties for saving
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('Output_video/output_with_full_annotations.mp4', fourcc, fps, (width, height))

    # Initialize variables
    frame_count = 0
    red_annotation_active = 0
    railway_consecutive_frames = 0
    railway_track_position = None
    last_yellow_lines = []
    railway_to_left = None
    flashing_step = 0

    # Process each frame of the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect "stopbraille-blocks" and "Railway track" using the line model
        line_results = line_model(frame)
        stopbraille_blocks_bbox = None
        railway_track_found = False

        if line_results and line_results[0] is not None and len(line_results[0]) > 0:
            for *xyxy, conf, cls in line_results[0].boxes.data.tolist():
                class_name = line_model.names[int(cls)]
                if class_name == 'stopbraille-blocks':
                    stopbraille_blocks_bbox = list(map(int, xyxy))
                if class_name == 'Railway track':
                    railway_track_found = True
                    if railway_track_position is None:
                        railway_track_position = int((xyxy[0] + xyxy[2]) / 2)

        # Update the railway consecutive frame counter and activate red annotation if needed
        if railway_track_found:
            railway_consecutive_frames += 1
            if railway_consecutive_frames >= 3:
                red_annotation_active = 20
        else:
            railway_consecutive_frames = 0

        # Detect yellow lines
        yellow_lines = []
        if stopbraille_blocks_bbox:
            xmin, ymin, xmax, ymax = stopbraille_blocks_bbox
            yellow_lines = detect_yellow_line_in_stopbraille_blocks(frame, xmin, ymin, xmax, ymax)
            if yellow_lines:
                last_yellow_lines = yellow_lines

        if not yellow_lines and last_yellow_lines:
            yellow_lines = last_yellow_lines

        for line in yellow_lines:
            cv2.line(frame, line[0], line[1], (0, 255, 0), 2)

        if railway_track_position is not None and len(yellow_lines) > 0 and railway_to_left is None:
            yellow_x_positions = [line[0][0] for line in yellow_lines]
            avg_yellow_x = np.mean(yellow_x_positions)
            railway_to_left = railway_track_position < avg_yellow_x

        # Detect people using the person detection model
        person_results = person_model(frame)

        people_in_danger = 0
        if person_results and person_results[0] is not None:
            for *xyxy, conf, cls in person_results[0].boxes.data.tolist():
                if person_model.names[int(cls)] == 'Person':
                    bbox = list(map(int, xyxy))
                    foot_position = get_foot_position(bbox)

                    color = (0, 255, 0)

                    if railway_track_position is not None and len(yellow_lines) > 0 and railway_to_left is not None:
                        if railway_to_left and foot_position[0] < avg_yellow_x:
                            if red_annotation_active > 0:
                                color = (0, 0, 255)
                                people_in_danger += 1
                        elif foot_position[0] > avg_yellow_x:
                            if red_annotation_active > 0:
                                color = (0, 0, 255)
                                people_in_danger += 1

                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
                    cv2.circle(frame, foot_position, 5, color, -1)

        if red_annotation_active > 0:
            red_annotation_active -= 1

        flashing_step += 5
        add_transparent_rectangle(frame, width, height, people_in_danger, flashing_step)

        out.write(frame)
        clear_output(wait=True)

        frame_count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
