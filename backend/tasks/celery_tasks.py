from celery import Celery
import asyncio
import json
import redis
from backend.config import settings
from backend.agents.graph import graph_app

celery_app = Celery(
    "credit_risk_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

@celery_app.task(bind=True, max_retries=3)
def run_analysis(self, job_id: str, file_paths: list[str]):
    try:
        redis_client.set(f"job:{job_id}", json.dumps({"status": "PROCESSING", "current_node": "starting"}))
        
        async def run_graph():
            initial_state = {
                "job_id": job_id,
                "input_files": file_paths,
                "parsed_chunks": [],
                "extracted_statements": [],
                "computed_ratios": {},
                "risk_score": {},
                "qualitative_commentary": "",
                "risk_flags": [],
                "errors": [],
                "current_node": "starting"
            }
            config = {"configurable": {"thread_id": job_id}}
            
            # Since LangGraph updates state asynchronously, we can listen or just wait for finish
            # For simplicity, we just invoke it. To update node status in real-time,
            # we'd iterate over stream().
            async for event in graph_app.astream(initial_state, config=config):
                for node_name, node_state in event.items():
                    current_node = node_state.get("current_node", node_name)
                    redis_client.set(f"job:{job_id}", json.dumps({"status": "PROCESSING", "current_node": current_node}))
                    
            return await graph_app.ainvoke(None, config=config) # Get final state
            
        final_state = asyncio.run(run_graph())
        
        if not final_state.get("extracted_statements"):
            raise ValueError(f"Extraction failed: {final_state.get('errors')}")

        result_data = {
            "job_id": job_id,
            "status": "COMPLETE",
            "memo_url": f"/outputs/{job_id}_credit_memo.pdf",
            "extracted_statements": final_state.get("extracted_statements", []),
            "computed_ratios": final_state.get("computed_ratios", {}),
            "risk_score": final_state.get("risk_score", {}),
            "qualitative_commentary": final_state.get("qualitative_commentary", ""),
            "risk_flags": final_state.get("risk_flags", []),
            "confidence": final_state.get("confidence", 0.0)
        }
        
        redis_client.set(f"job:{job_id}", json.dumps({"status": "COMPLETE"}))
        redis_client.set(f"result:{job_id}", json.dumps(result_data))
        
    except Exception as e:
        error_msg = str(e)
        redis_client.set(f"job:{job_id}", json.dumps({"status": "FAILED", "error": error_msg}))
