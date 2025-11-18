import cv2
import numpy as np
from imutils import perspective
from scipy.spatial import distance as dist

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def CCA_Analysis(orig_image, predict_image, erode_iteration, open_iteration):
    kernel1 = np.ones((5,5), dtype=np.float32)
    kernel_sharpening = np.array([[-1,-1,-1], 
                                  [-1,9,-1], 
                                 [-1,-1,-1]])
    image = predict_image
    image2 = orig_image    
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel1, iterations=open_iteration)
    image = cv2.filter2D(image, -1, kernel_sharpening)
    image = cv2.erode(image, kernel1, iterations=erode_iteration)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    labels = cv2.connectedComponents(thresh, connectivity=8)[1]
    unique_labels = np.unique(labels)
    count2 = 0

    for label in unique_labels:
        if label == 0:
            continue
        
        # Create a mask
        mask = np.zeros(thresh.shape, dtype="uint8")
        mask[labels == label] = 255

        # Find contours and determine contour area
        cnts, hieararch = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0]
        c_area = cv2.contourArea(cnts)
        
        # Threshold for tooth count
        if c_area > 2000:
            count2 += 1
        
        # Get the bounding box and midpoints
        rect = cv2.minAreaRect(cnts)
        box = cv2.boxPoints(rect)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        
        # Random color for the contour and text
        color1 = list(np.random.choice(range(150), size=3))  
        color = [int(color1[0]), int(color1[1]), int(color1[2])]  
        
        # Draw contours with reduced thickness
        cv2.drawContours(image2, [box.astype("int")], 0, color, 1)  # Reduced from 2 to 1

        # Calculate midpoints
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        # Draw midpoints with reduced size
        cv2.circle(image2, (int(tltrX), int(tltrY)), 3, (255, 0, 0), -1)  # Reduced from 5 to 3
        cv2.circle(image2, (int(blbrX), int(blbrY)), 3, (255, 0, 0), -1)
        cv2.circle(image2, (int(tlblX), int(tlblY)), 3, (255, 0, 0), -1)
        cv2.circle(image2, (int(trbrX), int(trbrY)), 3, (255, 0, 0), -1)

        # Draw connecting lines with reduced thickness
        cv2.line(image2, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), color, 1)  # Reduced from 2 to 1
        cv2.line(image2, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), color, 1)

        # Calculate distances
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        
        # Assuming pixelsPerMetric is 1, you can adjust as needed
        pixelsPerMetric = 1
        dimA = dA * pixelsPerMetric
        dimB = dB * pixelsPerMetric

        # Draw text with further reduced size and thickness
        font_scale = 0.2  # Further reduced from 0.4 to 0.2
        font_thickness = 1  # Thickness kept at 1
        
        cv2.putText(image2, "{:.1f}pixel".format(dimA), (int(tltrX - 15), int(tltrY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)
        cv2.putText(image2, "{:.1f}pixel".format(dimB), (int(trbrX + 10), int(trbrY)),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)
        cv2.putText(image2, "{:.1f}".format(label), (int(tltrX - 35), int(tltrY - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness)
    
    teeth_count = count2
    return image2, teeth_count