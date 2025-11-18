import cv2
import os
from .cca_analysis import CCA_Analysis

def Teeth_Section_with_Rectangles(image_path1, image_path2,output_path):
    img = cv2.imread(image_path1) 
    img1 = cv2.resize(img, (1024, 512))
    predicted = cv2.imread(image_path2)
    predicted = cv2.resize(predicted, (img1.shape[1], img1.shape[0]), interpolation=cv2.INTER_LANCZOS4)

    cca_result, teeth_count = CCA_Analysis(img1, predicted, 3, 2)

    result_path = output_path
    cv2.imwrite(result_path, cca_result)

    # إعادة المسار إلى الصورة المحفوظة
    return result_path

    # عرض النتيجة باستخدام cv2.imshow

