import base64
from typing import List
from backend.models.financial import DocumentChunk
import io
from PIL import Image

def parse_image(file_path: str) -> List[DocumentChunk]:
    chunks = []
    try:
        with Image.open(file_path) as img:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Compress or resize if too large
            img.thumbnail((2000, 2000))
            
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            img_data = buffered.getvalue()
            b64_image = base64.b64encode(img_data).decode("utf-8")
            
            chunks.append(DocumentChunk(
                content=b64_image,
                source=file_path,
                chunk_type="image",
                page_num=1
            ))
    except Exception as e:
        print(f"Error parsing image {file_path}: {e}")
        
    return chunks
