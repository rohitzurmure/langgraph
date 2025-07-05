import streamlit as st
from PyPDF2 import PdfReader

from graph import create_test_case_graph
from state import GraphState






#
# os.environ["groq_api_key"] = groq_api_key

def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in reader.pages])
    return ""

# --- Streamlit UI ---
st.set_page_config(page_title="Agentic Test Case Generator", layout="wide")
st.title("📄 Agentic Test Case Generator with Conversational Refinement")
st.markdown("Upload user stories and specifications to generate test cases. Then, chat with the AI to refine them.")

# --- State Management for Conversation ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Please upload your PDF files to begin."}]
if "generated_result" not in st.session_state:
    st.session_state.generated_result = []

# --- Sidebar for PDF Uploads ---
with st.sidebar:
    st.header("Upload Documents")
    user_pdf = st.file_uploader("Upload User Stories PDF", type="pdf")
    spec_pdf = st.file_uploader("Upload Specification PDF", type="pdf")
   
    if st.button("Generate Test Cases"):
        if user_pdf and spec_pdf:
            with st.spinner("Reading PDFs and generating test cases... This may take a moment."):
                user_text = extract_text_from_pdf(user_pdf)
                spec_text = extract_text_from_pdf(spec_pdf)

                # Create and run LangGraph
                graph = create_test_case_graph()
                
                # Initialize state
                initial_state = GraphState(
                    user_stories=user_text,
                    specifications=spec_text,
                    user_story_tests=[],
                    spec_tests=[],
                    merged_tests="",
                    final_tests="",
                    user_request="",
                    step="generate"
                )
                
                # Run the graph
                result = graph.invoke(initial_state)
                
                
                st.session_state.generated_result = result["final_tests"]
                st.session_state.messages.append({"role": "assistant", "content": "I have generated the initial test cases based on your documents. You can see them below. Feel free to ask me to make any changes or additions."})
                st.session_state.messages.append({"role": "assistant", "content": result["final_tests"]})
                st.success("Test cases generated successfully!")
        else:
            st.warning("Please upload both User Stories and Specification PDFs.")

# --- Main Chat Interface ---
st.header("Conversation")

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Handle user input for refinement
if prompt := st.chat_input("e.g., 'Add a negative test case for the login functionality.'"):
    if not st.session_state.generated_result:
        st.warning("Please generate the initial test cases first by uploading documents and clicking the button in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        with st.spinner("Refining the test cases based on your request..."):
            # Create refinement graph
            graph = create_test_case_graph()
            
            # Initialize state for refinement
            refinement_state = GraphState(
                user_stories="",
                specifications="",
                user_story_tests=[],
                spec_tests=[],
                merged_tests="",
                final_tests=st.session_state.generated_result,
                user_request=prompt,
                step="refine"
            )
            
            # Run refinement
            refined_result = graph.invoke(refinement_state)
            
            # Update the stored result and conversation history
            st.session_state.generated_result = refined_result["final_tests"]
            st.session_state.messages.append({"role": "assistant", "content": refined_result["final_tests"]})
            st.chat_message("assistant").markdown(refined_result["final_tests"])