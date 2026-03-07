import csv


def export_csv(data):

    with open("output.csv", "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow(["review", "sentiment"])

        for review, sentiment in data:
            writer.writerow([review, sentiment])