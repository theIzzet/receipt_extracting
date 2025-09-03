from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from utils.image_utils import image_to_base64, validate_image_format, convert_image_format
from prompts.receipt_prompt import PROMPT_TEMPLATE
from services.llm_service import call_mistral_api
import io

router = APIRouter()

@router.post("/upload")
async def upload_receipt(file: UploadFile = File(...)):
    try:
        # Dosya türünü kontrol et
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Sadece resim dosyaları yüklenebilir")
        
        # Dosya içeriğini oku
        file_content = await file.read()
        
        # Geri sarma (seek) için BytesIO'ya al
        file.file = io.BytesIO(file_content)
        
        # Resim formatını doğrula
        if not validate_image_format(file_content):
            
            try:
                converted_file = convert_image_format(io.BytesIO(file_content))
                file.file = converted_file
            except Exception as conv_error:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Desteklenmeyen resim formatı. Hata: {str(conv_error)}"
                )
        
        # Base64'e dönüştürme işlemi
        base64_image = image_to_base64(file.file)
        
        # LLM API'sini çağırıyoruz
        data = call_mistral_api(PROMPT_TEMPLATE, base64_image)
        
        return JSONResponse(content=data)
        
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")