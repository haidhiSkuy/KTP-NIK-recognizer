import cv2
import numpy as np


def resize(image: np.ndarray, scale_factor: float = 0.6) -> np.ndarray:
    height = image.shape[0]
    width = image.shape[1]

    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)
    dimensions = (new_width, new_height)
    new_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_LINEAR)

    if len(new_image.shape) == 2:  # Just has one dimension
        new_image = cv2.cvtColor(new_image, cv2.COLOR_GRAY2BGR)

    return new_image
