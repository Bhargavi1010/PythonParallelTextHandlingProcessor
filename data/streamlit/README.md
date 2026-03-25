🚀 Parallel Text Processing System

📌 Project Overview

The Parallel Text Processing System is a scalable and efficient text analysis application designed to process large datasets using parallel processing techniques.

The system performs:

- Sentiment analysis (Positive, Negative, Neutral)
- Chunk-based text processing
- Parallel execution for faster performance
- Real-time data visualization
- Smart search and analysis

---

🎯 Features

📂 File Upload

- Upload CSV and TXT files
- Handles large datasets efficiently
- Supports empty dataset validation

✍️ Manual Sentence Analysis

- Analyze any input sentence
- Displays:
  - Positive count
  - Negative count
  - Score
  - Final sentiment

⚡ Parallel Processing

- Uses multi-core processing
- Processes multiple chunks simultaneously
- Faster than sequential execution

🧩 Chunk-Based Processing

- Splits large data into smaller chunks
- Each chunk processed independently

🔍 Smart Search + Analysis

- Search keyword or sentence
- Retrieves related data from dataset
- Displays sentiment results

📊 Dashboard

- Total records
- Positive count
- Negative count

📈 Visualization

- Bar chart (sentiment distribution)
- Pie chart (percentage distribution)

⏱ Performance & Timestamp

- Last processed time
- Parallel execution time
- Sequential execution time
- Number of CPU cores used

📁 Export

- Download processed data as CSV

---

🧠 System Architecture

Input (File / Manual)
↓
Data Cleaning
↓
Chunk Division
↓
Parallel Processing Engine
↓
Sentiment Analysis
↓
Database Storage
↓
Search / Dashboard / Visualization

---

⚙️ How the System Works

1. Data Division

- Input text is divided into smaller chunks
- Improves efficiency and scalability

2. Chunk Processing

- Each chunk is processed independently
- Words matched with sentiment dictionary

3. Parallel Processing

- Multiple chunks processed at same time
- Uses multi-core CPU

4. Task Distribution

- Each chunk is assigned to a worker
- Tasks executed simultaneously

5. Result Merging

- All results are combined
- Final sentiment calculated

---

😊 Sentiment Analysis Logic

Score = Positive Words - Negative Words

Example:

Input:
"good bad worst"

Output:
Positive: 1
Negative: 2
Score: -1
Sentiment: Negative

---

📂 Dataset Details

Supported formats:

- CSV
- TXT

Data types:

- Reviews
- Comments
- Sentences

---

⚡ Performance Comparison

Mode| Performance
Sequential| Slower
Parallel| Faster ⚡

---

⚠️ Edge Cases Handled

- Empty dataset → Neutral handling
- Unknown words → Ignored safely
- Manual input → Works independently
- Large data → Chunk processing
- Search mismatch → Fixed

---

🖥️ Project Structure

streamlit/
│── app.py
│── processor.py
│── parallel_engine.py
│── chunk_manager.py
│── sentiment_rules.py
│── db_manager.py
│── database.py
│── csv_exporter.py
│── main.py
│── dataset.csv
│── empty.csv

---

▶️ How to Run

Step 1:

pip install streamlit pandas

Step 2:

streamlit run app.py

Step 3:

Open browser → http://localhost:8501

---

📊 UI Sections

- Upload Section
- Manual Sentence Analysis
- File Review
- Dashboard
- Visualization (Bar + Pie Charts)
- Smart Search

---

🧪 Testing

Tested with:

- Positive inputs
- Negative inputs
- Mixed sentences
- Empty dataset
- Large datasets

---

🔮 Future Enhancements

- Email feature
- Advanced filtering
- UI improvements
- ML-based sentiment analysis

---

📌 Conclusion

This system provides:

- Fast parallel processing
- Accurate sentiment analysis
- Professional visualization
- User-friendly interface

---

👨‍💻 Author

Marella Bhargavi 


📜 License

This project is licensed under the MIT License.