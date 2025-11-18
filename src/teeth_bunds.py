import cv2
import numpy as np

def Dental_Bunds(image_path):
    # تحميل الصورة
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # استخلاص الإطار الأحمر (الحدود)
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([50, 50, 255])
    mask = cv2.inRange(image, lower_red, upper_red)

    # الحصول على الخطوط الخارجية للإطار الأحمر
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # تعريف معلمات نصف الدائرة للفك السفلي
    lower_center_x, lower_center_y = 256, 130  # موقع المركز للفك السفلي
    lower_radius = 300  # نصف القطر للفك السفلي
    lower_angle = 0  # زاوية الدوران للفك السفلي
    lower_start_angle = 50  # زاوية البداية للفك السفلي
    lower_end_angle = 130  # زاوية النهاية للفك السفلي

    # رسم نصف دائرة للفك السفلي على صورة فارغة
    lower_circle_img = np.zeros_like(gray)
    cv2.ellipse(lower_circle_img, (lower_center_x, lower_center_y), (lower_radius, lower_radius), 
                lower_angle, lower_start_angle, lower_end_angle, 255, thickness=2)

    # تحقق من وجود تقاطع بين نصف الدائرة السفلي والإطار الأحمر
    lower_intersection = cv2.bitwise_and(lower_circle_img, mask)

    # حساب عدد البكسلات المتقاطعة للفك السفلي
    lower_num_intersecting_pixels = cv2.countNonZero(lower_intersection)

    # تعريف معلمات نصف الدائرة للفك العلوي
    upper_center_x, upper_center_y = 256, -400  # موقع المركز للفك العلوي
    upper_radius = 500  # نصف القطر للفك العلوي
    upper_angle = 0  # زاوية الدوران للفك العلوي
    upper_start_angle = 70  # زاوية البداية للفك العلوي
    upper_end_angle = 110  # زاوية النهاية للفك العلوي

    # رسم نصف دائرة للفك العلوي على صورة فارغة
    upper_circle_img = np.zeros_like(gray)
    cv2.ellipse(upper_circle_img, (upper_center_x, upper_center_y), (upper_radius, upper_radius), 
                upper_angle, upper_start_angle, upper_end_angle, 255, thickness=2)

    # تحقق من وجود تقاطع بين نصف الدائرة العلوي والإطار الأحمر
    upper_intersection = cv2.bitwise_and(upper_circle_img, mask)

    # حساب عدد البكسلات المتقاطعة للفك العلوي
    upper_num_intersecting_pixels = cv2.countNonZero(upper_intersection)

    # بناء النتيجة النصية بناءً على عدد البكسلات المتقاطعة
    if lower_num_intersecting_pixels > 12 or upper_num_intersecting_pixels > 12:  # تعديل العتبة حسب الحاجة
        result_text = "There are bunds teeth"
    else:
        result_text = "There are no bunds teeth"

    # عرض الصورة مع نصف الدوائر والإطار الأحمر للتأكد
    cv2.drawContours(image, contours, -1, (0, 0, 255), 1)  # تغيير اللون إلى الأحمر
    cv2.ellipse(image, (lower_center_x, lower_center_y), (lower_radius, lower_radius), 
                lower_angle, lower_start_angle, lower_end_angle, (255, 255, 255), 2)
    cv2.ellipse(image, (upper_center_x, upper_center_y), (upper_radius, upper_radius), 
                upper_angle, upper_start_angle, upper_end_angle, (255, 255, 255), 2)

    return result_text