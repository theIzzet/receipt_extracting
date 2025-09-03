import os
import requests
import json
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def call_mistral_api(prompt, base64_image: str):
    # Base64 string'den MIME type'ı çıkar
    if base64_image.startswith('data:'):
        # data:image/png;base64,...
        mime_type = base64_image.split(';')[0].split(':')[1]
    else:
        mime_type = "image/jpeg"  # varsayılan
    
    message = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": base64_image}
                }
            ]
        }
    ]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-small-3.1-24b-instruct:free",
        "messages": message,
        "temperature": 0
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30  # Timeout süresi ekle
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"API hatası: {response.text}"
            )

        result = response.json()
        response_text = result['choices'][0]['message']['content']

        # JSON formatını temizle
        if '```json' in response_text:
            json_str = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            json_str = response_text.split('```')[1].strip()
        else:
            json_str = response_text.strip()

        return json.loads(json_str)
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="API çağrısı zaman aşımına uğradı")
    except requests.exceptions.RequestException as re:
        raise HTTPException(status_code=502, detail=f"Ağ hatası: {str(re)}")
    except json.JSONDecodeError as je:
        raise HTTPException(status_code=500, detail=f"JSON parse hatası: {str(je)}")