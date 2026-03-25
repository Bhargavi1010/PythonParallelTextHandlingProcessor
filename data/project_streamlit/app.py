import streamlit as st
import pandas as pd
import time
import plotly.express as px

from processor import process_data
from database import create_table, insert_data, fetch_data, clear_data

st.set_page_config(
    page_title="Text Processing System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DARK UI ----------
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    .css-1d391kg {
        background-color: #111827;
    }
    </style>
""", unsafe_allow_html=True)

create_table()

st.title("🚀 Parallel Text Processing Dashboard")

# ---------- SIDEBAR ----------
st.sidebar.header("⚙ Controls")

uploaded_files = st.sidebar.file_uploader(
    "Upload Files",
    type=["txt", "csv", "xlsx"],
    accept_multiple_files=True
)

start_button = st.sidebar.button("▶ Start Processing")
clear_button = st.sidebar.button("🗑 Clear Data")

# ---------- CLEAR ----------
if clear_button:
    clear_data()
    st.success("Data Cleared")

# ---------- FILE HANDLING ----------
all_texts = []

if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)} file(s) uploaded")

    for file in uploaded_files:

        if file.type == "text/plain":
            text = file.read().decode("utf-8")
            all_texts.extend(text.split("\n"))

        elif file.type == "text/csv":
            df = pd.read_csv(file)
            all_texts.extend(df.astype(str).values.flatten())

        elif "excel" in file.type:
            df = pd.read_excel(file)
            all_texts.extend(df.astype(str).values.flatten())

# ---------- PROCESS ----------
if start_button and all_texts:

    st.subheader("⏳ Processing...")

    progress_bar = st.progress(0)
    status_text = st.empty()

    total = len(all_texts)
    results = []

    for i, chunk in enumerate(all_texts):
        processed = process_data([chunk])  # one by one for live progress
        results.extend(processed)

        percent = int(((i + 1) / total) * 100)
        progress_bar.progress(percent)
        status_text.text(f"Processing {i+1}/{total}")

    insert_data(results)

    st.success("✅ Processing Completed")

# ---------- FETCH ----------
data = fetch_data()

if data:
    df = pd.DataFrame(data, columns=["Text", "Score", "Sentiment"])

    st.subheader("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", len(df))
    col2.metric("Positive", (df["Sentiment"] == "Positive").sum())
    col3.metric("Negative", (df["Sentiment"] == "Negative").sum())
    col4.metric("Neutral", (df["Sentiment"] == "Neutral").sum())

    # ---------- CHARTS ----------
    st.subheader("📈 Visualizations")

    sentiment_counts = df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    col1, col2 = st.columns(2)

    # Bar Chart
    fig_bar = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Count",
        title="Sentiment Distribution"
    )
    col1.plotly_chart(fig_bar, use_container_width=True)

    # Pie Chart
    fig_pie = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        title="Sentiment Share"
    )
    col2.plotly_chart(fig_pie, use_container_width=True)

    # ---------- TABLE ----------
    st.subheader("📄 Data Table")
    st.dataframe(df, use_container_width=True)

    # ---------- SEARCH ----------
    st.subheader("🔍 Search")

    keyword = st.text_input("Enter keyword")

    if keyword:
        filtered = df[df["Text"].str.contains(keyword, case=False, na=False)]
        st.dataframe(filtered)

    # ---------- EXPORT ----------
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        data=csv,
        file_name="results.csv",
        mime="text/csv"
    )