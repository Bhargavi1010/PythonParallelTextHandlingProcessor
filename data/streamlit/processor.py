import re
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

POSITIVE_WORDS = {
    "good", "great", "excellent", "amazing", "awesome", "fantastic",
    "nice", "happy", "love", "like", "liked", "wonderful",
    "best", "positive", "enjoy", "enjoyed", "satisfied",
    "perfect", "fast", "quick", "smooth", "helpful",
    "friendly", "clean", "beautiful", "easy",
    "comfortable", "delightful", "brilliant", "super"
}

NEGATIVE_WORDS = {
    "bad", "worst", "poor", "terrible", "awful", "hate", "hated",
    "dislike", "boring", "slow", "late", "delay",
    "problem", "issue", "error", "bug", "hard",
    "difficult", "confusing", "annoying", "disappointed",
    "dirty", "noisy", "expensive", "waste",
    "useless", "fail", "failed", "broken", "negative"
}

INTENSIFIERS = {"very": 2, "extremely": 3, "too": 2}
NEGATIONS = {"not", "never", "no"}


def analyze_sentence(sentence):
    words = re.findall(r'\w+', sentence.lower())

    pos, neg = 0, 0

    i = 0
    while i < len(words):
        word = words[i]
        multiplier = 1

        if word in INTENSIFIERS and i + 1 < len(words):
            multiplier = INTENSIFIERS[word]
            i += 1
            word = words[i]

        is_negative = i > 0 and words[i - 1] in NEGATIONS

        if word in POSITIVE_WORDS:
            if is_negative:
                neg += multiplier
            else:
                pos += multiplier

        elif word in NEGATIVE_WORDS:
            if is_negative:
                pos += multiplier
            else:
                neg += multiplier

        i += 1

    score = pos - neg
    return pos, neg, score


def process_normal(data):
    start = time.time()
    results = [analyze_sentence(x) for x in data]
    end = time.time()
    return results, round(end - start, 4)


def process_parallel(data):
    start = time.time()

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(analyze_sentence, data))

    end = time.time()
    return results, round(end - start, 4)


def get_core_count():
    return multiprocessing.cpu_count()