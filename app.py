import cv2
import numpy as np
import os
from time import sleep

def resize_image(image, new_width=100):
    (old_height, old_width) = image.shape[:2]
    aspect_ratio = old_width /old_height
    new_height = int(new_width / aspect_ratio)
    return cv2.resize