import streamlit as st
import cv2
import numpy as np
import time

# App title and config
st.set_page_config(page_title="Thuno Happiness", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #000000;
    }
    .title {
        font-size: 4em !important;
        color: #FFD700;
        text-align: center;
        margin-bottom: 0.2em;
        font-family: 'Impact', sans-serif;
        text-shadow: 3px 3px 0px #FF4500;
    }
    .quote {
        font-size: 1.8em !important;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 0.5em;
        font-style: italic;
        font-family: 'Georgia', serif;
    }
    .ascii-container {
        font-family: 'Courier New', monospace;
        white-space: pre;
        line-height: 0.7;
        font-size: 6px;
        color: #FFFFFF;
        background-color: #000000;
        padding: 5px;
        overflow: hidden;
        text-align: center;
        margin: 0 auto;
        width: 100%;
        height: 80vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .footer {
        color: #888888;
        text-align: center;
        margin-top: 1em;
        font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)

# ASCII conversion functions
def resize_image(image, new_width=150):  # Increased width for more detail
    (old_height, old_width) = image.shape[:2]
    aspect_ratio = old_width / old_height
    new_height = int(new_width / aspect_ratio)
    return cv2.resize(image, (new_width, new_height))

def pixel_to_ascii(pixel_value, ascii_chars):
    pixel_value = min(255, max(0, int(pixel_value)))
    return ascii_chars[pixel_value * len(ascii_chars) // 256]

def frame_to_ascii(frame, ascii_chars="@%#*+=-:. "):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = resize_image(gray_frame)
    ascii_frame = ""
    for row in resized_frame:
        ascii_frame += "".join([pixel_to_ascii(pixel, ascii_chars) for pixel in row]) + "\n"
    return ascii_frame

def get_sample_video():
    video_path = "fun.webm"
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

# Main app
def main():
    # Title and quote
    st.markdown('<h1 class="title">THUNO HAPPINESS</h1>', unsafe_allow_html=True)
    st.markdown('<div class="quote">"A Thuno a day keeps the doctor away"</div>', unsafe_allow_html=True)
    
    # ASCII display container
    ascii_placeholder = st.empty()
    
    # Get video frames
    video_frames = get_sample_video()
    
    # Auto-play the ASCII conversion in a loop
    while True:
        for frame in video_frames:
            # Convert to ASCII
            ascii_art = frame_to_ascii(frame)
            
            # Display ASCII art
            ascii_placeholder.markdown(f"""
                <div class="ascii-container">
                {ascii_art}
                </div>
            """, unsafe_allow_html=True)
            
            # Control playback speed
            time.sleep(0.05)  # Faster playback for smoother animation
        
        # Footer
        st.markdown('<div class="footer">Press R to restart | © CYBERJIUTSU SYSTEMS</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()