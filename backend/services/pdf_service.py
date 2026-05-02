import os
from weasyprint import HTML
from backend.config import settings

class PDFService:
    def render_html_to_pdf(self, html_content: str, job_id: str) -> str:
        output_filename = f"{job_id}_credit_memo.pdf"
        output_path = os.path.join(settings.OUTPUT_DIR, output_filename)
        
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path

pdf_service = PDFService()
