import cv2
import numpy as np
import os
from time import sleep

def resize_image(image, new_width=100):
    (old_height, old_width) = image.shape[:2]
    aspect_ratio = old_width /old_height
    new_height = int(new_width / aspect_ratio)
    return cv2.resize

def pixel_to_ascii(pixel_value,ascii_chars):
    return ascii_chars[pixel_value * len(ascii_chars) //256 ]


def frame_to_ascii(frame, ascii_chars="@%#*+=-:. "):
    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Resize the frame
    resized_frame = resize_image(gray_frame)
    
    # Convert each pixel to ASCII
    ascii_frame = ""
    for row in resized_frame:
        ascii_frame += "".join([pixel_to_ascii(pixel, ascii_chars) for pixel in row]) + "\n"
    
    return ascii_frame

def video_to_ascii(video_path, output_width=100, fps=10):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    # Get video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1 / fps
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert frame to ASCII
            ascii_frame = frame_to_ascii(frame)
            
            # Clear screen between frames (works best in terminal)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Print the ASCII frame
            print(ascii_frame)
            
            # Control playback speed
            sleep(frame_delay)
    
    except KeyboardInterrupt:
        print("\nASCII video playback stopped.")
    finally:
        cap.release()

if __name__ == "__main__":