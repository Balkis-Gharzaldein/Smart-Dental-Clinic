import cv2
import numpy as np
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def highlight_restorations_on_base_image(segmented_image_path, output_image_path):
    # Load the segmented image
    segmented_image = cv2.imread(segmented_image_path)

    # Convert the image to HSV for easier color-based masking
    hsv_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2HSV)

    # Define the color range for the red contour (in HSV space)
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    # Create a mask for the red contour
    red_mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    red_mask = cv2.add(red_mask1, red_mask2)

    # Find contours in the red mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through each contour (representing a tooth) and highlight restorations
    for contour in contours:
        # Create a mask for the current tooth
        mask = np.zeros_like(red_mask)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        # Extract the tooth using the mask
        tooth_image = cv2.bitwise_and(segmented_image, segmented_image, mask=mask)

        # Crop the tooth image to the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        tooth_image_cropped = tooth_image[y:y+h, x:x+w]

        # Convert the tooth image to grayscale to find the whitest area
        gray_tooth_image = cv2.cvtColor(tooth_image_cropped, cv2.COLOR_BGR2GRAY)

        # Threshold the grayscale image to find the brightest spots (likely restorations)
        _, thresh = cv2.threshold(gray_tooth_image, 250, 255, cv2.THRESH_BINARY)

        # Find contours of the bright spots
        bright_contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the edges of the whitest areas (restorations) in blue on the original image
        for bright_contour in bright_contours:
            cv2.drawContours(segmented_image[y:y+h, x:x+w], [bright_contour], -1, (255, 0, 0), thickness=2)

    segmented_image_resized = cv2.resize(segmented_image, (1024, 512))
    # Save the final image with highlighted restorations
    cv2.imwrite(output_image_path, segmented_image_resized)

    print(f'Saved the final image with restorations highlighted at {output_image_path}')


