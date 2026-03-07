import time


def split_into_chunks(path, chunk_size=1200):

    with open(path) as f:
        lines = f.readlines()[1:]

    chunks = []

    for i in range(0, len(lines), chunk_size):
        chunks.append(lines[i:i+chunk_size])

    return lines, chunks


# Run test when file executed directly
if __name__ == "__main__":

    start = time.time()

    rows, chunks = split_into_chunks("data/dataset.csv")

    end = time.time()

    print("\nChunk Processing Result")
    print("---------------------------")

    print("Total rows:", len(rows))
    print("Total chunks:", len(chunks))

    print("Chunk processing time:", round(end-start,4), "sec")