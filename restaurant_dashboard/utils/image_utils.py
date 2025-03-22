# utils/image_utils.py
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

def resize_image(image, max_size=(800, 800), format='JPEG', quality=85):
    """
    Resize an image to a maximum size while maintaining aspect ratio
    """
    if not image:
        return None
    
    img = Image.open(image)
    
    # Convert to RGB if image is in RGBA mode
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # Get image format
    name, ext = os.path.splitext(image.name)
    if not ext:
        ext = '.jpg'
    
    # Calculate new dimensions
    img_width, img_height = img.size
    max_width, max_height = max_size
    
    # Only resize if image is larger than max dimensions
    if img_width > max_width or img_height > max_height:
        # Calculate ratio to maintain aspect ratio
        ratio = min(max_width / img_width, max_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Save resized image
    buffer = BytesIO()
    img.save(buffer, format=format, quality=quality)
    buffer.seek(0)
    
    # Create new ContentFile with resized image
    resized_image = ContentFile(buffer.read())
    resized_image.name = f"{name}{ext}"
    
    return resized_image