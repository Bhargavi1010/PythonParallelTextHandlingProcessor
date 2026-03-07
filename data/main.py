import pandas as pd
import time
from collections import Counter

from chunk_manager import split_into_chunks
from parallel_engine import single_processing, thread_processing, multi_processing
from sentiment_rules import analyze_sentiment
from db_manager import setup_db, bulk_insert, query_test
from csv_exporter import export_csv


def main():

    print("\nLoading dataset...")

    data = pd.read_csv("data/dataset.csv")["text"].tolist()

    print("Total records:", len(data))


    # ---------------- CHUNKING ----------------

    start = time.time()

    rows, chunks = split_into_chunks("data/dataset.csv")

    end = time.time()

    print("\nChunk Processing Result")
    print("---------------------------")
    print("Total rows:", len(rows))
    print("Total chunks:", len(chunks))
    print("Chunk Processing Time :", round(end-start,4),"sec")


    # ---------------- PARALLEL PROCESSING ----------------

    single_res, single_time = single_processing(data)
    thread_res, thread_time = thread_processing(data)
    multi_res, multi_time = multi_processing(data)


    print("\nProcessing Performance")
    print("---------------------------")

    print("Single Processing :", round(single_time,4),"sec")
    print("Thread Processing :", round(thread_time,4),"sec")
    print("Multiprocessing :", round(multi_time,4),"sec")


    fastest = min(
        [("Single",single_time),
         ("Thread",thread_time),
         ("Multiprocessing",multi_time)],
        key=lambda x: x[1]
    )

    print("Fastest Method :", fastest[0])


    # ---------------- SENTIMENT DISTRIBUTION ----------------

    dist = Counter(single_res)

    total = len(single_res)

    print("\nSentiment Distribution")
    print("---------------------------")

    for k,v in dist.items():

        percent = round((v/total)*100,1)

        print(k.capitalize(),":",v,"(",percent,"%)")


    # ---------------- DATABASE PERFORMANCE ----------------

    setup_db()

    insert_data = list(zip(data,single_res))

    insert_time = bulk_insert(insert_data)

    before, after = query_test()


    print("\nDatabase Performance")
    print("---------------------------")

    print("Bulk Insert Time :", round(insert_time,4),"sec")

    print("Query Before Index :", round(before,4),"sec")

    print("Query After Index :", round(after,4),"sec")

    print("Index Improvement :", round(before/after,2),"X Faster")


    # ---------------- CSV EXPORT ----------------

    export_csv(insert_data)

    print("\nCSV Export Completed")


    # ---------------- SCALABILITY ----------------

    print("\nScalability Observation")

    print("---------------------------")

    print("Processing time increases as dataset grows")

    print("Multiprocessing performs better for large datasets")

    print("Index significantly improves query performance")


    print("\nProject Execution Completed Successfully")


# IMPORTANT FOR MULTIPROCESSING
if __name__ == "__main__":
    main()