# Architecture Document: Multi-Modal Credit Risk Analyst Agent

## Why LangGraph?
We chose LangGraph over a simple sequential execution pipeline for several key reasons:
1. **State Management**: LangGraph provides robust persistence and management of the `AgentState` automatically across the entire DAG.
2. **Conditional Routing**: It allows us to naturally build logic like "if extraction fails, route to an error state instead of attempting analysis."
3. **Resilience & Resumability**: By using `MemorySaver` (or an external checkpointer like Postgres), we can resume the workflow if it crashes midway, preventing the need to re-run expensive LLM extractions.
4. **Tool/Agent Extensibility**: The graph structure makes it trivial to add "human-in-the-loop" approval nodes or additional AI verification steps in the future without major refactoring.

## Node Responsibilities & Failure Modes
1. **Ingestion Node**: Reads files based on extension, parses them into chunks.
   *Failure Modes*: Corrupted files, unsupported extensions. These are handled gracefully by returning parsing errors.
2. **Extraction Node**: Calls the multimodal LLM (GPT-4o or Gemini 1.5 Pro) to convert chunks into structured JSON `FinancialStatement`.
   *Failure Modes*: LLM returns invalid JSON or hallucinates. Handled via Pydantic parsing with `try/except` and fallbacks.
3. **Analysis Node**: Uses deterministic python functions (`ratio_engine.py`) to compute 12 key financial ratios, then uses an LLM to generate qualitative commentary based on the computed ratios.
   *Failure Modes*: Division by zero or missing required fields. Handled by allowing `None` values and flagging them.
4. **Scoring Node**: Deterministically calculates a composite risk score (0-100) using weighted ratios and triggers APPROVE/REFER/REJECT decisions. Includes Altman Z-Score override.
   *Failure Modes*: Insufficient data to score confidently.
5. **Memo Generation Node**: Uses Jinja2 and WeasyPrint to create a styled PDF report.
   *Failure Modes*: HTML/CSS rendering errors or file system permission issues.

## Multimodal Extraction
The system ingests data via three paths:
- **PDFs**: Parsed via PyMuPDF. Text is extracted directly, and table structures are maintained as well as possible. Pages with complex imagery or unparseable tables can be fallback-rendered to images.
- **Images (Scanned documents)**: Parsed via PIL, base64 encoded, and passed to a vision model (like `gpt-4o` or Gemini Vision) with strict instructions to output JSON.
- **CSV/Excel**: Parsed via pandas. Converted into text/markdown representations for standard LLM extraction.

## Scoring Model Design
The scoring model mimics a traditional lending institution's scorecard:
- **Industry Benchmarks**: Uses NBFC/lending sector defaults.
- **Weights**: The 5-factor Altman Z-Score has the highest weight (25%) as it's the strongest predictor of bankruptcy. Solvency and Leverage (Interest Coverage, Debt to Equity) make up the next largest chunk.
- **Overrides**: An Altman Z-Score below 1.81 indicates severe distress, and automatically overrides the composite score to trigger a `REJECT`.

## LLM Provider Interchangeability
The system abstracts the LLM calls into an `LLMService`. You can seamlessly swap between OpenAI and Gemini by setting `MODEL_PROVIDER=openai` or `MODEL_PROVIDER=gemini` in your `.env` file, without touching the core code. The underlying structure utilizes LangChain's generic BaseChatModel interfaces to normalize the inputs and outputs.

## Scalability
To scale to thousands of concurrent documents:
1. **Queue**: Replace Redis with AWS SQS or RabbitMQ for the Celery broker.
2. **Storage**: Replace local file storage with AWS S3 or GCP Cloud Storage. Update `storage_service.py`.
3. **State Checkpointing**: Change LangGraph's `MemorySaver()` to a Postgres-backed checkpointer.
4. **Workers**: Horizontally scale the Celery workers.
