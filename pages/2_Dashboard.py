import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import get_statistics, get_score_history

from database.database import get_statistics

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analytics Dashboard")

st.markdown("View statistics of all prompt comparisons.")

stats = get_statistics()

if stats:

    total, highest, average, lowest = stats

    total = total if total is not None else 0
    highest = highest if highest is not None else 0
    average = average if average is not None else 0
    lowest = lowest if lowest is not None else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📌 Total Comparisons", total)

    with col2:
        st.metric("🏆 Highest Score", highest)

    with col3:
        st.metric("📈 Average Score", f"{average:.2f}")

    with col4:
        st.metric("📉 Lowest Score", lowest)

else:
    st.info("No statistics available.")


st.divider()

st.subheader("📊 Prompt Score Comparison")

history = get_score_history()

if history:

    df = pd.DataFrame(
        history,
        columns=[
            "Prompt",
            "Score",
            "Date"
        ]
    )

    fig = px.bar(
        df,
        x="Prompt",
        y="Score",
        color="Prompt",
        title="Prompt Scores"
    )

    st.plotly_chart(fig, use_container_width=True)

else:

    st.info("No data available for charts.")



st.divider()

st.subheader("📈 Score Trend")

if history:

    df["Comparison"] = range(1, len(df) + 1)

    fig2 = px.line(
        df,
        x="Comparison",
        y="Score",
        markers=True,
        title="Score Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("🥧 Score Distribution")

if history:

    fig3 = px.pie(
        df,
        names="Prompt",
        values="Score",
        title="Prompt Score Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )