from langgraph.graph import StateGraph, END
from backend.agents.state import AgentState
from backend.agents.nodes.ingestion import ingestion_node
from backend.agents.nodes.extraction import extraction_node
from backend.agents.nodes.analysis import analysis_node
from backend.agents.nodes.scoring import scoring_node
from backend.agents.nodes.memo_gen import memo_gen_node
from langgraph.checkpoint.memory import MemorySaver

def should_continue(state: AgentState):
    statements = state.get("extracted_statements", [])
    if not statements:
        return "extraction_failed"
    return "analysis_node"

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("ingestion_node", ingestion_node)
    workflow.add_node("extraction_node", extraction_node)
    workflow.add_node("analysis_node", analysis_node)
    workflow.add_node("scoring_node", scoring_node)
    workflow.add_node("memo_gen_node", memo_gen_node)
    
    # Adding end state for failure
    workflow.add_node("extraction_failed", lambda state: {"current_node": "failed"})
    
    workflow.set_entry_point("ingestion_node")
    workflow.add_edge("ingestion_node", "extraction_node")
    workflow.add_conditional_edges(
        "extraction_node",
        should_continue,
        {
            "analysis_node": "analysis_node",
            "extraction_failed": "extraction_failed"
        }
    )
    
    workflow.add_edge("analysis_node", "scoring_node")
    workflow.add_edge("scoring_node", "memo_gen_node")
    workflow.add_edge("memo_gen_node", END)
    workflow.add_edge("extraction_failed", END)
    
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    return app

graph_app = build_graph()
