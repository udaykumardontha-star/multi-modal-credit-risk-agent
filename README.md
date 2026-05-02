# Multi-Modal Credit Risk Analyst Agent

Upload a company's financial documents (PDF, scanned images, or CSV) and the system automatically extracts financials, runs ratio analysis, and outputs a credit memo with an approval decision — no manual steps.

Tested on mock data — sample output below.

| Company | Score | Decision |
|---|---|---|
| Rajesh Industries | 74/100 | Approved |
| Priya Textiles | 58/100 | Refer to analyst |
| Suresh Pharma | 41/100 | Rejected |

Sample credit memo: [sample_output/sample_credit_memo.pdf](sample_output/sample_credit_memo.pdf)

---

## How it works

```text
Upload Files → Ingestion → Extraction (GPT-4o Vision) → Ratio Analysis → Risk Scoring → Credit Memo PDF
```

## Features

- Accepts PDFs, scanned balance sheet images, and CSV files in a single upload
- Extracts financial figures using GPT-4o vision — works even on scanned documents
- Computes 12 financial ratios including Altman Z-Score
- Outputs APPROVE / REFER / REJECT with a weighted composite score
- Generates a professional credit memo PDF with analyst commentary
- Fully async — built on Celery + Redis so multiple documents process in parallel

## Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI |
| Agent Orchestration | LangGraph, LangChain |
| LLM | OpenAI GPT-4o / Google Gemini |
| Task Queue | Celery, Redis |
| PDF Generation | WeasyPrint, Jinja2 |
| Frontend | React (Vite), TypeScript, Tailwind CSS |

## Quickstart

1. Clone the repo
2. Copy and configure environment variables:
```bash
cp .env.example .env
# Add your OPENAI_API_KEY
```
3. Run with Docker:
```bash
docker compose up --build
```
4. Open the app:
   - Frontend: `http://localhost:5173`
   - API docs: `http://localhost:8000/docs`

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/analyze` | Upload financial documents |
| `GET` | `/api/v1/results/{job_id}` | Poll job status and get results |
| `GET` | `/health` | Health check |

## Risk Scoring

Composite score (0-100) calculated from 12 ratios:

- Altman Z-Score — 25% weight (below 1.81 auto-rejects)
- Interest Coverage — 20%
- Debt-to-Equity — 15%
- Current Ratio — 15%
- EBITDA Margin — 10%
- Net Margin — 10%
- ROA — 5%

Thresholds: 70+ → Approve, 45-69 → Refer, below 45 → Reject

## Testing

```bash
cd backend
pip install -r requirements.txt
pytest tests/
```

## License

MIT