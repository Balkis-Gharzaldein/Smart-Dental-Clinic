import cv2
import numpy as np

def highlight_caries_on_base_image(segmented_image_path, output_image_path):
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

    # Convert the HEX color for caries to RGB
    caries_color = np.array([30, 30, 30])  # RGB equivalent of HEX #585858

    # Set a narrow threshold range around the caries color
    lower_caries_threshold = caries_color - 8
    upper_caries_threshold = caries_color + 8

    # Loop through each contour (representing a tooth) and highlight caries
    for contour in contours:
        # Create a mask for the current tooth
        mask = np.zeros_like(red_mask)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        # Extract the tooth using the mask
        tooth_image = cv2.bitwise_and(segmented_image, segmented_image, mask=mask)

        # Crop the tooth image to the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        tooth_image_cropped = tooth_image[y:y+h, x:x+w]

        # Apply the caries detection based on the RGB threshold
        caries_mask = cv2.inRange(tooth_image_cropped, lower_caries_threshold, upper_caries_threshold)

        # Find contours of the detected caries areas
        caries_contours, _ = cv2.findContours(caries_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the edges of the caries areas in blue on the original image
        for caries_contour in caries_contours:
            cv2.drawContours(segmented_image[y:y+h, x:x+w], [caries_contour], -1, (0, 0, 255), thickness=1)

    segmented_image_resized = cv2.resize(segmented_image, (1024, 512))

    # Save the final image with highlighted caries
    cv2.imwrite(output_image_path, segmented_image_resized)

    print(f'Saved the final image with caries highlighted at {output_image_path}')

