
#  Agentic Test Case Generator with Conversational Refinement

**Generate structured, traceable test cases from user stories and specifications — and refine them via natural language conversation.**

Built with [Streamlit](https://streamlit.io), [LangGraph](https://docs.langchain.com/langgraph/), and powered by [Groq](https://groq.com), this app streamlines test case creation by combining intelligent automation with human feedback.

---

## 🚀 Features

- 📄 **Upload PDFs** containing user stories and technical specifications.
- 🧠 **LLM-powered generation** of detailed test cases for both.
- 🔄 **Smart merging** of overlapping or duplicate tests.
- 🔗 **Traceability** — track test case origin (User Story, Spec, or Both).
- 💬 **Conversational refinement** using simple prompts (e.g., “Add a negative test case for login”).

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend Orchestration**: LangGraph
- **LLM Provider**: Groq (LLaMA3 via `langchain_groq`)
- **PDF Parsing**: PyPDF2

---

## 📦 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/agentic-test-case-generator.git
cd agentic-test-case-generator
```

2. **Install Dependencies**

We recommend using a virtual environment:

```bash
pip install -r requirements.txt
```

_Example `requirements.txt`:_

```text
streamlit
PyPDF2
langgraph
langchain
langchain-groq
```

3. **Run the App**

```bash
streamlit run main.py
```

---

## 🔐 Authentication

The app requires a **Groq API key**.

- You’ll be prompted to enter the API key in the **sidebar**.
- You can clear the stored key via the "Logout" button.

Get your key from [Groq Console](https://console.groq.com).

---

## 📂 How It Works

### 1. Upload PDFs
- One for **user stories**
- One for **technical specifications**

### 2. Click “Generate Test Cases”
- Extracts text from PDFs
- Creates test cases from each source
- Merges and deduplicates them
- Adds a traceability column

### 3. Chat with the AI
Use natural language prompts like:

- “Add more edge cases.”
- “Include performance test scenarios.”
- “Remove tests related to password reset.”

The AI refines the current list of test cases accordingly.

---

## 🧱 Project Structure

```
.
├── main.py             # Streamlit UI + interaction logic
├── nodes.py            # LLM prompt functions (test generation, merge, refine)
├── graph.py            # LangGraph workflow definition
├── state.py            # State schema for LangGraph
└── README.md
```

---

## ✅ Example Use Case

Upload:
- `user_stories.pdf`: describing a login system
- `spec.pdf`: outlining technical requirements for auth flow

The app will generate a structured markdown test suite like:

| Test Case ID | Description | Steps | Expected Results | Source |
|--------------|-------------|-------|------------------|--------|
| TC-01        | Valid login | 1. Go to login page... | User is logged in | Both |

Then ask:
> “Add a test for password expiration handling.”

And it will update the test suite accordingly.

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open issues for bugs, improvements, or ideas.

---

## 🌐 Acknowledgments

- [LangChain](https://www.langchain.com/)
- [LangGraph](https://docs.langchain.com/langgraph/)
- [Groq](https://groq.com)
- [Streamlit](https://streamlit.io)
