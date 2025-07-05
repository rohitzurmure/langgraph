from langchain_groq import ChatGroq
from state import GraphState
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
st.sidebar.header("🔐 API Configuration")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password", value=st.session_state.get("api_key", ""))

if not api_key:
    st.warning("Please enter your API Key to proceed.")
    st.stop()

# Try initializing the LLM and catch if the API key is invalid
llm = None
try:
    llm = ChatGroq(
        api_key=api_key,
        model="llama3-8b-8192",
        temperature=0.2,
        max_tokens=6000,
        request_timeout=60.0
    )

    # Make a small test call to validate the API
    test_response = llm.invoke("Say Hello")
    if not test_response or "error" in str(test_response).lower():
        raise ValueError("Invalid response from API")

    st.success("Initialized Groq LLaMA3 Model.")

except Exception as e:
    st.error("Invalid API Key or error during model initialization. Please try again.")
    st.session_state["api_key"] = ""  # Clear stored key
    st.stop()


def generate_user_story_tests(state: GraphState) -> GraphState:
    """Generate test cases from user stories"""
    prompt = f"""
    You are a meticulous QA engineer with a knack for identifying all possible scenarios and edge cases.
    
    Generate detailed test cases based on the following user stories:
    
    {state["user_stories"]}
    
    Provide a comprehensive list of clear, structured test cases in a markdown table format, 
    covering all scenarios mentioned in the user stories.
    """
    
    response = llm.invoke(prompt)
    state["user_story_tests"] = [response.content]
    return state

def generate_spec_tests(state: GraphState) -> GraphState:
    """Generate test cases from specifications"""
    prompt = f"""
    You are a meticulous QA engineer with a knack for identifying all possible scenarios and edge cases.
    
    Generate detailed test cases based on the following technical specifications:
    
    {state["specifications"]}
    
    Provide a comprehensive list of clear, structured test cases in a markdown table format, 
    covering all scenarios mentioned in the specifications.
    """
    
    response = llm.invoke(prompt)
    state["spec_tests"] = [response.content]
    return state

def merge_test_cases(state: GraphState) -> GraphState:
    """Merge and deduplicate test cases"""
    user_tests = "\n".join(state["user_story_tests"])
    spec_tests = "\n".join(state["spec_tests"])
    
    prompt = f"""
    You are an expert at synthesizing information. Your primary function is to ensure that 
    the final test suite is efficient and free of redundancy.
    
    Merge the following two sets of test cases. Intelligently identify and remove duplicate 
    or overlapping test cases, and combine related ones.
    
    User Story Test Cases:
    {user_tests}
    
    Specification Test Cases:
    {spec_tests}
    
    Provide a final, merged list of unique test cases in a single markdown table. 
    Ensure the table includes columns for Test Case ID, Description, Steps, and Expected Results.
    """
    
    response = llm.invoke(prompt)
    state["merged_tests"] = response.content
    return state

def add_traceability(state: GraphState) -> GraphState:
    """Add traceability information to test cases"""
    prompt = f"""
    You are a quality assurance auditor who ensures every requirement is tested. 
    You meticulously track the origin of each test case.
    
    For each test case in the provided merged list, add a 'Source' column. 
    Based on the original requirements, determine if the test case originated from the 
    'User Story', the 'Specification', or was relevant to 'Both'.
    
    Here is the merged list of test cases:
    {state["merged_tests"]}
    
    Provide the final list of merged test cases in a markdown table, with an additional 
    'Source' column populated with 'User Story', 'Specification', or 'Both' for each test case.
    """
    
    response = llm.invoke(prompt)
    state["final_tests"] = response.content
    return state

def refine_test_cases(state: GraphState) -> GraphState:
    """Refine test cases based on user feedback"""
    prompt = f"""
    You are a senior QA lead who reviews test suites and perfects them based on feedback 
    from the development team and stakeholders. You understand user requests for changes 
    and implement them accurately.
    
    Here is the original list of test cases:
    ---
    {state["final_tests"]}
    ---
    
    Here is the user's request for changes:
    ---
    {state["user_request"]}
    ---
    
    Your task is to update the original list of test cases according to the user's request.
    You can add new test cases, delete irrelevant ones, or modify existing ones.
    The final output must be the complete, updated list of test cases in the same markdown 
    table format as the original.
    """
    
    response = llm.invoke(prompt)
    state["final_tests"] = response.content
    return state

def route_step(state: GraphState) -> str:
    """Route based on the current step"""
    if state["step"] == "refine":
        return "refine"
    else:
        return "generate"
    
if not llm:
    st.warning("Please enter your correct API Key to proceed.")
    st.stop()