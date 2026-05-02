from backend.agents.state import AgentState
from backend.agents.tools.pdf_parser import parse_pdf
from backend.agents.tools.image_parser import parse_image
from backend.agents.tools.csv_parser import parse_csv_excel
import os

def ingestion_node(state: AgentState) -> AgentState:
    files = state.get("input_files", [])
    chunks = []
    errors = []
    
    for file_path in files:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            file_chunks = parse_pdf(file_path)
            chunks.extend([c.model_dump() for c in file_chunks])
        elif ext in [".png", ".jpg", ".jpeg", ".webp"]:
            file_chunks = parse_image(file_path)
            chunks.extend([c.model_dump() for c in file_chunks])
        elif ext in [".csv", ".xlsx"]:
            file_chunks = parse_csv_excel(file_path)
            chunks.extend([c.model_dump() for c in file_chunks])
        else:
            errors.append(f"Unsupported file extension: {ext}")
            
    return {
        "parsed_chunks": chunks,
        "errors": errors,
        "current_node": "parsing documents"
    }
