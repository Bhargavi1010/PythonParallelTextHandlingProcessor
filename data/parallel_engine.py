import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from sentiment_rules import analyze_sentiment


def single_processing(data):

    start = time.time()

    results = [analyze_sentiment(x) for x in data]

    end = time.time()

    return results, end - start


def thread_processing(data):

    start = time.time()

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(analyze_sentiment, data))

    end = time.time()

    return results, end - start


def multi_processing(data):

    start = time.time()

    with Pool() as pool:
        results = pool.map(analyze_sentiment, data)

    end = time.time()

    return results, end - start


# ---------- TEST RUN ----------

if __name__ == "__main__":

    sample_data = [
        "this product is good",
        "very bad experience",
        "excellent service",
        "poor quality item",
        "great product",
        "worst purchase"
    ] * 10000

    s_res, s_time = single_processing(sample_data)
    t_res, t_time = thread_processing(sample_data)
    m_res, m_time = multi_processing(sample_data)

    print("\nProcessing Performance")
    print("----------------------------")

    print("Single Processing :", round(s_time,4), "sec")
    print("Thread Processing :", round(t_time,4), "sec")
    print("Multiprocessing   :", round(m_time,4), "sec")

    fastest = min(s_time, t_time, m_time)

    if fastest == s_time:
        method = "Single"
    elif fastest == t_time:
        method = "Thread"
    else:
        method = "Multiprocessing"

    print("Fastest Method :", method)
    
    
    