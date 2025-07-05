from typing import TypedDict, List

class GraphState(TypedDict):
    """State of the test case generation graph"""
    user_stories: str
    specifications: str
    user_story_tests: List[str]
    spec_tests: List[str]
    merged_tests: str
    final_tests: str
    user_request: str
    step: str  # "generate" or "refine"