import streamlit as st
from llm.gemini import generate_response
from llm.evaluator import evaluate_response
from llm.optimizer import optimize_prompt
from utils.pdf_generator import create_pdf
from database.database import (
    create_database,
    save_history
)

create_database()
if "results" not in st.session_state:
    st.session_state.results = []

if "best_prompt" not in st.session_state:
    st.session_state.best_prompt = None

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.title("🤖 PromptPilot AI")

    st.markdown("---")

    st.success("🚀 AI Prompt Engineering Platform")

    st.markdown("---")

    st.markdown("### 👨‍💻 Developer")

    st.write("**Vinay Kumar**")

    st.write("B.Tech CSE (AI & ML)")

    st.write("Lovely Professional University")

    st.markdown("---")

    st.caption("Version 1.0")

load_css()

st.set_page_config(
    page_title="Prompt Engineering Optimiser",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<div style="text-align:center; padding:20px 0;">

<h1 style="color:#4F8BF9;">
🤖 PromptPilot AI
</h1>

<h3>
Optimize • Compare • Evaluate AI Prompts
</h3>

<p style="font-size:18px;">
AI-powered platform for prompt engineering,
optimization, evaluation and comparison using Google Gemini.
</p>

</div>
""", unsafe_allow_html=True)
st.divider()


st.header("✨ AI Prompt Optimizer")

# Initialize session state
if "optimized_prompt" not in st.session_state:
    st.session_state.optimized_prompt = ""

if "promptA_text" not in st.session_state:
    st.session_state.promptA_text = ""

user_prompt = st.text_area(
    "Enter a prompt to optimize",
    height=120,
    placeholder="Example: Explain Python"
)

col_opt1, col_opt2 = st.columns([1, 1])

with col_opt1:

    if st.button("✨ Optimize Prompt", key="optimize_btn"):

        if user_prompt.strip():

            with st.spinner("Optimizing prompt..."):

                st.session_state.optimized_prompt = optimize_prompt(user_prompt)

        else:

            st.warning("Please enter a prompt first.")

with col_opt2:

    if st.session_state.optimized_prompt:

        if st.button("➡ Use as Prompt A", key="use_prompt_button"):

            st.session_state.promptA_text = st.session_state.optimized_prompt

            st.success("Optimized prompt loaded into Prompt A!")

if st.session_state.optimized_prompt:

    st.subheader("🚀 Optimized Prompt")

    st.code(st.session_state.optimized_prompt, language="text")

st.divider()

col1, col2 = st.columns(2)

with col1:
    prompt1 = st.text_area(
    "Prompt A",
    height=200,
    placeholder="Enter first prompt...",
    key="promptA_text"
)

with col2:
    prompt2 = st.text_area(
        "Prompt B",
        height=200,
        placeholder="Enter second prompt..."
    )

prompt3 = st.text_area(
    "Prompt C (Optional)",
    height=150,
    placeholder="Enter third prompt..."
)
# Store comparison state
if "comparison_done" not in st.session_state:
    st.session_state.comparison_done = False

if st.button("🚀 Compare Prompts", use_container_width=True):

    prompts = []

    if prompt1.strip():
        prompts.append(("Prompt A", prompt1))

    if prompt2.strip():
        prompts.append(("Prompt B", prompt2))

    if prompt3.strip():
        prompts.append(("Prompt C", prompt3))

    if len(prompts) < 2:
        st.warning("Please enter at least two prompts.")

    else:

        results = []
        st.session_state.results = []

        for title, prompt in prompts:

            # st.subheader(title)

            with st.spinner(f"Generating response for {title}..."):
                response = generate_response(prompt)
                score = evaluate_response(prompt, response)

            # st.markdown(f"""
            # <div class="card">

            # ### 🤖 {title}

            # <div class="score">
            # ⭐ AI Score : {score}/100
            # </div>

            # </div>
            # """, unsafe_allow_html=True)

            # st.write(response)

            results.append({
                "title": title,
                "score": score,
                "response": response
            })
            st.session_state.results = results

            save_history(title, prompt, response, score)

            # st.divider()

        # -----------------------------
        # Best Prompt (Outside the loop)
        # -----------------------------

        best_prompt = max(results, key=lambda x: x["score"])

        st.session_state.best_prompt = best_prompt
        st.session_state.results = results

#         st.markdown("""
# # 🏆 Best Prompt
# """)

#         st.markdown(f"""
# <div class="card">

# ## 🥇 {best_prompt['title']}        

# <div class="score">

# Score : {best_prompt['score']}/100

# </div>

# </div>
# """, unsafe_allow_html=True)

#         st.subheader("📄 Best Response")

#         st.write(best_prompt["response"])

# # Generate PDF
#         pdf_file = create_pdf(best_prompt, results)

#         with open(pdf_file, "rb") as file:

#             st.download_button(
#                 label="📄 Download PDF Report",
#                 data=file,
#                 file_name="Prompt_Report.pdf",
#                 mime="application/pdf",
#                 use_container_width=True
#             )
# PDF Download
if st.session_state.best_prompt is not None:

    pdf_file = create_pdf(
        st.session_state.best_prompt,
        st.session_state.results
    )

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name="Prompt_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
            # -----------------------------
            # Show previous comparison after rerun
            # -----------------------------
if st.session_state.best_prompt is not None:
        # Show all compared prompts again
    for result in st.session_state.results:

        st.subheader(result["title"])

        st.markdown(f"""
        <div class="card">

        ### 🤖 {result['title']}

        <div class="score">
        ⭐ AI Score : {result['score']}/100
        </div>

        </div>
        """, unsafe_allow_html=True)

        st.write(result["response"])

        st.divider()

    st.divider()

    st.markdown("# 🏆 Best Prompt")

    st.markdown(f"""
    <div class="card">

    ## 🥇 {st.session_state.best_prompt['title']}

    <div class="score">

    Score : {st.session_state.best_prompt['score']}/100

    </div>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("📄 Best Response")

    st.write(st.session_state.best_prompt["response"])


