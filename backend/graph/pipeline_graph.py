from langgraph.graph import END, START, StateGraph

from backend.graph.nodes import (
    run_step1,
    run_step2,
    run_step3,
    run_step4,
    run_step5,
    run_step6,
)
from backend.graph.state import PipelineGraphState


def build_pipeline_graph():
    # Initialize the graph with our TypedDict state
    builder = StateGraph(PipelineGraphState)
    
    # Add nodes
    builder.add_node("step1", run_step1)
    builder.add_node("step2", run_step2)
    builder.add_node("step3", run_step3)
    builder.add_node("step4", run_step4)
    builder.add_node("step5", run_step5)
    builder.add_node("step6", run_step6)
    
    # Define linear execution flow
    builder.add_edge(START, "step1")
    builder.add_edge("step1", "step2")
    builder.add_edge("step2", "step3")
    builder.add_edge("step3", "step4")
    builder.add_edge("step4", "step5")
    builder.add_edge("step5", "step6")
    builder.add_edge("step6", END)
    
    # Compile the graph
    graph = builder.compile()
    return graph

# Export a compiled singleton instance
pipeline_graph = build_pipeline_graph()
