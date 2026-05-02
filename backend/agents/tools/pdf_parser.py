import fitz  # PyMuPDF
import base64
from typing import List
from backend.models.financial import DocumentChunk

def parse_pdf(file_path: str) -> List[DocumentChunk]:
    chunks = []
    try:
        doc = fitz.open(file_path)
        for i, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                chunks.append(DocumentChunk(
                    content=text,
                    source=file_path,
                    chunk_type="text",
                    page_num=i + 1
                ))
            
            # Extract images or tables as images if text is minimal (simple approach)
            # For complex extraction, we can render the whole page as an image to be safe
            pix = page.get_pixmap()
            img_data = pix.tobytes("jpeg")
            b64_image = base64.b64encode(img_data).decode("utf-8")
            chunks.append(DocumentChunk(
                content=b64_image,
                source=file_path,
                chunk_type="image",
                page_num=i + 1
            ))
            
    except Exception as e:
        print(f"Error parsing PDF {file_path}: {e}")
        
    return chunks
