# import cv2
# from Restoration import detect_restoration


# def main(imagePath):
#     # Load the image
#     image = cv2.imread(imagePath)

#     # Detect restorations
#     detect_restoration(image)


# if __name__ == "__main__":
#     image_path = 'C:/Users/HP/Desktop/SDC/real x-ray/Screenshot 2024-08-14 115557.png'
#     main(image_path)

import cv2
from image_analysis import analysis  
from caries import highlight_caries_on_base_image
from restorations import highlight_restorations_on_base_image  
from model import Segmantation_Model
from teeth_bunds import Dental_Bunds
from teeth_section import Teeth_Section_with_Rectangles

def main(image_path):
    Segmantation_Model(image_path)
    while True:
        print("\nChoose an option:")
        print("1 - Detect Caries")
        print("2 - Detect Restorations")
        print("3 - Image Analysis")
        print("4 - Dental_Bunds")
        print("5 - Teeth Section with Rectangles")
        
        print("6 - Exit")

        choice = input("Enter the number of your choice: ")

        if choice == "1":
            output_image_path = 'highlighted_caries_image.png'  
            highlight_caries_on_base_image('C:/AI_Dental/image_with_contours.png', output_image_path) 
        elif choice == "2":
            output_image_path = 'highlighted_restorations_image.png' 
            highlight_restorations_on_base_image('C:/AI_Dental/image_with_contours.png', output_image_path)
        elif choice == "3":
            analysis()  
        elif choice == "4":
            Dental_Bunds()
        elif choice == "5":
            Teeth_Section_with_Rectangles(image_path)
        elif choice == "6":
            print("Exiting the program.")
            break  
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    image_path = 'C:/Users/HP/Downloads/30.png'
    main(image_path)