import csv
import random

reviews = [
    "this product is good",
    "very bad experience",
    "excellent service",
    "poor quality item",
    "great product",
    "worst purchase",
    "happy with the product",
    "terrible support",
    "average item",
]

with open("data/dataset.csv", "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow(["text"])

    for i in range(60000):

        writer.writerow([random.choice(reviews)])

print("Dataset created with 60000 rows")