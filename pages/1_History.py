import streamlit as st
import pandas as pd

from database.database import get_history

st.set_page_config(
    page_title="Prompt History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Prompt History")

st.markdown("View all previously compared prompts.")

history = get_history()
search = st.text_input(
    "🔍 Search Prompt",
    placeholder="Type Prompt A, Prompt B..."
)

if history:

    df = pd.DataFrame(
        history,
        columns=[
            "Date & Time",
            "Prompt",
            "Score"
        ]
    )
    if search:

        df = df[
            df["Prompt"].str.contains(
                search,
                case=False,
                na=False
            )
        ]
    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download History (CSV)",
        data=csv,
        file_name="prompt_history.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info("No history available.")