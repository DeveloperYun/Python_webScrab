import csv

def save_to_file(jobs):
    file = open("jobs.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    for job in jobs:
        writer.writerow(list(job.values())) # 딕셔너리라서 이런 접근이 가능.
    return