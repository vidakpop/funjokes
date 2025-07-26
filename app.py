import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import base64
from io import BytesIO

# App title and config
st.set_page_config(page_title="ASCII Video Magic", page_icon="🎬", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .title {
        font-size: 3.5em !important;
        color: #FF4B4B;
        text-align: center;
        text-shadow: 2px 2px 8px #FF4B4B;
        margin-bottom: 0.5em;
    }
    .subheader {
        color: #FFFFFF !important;
        text-align: center;
        margin-bottom: 2em;
    }
    .sidebar .sidebar-content {
        background-color: #1A1D24;
    }
    .stSlider > div > div > div > div {
        background: #FF4B4B;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5em 1em;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Hardcoded video (using a sample video or you can replace with your own)
def get_sample_video():
    # This is a placeholder - in a real app, you would use a real video file
    # For demo purposes, we'll generate a synthetic video
    video_frames = []
    for i in range(30):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.putText(img, f"Frame {i+1}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        video_frames.append(img)
    return video_frames

# ASCII conversion functions
def resize_image(image, new_width=100):
    (old_height, old_width) = image.shape[:2]
    aspect_ratio = old_width / old_height
    new_height = int(new_width / aspect_ratio)
    return cv2.resize(image, (new_width, new_height))

def pixel_to_ascii(pixel_value, ascii_chars):
    return ascii_chars[pixel_value * len(ascii_chars) // 256]

def frame_to_ascii(frame, ascii_chars="@%#*+=-:. "):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = resize_image(gray_frame)
    ascii_frame = ""
    for row in resized_frame:
        ascii_frame += "".join([pixel_to_ascii(pixel, ascii_chars) for pixel in row]) + "\n"
    return ascii_frame

# Main app
def main():
    # Title and header
    st.markdown('<h1 class="title">🎬 ASCII Video Magic</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="subheader">Transform videos into mesmerizing ASCII art</h3>', unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.header("Controls")
        width = st.slider("ASCII Width", 30, 150, 80, help="Number of ASCII characters per line")
        fps = st.slider("Playback Speed (FPS)", 1, 30, 10)
        ascii_chars = st.text_input("ASCII Characters", value="@%#*+=-:. ", 
                                   help="Character set from darkest to lightest")
        st.markdown("---")
        st.markdown("**About**")
        st.markdown("This app converts video frames to ASCII art in real-time.")
    
    # Video processing
    video_frames = get_sample_video()
    
    # Placeholders for display
    original_placeholder = st.empty()
    ascii_placeholder = st.empty()
    status_text = st.empty()
    
    # Play button
    if st.button("▶️ Play ASCII Conversion"):
        status_text.info("Processing video...")
        
        for i, frame in enumerate(video_frames):
            # Display original frame
            original_placeholder.image(frame, caption=f"Original Frame {i+1}", use_column_width=True)
            
            # Convert to ASCII
            ascii_art = frame_to_ascii(frame, ascii_chars)
            
            # Display ASCII art with monospace font
            ascii_placeholder.markdown(f"""
                <div style="
                    font-family: monospace;
                    white-space: pre;
                    line-height: 0.8;
                    font-size: 8px;
                    color: #FFFFFF;
                    background-color: #000000;
                    padding: 10px;
                    border-radius: 5px;
                    overflow: auto;
                    max-height: 500px;
                ">
                {ascii_art}
                </div>
            """, unsafe_allow_html=True)
            
            # Add some delay to control playback speed
            time.sleep(1/fps)
        
        status_text.success("Video processing complete!")

if __name__ == "__main__":
    main()