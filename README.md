# Multi-Modal Credit Risk Analyst Agent

An agentic system that accepts uploaded financial documents, automatically extracts structured financial data using a vision LLM, performs ratio analysis and risk scoring, and generates a formatted credit memo PDF.

## Architecture

```text
Upload Files -> Ingestion -> Extraction (LLM) -> Analysis & Ratios -> Scoring -> Memo Generation (PDF) -> Result!
```

## Features
- **Multi-Modal Support**: Analyzes PDFs, images (PNG, JPG, WEBP), and CSV/Excel files.
- **Zero Human-in-the-loop**: Fully automated processing from ingestion to decision.
- **Advanced Ratio Analysis**: Automatically calculates 12 key financial ratios including the Altman Z-Score.
- **Weighted Risk Scoring**: Scorecard-based decision rules (APPROVE / REFER / REJECT).
- **Credit Memo Generation**: Generates a professional PDF document with key figures, ratios, and LLM-generated analyst commentary.
- **Asynchronous Processing**: Non-blocking API using Celery and Redis.

## Tech Stack
| Component | Technology |
| --- | --- |
| **Backend Framework** | FastAPI |
| **Agent Orchestration** | LangGraph, LangChain |
| **LLM Provider** | OpenAI (GPT-4o) / Google Gemini |
| **Task Queue** | Celery, Redis |
| **PDF Generation** | WeasyPrint, Jinja2 |
| **Frontend Framework** | React (Vite), TypeScript |
| **Styling** | Tailwind CSS |

## Quickstart

1. **Clone the repository** (or download files)
2. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```
3. **Run with Docker Compose**:
   ```bash
   docker compose up --build
   ```
4. **Access the Application**:
   - Frontend: `http://localhost:5173`
   - Backend API Docs: `http://localhost:8000/docs`

## API Reference
| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/v1/analyze` | Upload financial documents (multipart/form-data) |
| `GET` | `/api/v1/results/{job_id}` | Poll job status and retrieve final results |
| `GET` | `/health` | Health check |

## How Risk Scoring Works
The system calculates a composite score (0-100) using 12 ratios with weights biased toward solvency and leverage:
- **Altman Z-Score**: 25% (Scores < 1.81 auto-reject)
- **Interest Coverage**: 20%
- **Debt-to-Equity**: 15%
- **Current Ratio**: 15%
- **EBITDA Margin**: 10%
- **Net Margin**: 10%
- **ROA**: 5%

**Decision Thresholds:**
- `>= 70`: APPROVE
- `45 - 69`: REFER
- `< 45`: REJECT

## Testing

```bash
cd backend
pip install -r requirements.txt
pytest tests/
```

## License
MIT
