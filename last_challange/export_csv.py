import csv

# jobs = 리스트
def save_to_file(jobs,word):
    file = open(f"{word}.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Link"])

    for job in jobs:
        writer.writerow(list(job.values()))
    return