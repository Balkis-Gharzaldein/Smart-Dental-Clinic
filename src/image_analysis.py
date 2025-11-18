import cv2
import numpy as np

def analyze_bone_absorption(image_path, lower_threshold=50, upper_threshold=75, roi_upper=None, roi_lower=None):
    # تحميل الصورة
    image = cv2.imread(image_path)
    
    # تحويل الصورة إلى تدرجات رمادية
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    results = {}
    
    # معالجة المنطقة العليا (الفك العلوي)
    if roi_upper:
        x, y, w, h = roi_upper
        roi_upper_gray_image = gray_image[y:y+h, x:x+w]
        
        # تحسين التباين
        equalized_upper_image = cv2.equalizeHist(roi_upper_gray_image)
        
        # تطبيق العتبة اللونية باستخدام نطاق محدد
        threshold_upper_image = cv2.inRange(equalized_upper_image, lower_threshold, upper_threshold)
        
        # حساب عدد البكسلات فوق العتبة
        absorption_upper_pixels = cv2.countNonZero(threshold_upper_image)
        total_upper_pixels = roi_upper_gray_image.size
        absorption_upper_level = absorption_upper_pixels / total_upper_pixels
        
        results['upper'] = {
            'absorption_level': absorption_upper_level,
            'threshold_image': threshold_upper_image,
            'roi_gray_image': roi_upper_gray_image
        }
    
    # معالجة المنطقة السفلى (الفك السفلي)
    if roi_lower:
        x, y, w, h = roi_lower
        roi_lower_gray_image = gray_image[y:y+h, x:x+w]
        
        # تحسين التباين
        equalized_lower_image = cv2.equalizeHist(roi_lower_gray_image)
        
        # تطبيق العتبة اللونية باستخدام نطاق محدد
        threshold_lower_image = cv2.inRange(equalized_lower_image, lower_threshold, upper_threshold)
        
        # حساب عدد البكسلات فوق العتبة
        absorption_lower_pixels = cv2.countNonZero(threshold_lower_image)
        total_lower_pixels = roi_lower_gray_image.size
        absorption_lower_level = absorption_lower_pixels / total_lower_pixels
        
        results['lower'] = {
            'absorption_level': absorption_lower_level,
            'threshold_image': threshold_lower_image,
            'roi_gray_image': roi_lower_gray_image
        }
    
    return results

def analysis(image_path):
    lower_threshold = 100  
    upper_threshold = 110  
    
    # تحديد منطقتي الاهتمام (الفك العلوي والفك السفلي)
    roi_upper = (30, 60, 610, 75)  # (x, y, width, height) لمنطقة الفك العلوي
    roi_lower = (30, 360, 610, 60)  # (x, y, width, height) لمنطقة الفك السفلي
    
    results = analyze_bone_absorption(image_path, lower_threshold, upper_threshold, roi_upper, roi_lower)
    
    # بناء النص لاحتواء النتائج
    analysis_result = ""

    if 'upper' in results:
        upper_result = f'Upper Jaw Absorption Level: {results["upper"]["absorption_level"]:.2%}\n'
        analysis_result += upper_result
    
    if 'lower' in results:
        lower_result = f'Lower Jaw Absorption Level: {results["lower"]["absorption_level"]:.2%}\n'
        analysis_result += lower_result
    
    return analysis_result