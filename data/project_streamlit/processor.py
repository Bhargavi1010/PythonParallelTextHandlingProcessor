import concurrent.futures

positive_words = ["good", "great", "excellent", "amazing", "happy"]
negative_words = ["bad", "poor", "terrible", "sad"]

def analyze_text(text):
    text_lower = text.lower()
    score = 0

    for word in positive_words:
        if word in text_lower:
            score += 1

    for word in negative_words:
        if word in text_lower:
            score -= 1

    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "Text": text,
        "Score": score,
        "Sentiment": sentiment
    }

def process_data(text_list):
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        processed = executor.map(analyze_text, text_list)
        results = list(processed)

    return results