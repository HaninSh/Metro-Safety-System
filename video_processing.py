import cv2
import numpy as np
import gdown
import subprocess
import sys

def download_video(url, save_path):
    try:
        if 'drive.google.com' in url:
            file_id = url.split('/d/')[1].split('/')[0]
            download_url = f'https://drive.google.com/uc?id={file_id}'
        else:
            download_url = url

        gdown.download(download_url, save_path, quiet=False)
        print("Download successful!")
        return True
    except Exception as e:
        print(f"Error downloading video: {e}")
        return False

def detect_yellow_line_in_stopbraille_blocks(frame, xmin, ymin, xmax, ymax):
    roi = frame[ymin:ymax, xmin:xmax]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([0, 60, 100])
    upper_yellow = np.array([40, 255, 255])
    mask = cv2.inRange(hsv_roi, lower_yellow, upper_yellow)
    lines = cv2.HoughLinesP(mask, 1, np.pi / 180, threshold=50, minLineLength=100, maxLineGap=10)

    detected_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            x1 += xmin
            y1 += ymin
            x2 += xmin
            y2 += ymin
            detected_lines.append([(x1, y1), (x2, y2)])

    return detected_lines

def get_foot_position(bbox):
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int(y2)

def add_transparent_rectangle(frame, width, height, people_in_danger, flashing_step):
    rect_x1 = width - 220
    rect_y1 = 10
    rect_x2 = width - 10
    rect_y2 = 100
    overlay = frame.copy()
    if people_in_danger == 0:
        overlay_color = (0, 255, 0, 100)
    else:
        red_intensity = 100 + int(155 * np.sin(flashing_step / 10.0))
        overlay_color = (0, 0, red_intensity, 100)

    cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), overlay_color[:3], -1)
    alpha = overlay_color[3] / 255.0
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    text = f"Danger: {people_in_danger}"
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
    text_x = rect_x1 + (rect_x2 - rect_x1 - text_size[0]) // 2
    text_y = rect_y1 + (rect_y2 - rect_y1 + text_size[1]) // 2
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)


def install_requirements(file_path):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file_path])

def download_models():
    subprocess.run(["sed", "-i", "s/\r$//", "download_models.sh"])
    # Run the bash script
    subprocess.run(["bash", "download_models.sh"])