def run_pipeline(question: str):
    # Monday: mock output so frontend/backend connect
    return {
        "planner_route": "research",
        "retrieved_chunks": [
            {"text": "This is placeholder financial text about interest rates and inflation.",
             "source": "placeholder.pdf", "page": 1}
        ],
        "draft_answer": "Draft: interest rates tend to ...",
        "final_answer": "Final: higher rates typically increase mortgage costs..."
    }