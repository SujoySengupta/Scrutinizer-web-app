import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Code Scrutinizer", layout="centered")
st.title("AI Code Scrutinizer (Cloud Edition)")
st.markdown("Automated architectural and structural code reviewer, powered by OpenRouter.")

try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")

if not api_key:
    st.info("Enter your API key in the sidebar to begin.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key.strip(),
    default_headers={
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "AI Code Scrutinizer"
    }
)

code_to_review = st.text_area(
    "Paste your source code here:", 
    height=350, 
    placeholder="// Paste Java, Python, SQL, or C code here for architecture review..."
)

if st.button("Run Architectural Audit", type="primary"):
    if not code_to_review.strip():
        st.error("Paste some source code before running!")
    else:
        with st.spinner("Analyzing codebase architecture..."):
            try:
                system_prompt = "You are an expert enterprise Software Architect with a very deep experience. Perform a strict architectural critique on the following code snippet. Focus entirely on structural analysis: 1. Architectural violations. 2. Potential performance bottlenecks. 3. Code maintainability gaps. Provide raw, direct, and actionable engineering feedback using simple terms."
                
                response = client.chat.completions.create(
                    model="google/gemini-2.5-flash",
                    max_tokens = 2000,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Code to analyze:\\n{code_to_review}\n"}
                    ]
                )
                
                st.success("Audit Complete")
                st.subheader("Architectural Audit Report")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"API Error: {e}")