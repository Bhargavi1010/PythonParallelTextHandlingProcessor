positive_words = [
    "good","great","excellent","happy","love","amazing","best","nice"
]

negative_words = [
    "bad","poor","worst","terrible","hate","awful","problem","issue"
]


def analyze_sentiment(text):

    score = 0

    text = text.lower()

    for w in positive_words:
        if w in text:
            score += 1

    for w in negative_words:
        if w in text:
            score -= 1

    if score > 0:
        return "positive"

    elif score < 0:
        return "negative"

    else:
        return "neutral"


# test output
if __name__ == "__main__":

    samples = [
        "this product is good",
        "very bad experience",
        "average item"
    ]

    print("\nSentiment Test Result")
    print("----------------------")

    for s in samples:
        result = analyze_sentiment(s)
        print(s, "->", result)