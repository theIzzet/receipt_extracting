import base64
from io import BytesIO
from PIL import Image
import imghdr

def image_to_base64(image_file):
    """
    Çeşitli resim formatlarını base64'e dönüştürür
    """
    try:
        # Önce resim türünü kontrol et
        image_data = image_file.read()
        
        # Resim türünü belirle
        image_format = imghdr.what(None, h=image_data)
        
        if image_format is None:
            # PIL ile tekrar deneyelim
            try:
                image = Image.open(BytesIO(image_data))
                image_format = image.format.lower()
            except:
                raise ValueError("Desteklenmeyen resim formatı")
        
        # Desteklenen formatları kontrol et
        supported_formats = ['jpeg', 'jpg', 'png', 'bmp', 'gif', 'tiff', 'webp']
        if image_format not in supported_formats:
            raise ValueError(f"Desteklenmeyen resim formatı: {image_format}")
        
        # Base64'e dönüştür
        base64_data = base64.b64encode(image_data).decode("utf-8")
        
        # MIME type'ı belirle
        mime_type = f"image/{image_format}"
        if image_format == 'jpg':
            mime_type = "image/jpeg"
        
        return f"data:{mime_type};base64,{base64_data}"
        
    except Exception as e:
        raise ValueError(f"Resim işleme hatası: {str(e)}")

def validate_image_format(file_content):
    """
    Resim formatını doğrular
    """
    supported_formats = ['jpeg', 'jpg', 'png', 'bmp', 'gif', 'tiff', 'webp']
    image_format = imghdr.what(None, h=file_content)
    
    if image_format and image_format.lower() in supported_formats:
        return True
    return False

def convert_image_format(image_file, target_format='png'):
    """
    Resmi desteklenen bir formata dönüştürür
    """
    try:
        image_data = image_file.read()
        image = Image.open(BytesIO(image_data))
        
        # RGBA formatına dönüştür (transparency sorunlarını çözmek için)
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        
        # Byte stream'e kaydet
        output = BytesIO()
        image.save(output, format=target_format.upper())
        output.seek(0)
        
        return output
    except Exception as e:
        raise ValueError(f"Resim dönüştürme hatası: {str(e)}")