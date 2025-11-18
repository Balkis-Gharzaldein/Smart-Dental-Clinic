import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def Segmantation_Model(image_path):
    model = load_model('C:/Users/HP/Downloads/dental_xray_seg_250.h5')

    # Load and preprocess the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image_resized = cv2.resize(image, (512, 512))
    image_normalized = image_resized / 255.0
    image_input = np.expand_dims(image_normalized, axis=[0, -1])

    # Predict using the model
    prediction = model.predict(image_input)
    prediction_binary = (prediction > 0.5).astype(np.uint8)

    # Save segmentation result
    segmentation_result_path = 'segmentation_result.png'
    cv2.imwrite(segmentation_result_path, prediction_binary[0, :, :, 0] * 255)

    # Draw contours on the image
    contours, _ = cv2.findContours(prediction_binary[0, :, :, 0], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_with_contours = cv2.cvtColor(image_resized, cv2.COLOR_GRAY2BGR)
    contour_color = (0, 0, 255)
    contour_thickness = 1
    cv2.drawContours(image_with_contours, contours, -1, contour_color, contour_thickness)
    
    # Save image with contours
    image_with_contours_path = 'image_with_contours.png'
    cv2.imwrite(image_with_contours_path, image_with_contours)

    # Colorize and save segmentation result
    image_color = cv2.imread(image_path)
    image_color_resized = cv2.resize(image_color, (512, 512))
    prediction_rgb = cv2.cvtColor(prediction_binary[0, :, :, 0] * 255, cv2.COLOR_GRAY2BGR)
    segmentation_result_colored = cv2.bitwise_and(image_color_resized, prediction_rgb)
    cv2.drawContours(segmentation_result_colored, contours, -1, contour_color, contour_thickness)
    
    segmentation_colored_result_with_contours_path = 'segmentation_colored_result_with_contours.png'
    cv2.imwrite(segmentation_colored_result_with_contours_path, segmentation_result_colored)

    return (image_with_contours_path, 
            segmentation_colored_result_with_contours_path, 
            segmentation_result_path)

