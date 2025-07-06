📄 Agentic Test Case Generator with Conversational Refinement
An interactive Streamlit-based application that transforms user stories and technical specifications into comprehensive test cases using LLMs. Users can upload PDFs, generate test cases, and refine them in real-time through natural language prompts.

🚀 Features
🧠 LLM-Powered Test Case Generation using LangGraph and Groq’s LLaMA 3 API

📄 Upload user stories and specifications as PDFs

🧪 Get structured test cases in a clean markdown table

🗣️ Chat interface for refining and extending test cases via conversational feedback

🔐 Built-in API key management via sidebar

🔁 Maintains full traceability between requirements and test cases

📂 Project Structure
bash
Copy
Edit
.
├── main.py          # Streamlit app frontend
├── nodes.py         # Core logic for test generation and refinement
├── graph.py         # LangGraph workflow definition
├── state.py         # Shared state definition across graph steps
└── README.md        # Project documentation
📸 Demo


Upload your documents → View initial test cases → Ask for refinements like:
“Add a negative test for login failure” or “Include edge cases for file upload.”

⚙️ Requirements
Python 3.9+

Groq API key

PDF files containing user stories and specifications

🔧 Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
If you don't have a requirements.txt yet, here's a starting point:

txt
Copy
Edit
streamlit
PyPDF2
langchain
langgraph
langchain-groq
🔑 Set Up Groq API Key
Sign up at Groq Console

Copy your API key

Launch the app and paste your API key into the sidebar

▶️ Running the App
bash
Copy
Edit
streamlit run main.py
🧠 How It Works
This app uses a LangGraph workflow with the following steps:

generate_user_story_tests: Extracts test cases from user stories

generate_spec_tests: Extracts test cases from technical specs

merge_test_cases: Merges & deduplicates all cases

add_traceability: Adds traceability source info

refine_test_cases: Updates tests based on user feedback

💬 Sample User Prompts for Refinement
“Add test cases for invalid email format”

“Combine duplicate login tests”

“Include performance edge cases”

📈 Future Improvements
Export to CSV or Jira-compatible format

Multi-file PDF parsing

UI enhancements for previewing test tables

Support for other LLM providers (OpenAI, Claude, etc.)

