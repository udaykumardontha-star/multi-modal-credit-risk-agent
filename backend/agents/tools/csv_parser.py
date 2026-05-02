import pandas as pd
from typing import List
from backend.models.financial import DocumentChunk

def parse_csv_excel(file_path: str) -> List[DocumentChunk]:
    chunks = []
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        csv_content = df.to_csv(index=False)
        chunks.append(DocumentChunk(
            content=csv_content,
            source=file_path,
            chunk_type="table",
            page_num=1
        ))
    except Exception as e:
        print(f"Error parsing table {file_path}: {e}")
        
    return chunks
