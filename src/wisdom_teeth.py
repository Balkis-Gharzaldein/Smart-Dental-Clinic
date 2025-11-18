import cv2
import numpy as np
import matplotlib.pyplot as plt

def Wisdom_Teeth(image_path, output_image_path):
    # Load the image using OpenCV
    image_cv = cv2.imread(image_path)

    # Convert the image to HSV for better color detection
    hsv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)

    # Define the red color range in HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Threshold the image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Get image dimensions and center
    height, width, _ = image_cv.shape
    center_x, center_y = width // 2, height // 2

    # Coordinates of wisdom teeth positions relative to the center
    wisdom_teeth_positions = {
        "Top Right": (center_x + 175, center_y - 130),
        "Top Left": (center_x - 172, center_y - 130),
        "Bottom Right": (center_x + 175, center_y + 10),
        "Bottom Left": (center_x - 175, center_y + 10),
    }

    # Define the region size for each wisdom tooth
    region_size = 50  # This defines how large the checking region is around each tooth

    # Function to check if a region contains any red pixels
    def check_red_pixels(region, mask):
        x, y = region
        x_start, y_start = int(x - region_size / 2), int(y - region_size / 2)
        x_end, y_end = int(x + region_size / 2), int(y + region_size / 2)
        
        # Ensure coordinates are within image bounds
        x_start, y_start = max(0, x_start), max(0, y_start)
        x_end, y_end = min(mask.shape[1], x_end), min(mask.shape[0], y_end)
        
        # Extract the region from the mask
        region_mask = mask[y_start:y_end, x_start:x_end]
        
        # Check if there are any non-zero pixels (i.e., red pixels)
        return np.any(region_mask > 0)

    # Check intersections for each wisdom tooth region
    intersections = {}
    for label, (x, y) in wisdom_teeth_positions.items():
        region = (x, y)
        intersecting = check_red_pixels(region, mask)
        intersections[label] = intersecting

    # Draw the results on the original image
    for label, (x, y) in wisdom_teeth_positions.items():
        color = (0, 255, 0) if intersections[label] else (0, 0, 255)
        cv2.circle(image_cv, (x, y), 10, color, -1)
        cv2.putText(image_cv, label, (x + 15, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Draw rectangle around each wisdom tooth position
        x_start, y_start = x - region_size // 2, y - region_size // 2
        cv2.rectangle(image_cv, (x_start, y_start), (x_start + region_size, y_start + region_size), color, 2)
        segmented_image_resized = cv2.resize(image_cv, (1024, 512))

    # Save the final image with the annotations
    cv2.imwrite(output_image_path, segmented_image_resized)

