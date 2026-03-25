import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError
from processor import (
    process_parallel,
    process_normal,
    analyze_sentence,
    get_core_count
)
from database import init_db, insert_results, fetch_results, clear_database

init_db()

st.set_page_config(layout="wide")
st.title("🚀 Parallel Text Processing System")

# SESSION STATE
for key in ["data", "parallel_time", "normal_time"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Sidebar
st.sidebar.header("Upload Section")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or TXT",
    type=["csv", "txt"]
)

start = st.sidebar.button("Start Processing")
clear = st.sidebar.button("Clear Data")

if clear:
    clear_database()
    st.session_state.data = None
    st.success("Data Cleared")
    st.rerun()

# ================= MANUAL =================
st.subheader("⚡ Manual Sentence Analysis")

manual = st.text_input("Enter sentence")

if manual:
    pos, neg, score = analyze_sentence(manual)

    sentiment = "Neutral"
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"

    st.write(f"Positive: {pos}")
    st.write(f"Negative: {neg}")
    st.write(f"Score: {score}")
    st.success(f"Sentiment: {sentiment}")

# ================= PROCESS =================
if uploaded_file and start:

    try:
        # ===== TXT FILE =====
        if uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")

            if not text.strip():
                st.warning("⚠️ File has no data. Please upload valid data")
                st.stop()

            data = [i.strip() for i in text.split(".") if i.strip()]

        # ===== CSV FILE =====
        else:
            df = pd.read_csv(uploaded_file)

            if df.empty:
                st.warning("⚠️ File has no data. Please upload valid data")
                st.stop()

            data = df.iloc[:, 0].dropna().astype(str).tolist()

        # ===== FINAL CHECK =====
        if not data:
            st.warning("⚠️ File has no usable data")
            st.stop()

        # ===== PROCESS =====
        normal_res, normal_time = process_normal(data)
        parallel_res, parallel_time = process_parallel(data)

        final_data = []
        for text, (_, _, score) in zip(data, parallel_res):

            sentiment = "Neutral"
            if score > 0:
                sentiment = "Positive"
            elif score < 0:
                sentiment = "Negative"

            final_data.append((text, score, sentiment))

        insert_results(final_data)

        st.session_state.data = fetch_results()
        st.session_state.parallel_time = parallel_time
        st.session_state.normal_time = normal_time

        st.success("Processing Completed")

    except EmptyDataError:
        st.error("❌ File has no data. Please upload valid data")
        st.stop()

    except Exception as e:
        st.error("❌ Invalid file format or corrupted file")
        st.stop()

# ================= DISPLAY =================
if st.session_state.data:

    df = pd.DataFrame(
        st.session_state.data,
        columns=["ID", "Text", "Score", "Sentiment", "Timestamp"]
    )

    # FILE REVIEW
    st.subheader("📄 File Review")
    st.dataframe(df)

    # DASHBOARD
    st.subheader("📊 Dashboard")

    total = len(df)
    pos = (df["Score"] > 0).sum()
    neg = (df["Score"] < 0).sum()
    neu = total - pos - neg

    c1, c2, c3 = st.columns(3)
    c1.metric("Total", total)
    c2.metric("Positive", pos)
    c3.metric("Negative", neg)

    # PROCESS INFO
    st.subheader("⏱ Processing Info")

    st.write(f"Last Processed Time: {df['Timestamp'].iloc[0]}")
    st.write(f"Parallel Time: {st.session_state.parallel_time} sec")
    st.write(f"Normal Time: {st.session_state.normal_time} sec")
    st.write(f"Cores Used: {get_core_count()}")

    # VISUALIZATION
    st.subheader("📈 Visualization")

    chart = pd.DataFrame({
        "Sentiment": ["Positive", "Negative", "Neutral"],
        "Count": [pos, neg, neu]
    })

    st.bar_chart(chart.set_index("Sentiment"))

    st.pyplot(chart.set_index("Sentiment").plot.pie(
        y="Count", autopct="%1.1f%%"
    ).figure)

    # SEARCH
    st.subheader("🔎 Smart Search + Analysis")

    keyword = st.text_input("Enter sentence or keyword")

    if keyword:
        pos, neg, score = analyze_sentence(keyword)

        st.write(f"Input Analysis → Pos: {pos}, Neg: {neg}, Score: {score}")

        filtered = df[df["Text"].str.contains(keyword, case=False)]

        if not filtered.empty:
            st.dataframe(filtered)
        else:
            st.warning("No match → showing similar sentiment")

            if score > 0:
                st.dataframe(df[df["Score"] > 0].head(5))
            elif score < 0:
                st.dataframe(df[df["Score"] < 0].head(5))
            else:
                st.dataframe(df[df["Score"] == 0].head(5))

    # EXPORT
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "results.csv")