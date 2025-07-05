from langgraph.graph import StateGraph, END
from state import GraphState

from nodes import (
    generate_user_story_tests,
    generate_spec_tests,
    merge_test_cases,
    add_traceability,
    refine_test_cases,
    route_step
)

def create_test_case_graph():
    """Create the LangGraph workflow for test case generation"""
    
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("generate_user_tests", generate_user_story_tests)
    workflow.add_node("generate_spec_tests", generate_spec_tests)
    workflow.add_node("merge_tests", merge_test_cases)
    workflow.add_node("add_traceability", add_traceability)
    workflow.add_node("refine_tests", refine_test_cases)
    
    # Add conditional start based on step
    workflow.add_conditional_edges(
        "__start__",
        route_step,
        {
            "generate": "generate_user_tests",
            "refine": "refine_tests"
        }
    )
    
    # Add edges for generation flow
    workflow.add_edge("generate_user_tests", "generate_spec_tests")
    workflow.add_edge("generate_spec_tests", "merge_tests")
    workflow.add_edge("merge_tests", "add_traceability")
    workflow.add_edge("add_traceability", END)
    
    # Add edge for refinement flow
    workflow.add_edge("refine_tests", END)
    
    # Compile the graph
    return workflow.compile()