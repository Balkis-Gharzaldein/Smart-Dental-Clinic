from .image_analysis import analysis  
from .caries import highlight_caries_on_base_image
from .restorations import highlight_restorations_on_base_image  
from .model import Segmantation_Model
from .teeth_bunds import Dental_Bunds
from .teeth_section import Teeth_Section_with_Rectangles

def main(image_path, choice):
    # Run the segmentation model first
    Segmantation_Model(image_path)
    
    # Process based on the choice
    if choice == "CARIES":
        output_image_path = 'highlighted_caries_image.png'  
        highlight_caries_on_base_image('C:/AI_Dental/image_with_contours.png', output_image_path)
    elif choice == "RESTORITIONS":
        output_image_path = 'highlighted_restorations_image.png'
        highlight_restorations_on_base_image('C:/AI_Dental/image_with_contours.png', output_image_path)
    elif choice == "IMAGE_ANALYSIS":
        analysis()  
    elif choice == "TEETH_BUNDS":
        Dental_Bunds()
    elif choice == "TEETH_SECTION":
        Teeth_Section_with_Rectangles(image_path)
    else:
        raise ValueError("Invalid choice")
    
    # Return the paths or results (adjust based on your logic)
    output_paths = {
        'image_with_contours': 'path/to/image_with_contours.png',
        'segmentation_colored_result_with_contours': 'path/to/segmentation_colored_result_with_contours.png',
        'segmentation_result': 'path/to/segmentation_result.png',
    }
    return output_paths

def model_analysis(image_path):
    return Segmantation_Model(image_path)
