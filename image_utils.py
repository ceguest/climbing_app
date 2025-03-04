from PIL import Image as IM
import cv2

def open_image_and_size(image_path, width, height):
    img = IM.open(image_path)
    img_res = img.resize((int(width), int(height)))
    return img_res

def convert_cv2_to_pil(img):
    # Rearrange the color channel
    b, g, r = cv2.split(img)
    img = cv2.merge((r, g, b))

    # Convert the cv2 Image object into a tk Image object
    im = IM.fromarray(img)
    return im