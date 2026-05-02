from backend.agents.nodes.extraction import extraction_node

def test_extraction_no_statements(monkeypatch):
    # If the LLM throws or fails, we should gracefully return empty
    def mock_extract(*args, **kwargs):
        return "invalid json"
        
    monkeypatch.setattr("backend.services.llm_service.llm_service.generate_text", mock_extract)
    state = {
        "parsed_chunks": [{"content": "some text", "chunk_type": "text", "source": "a", "page_num": 1}]
    }
    result = extraction_node(state)
    assert result["extracted_statements"] == []
    assert len(result["errors"]) > 0
