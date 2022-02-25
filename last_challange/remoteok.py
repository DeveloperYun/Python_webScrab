import requests
from bs4 import BeautifulSoup

# 프로그램을 봇으로 인지해서 503을 띄워버리는 문제 발생
# 해결책 : user_Agent
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

# title, company, applyLink
def extract_job(html):
    company = html.find("h3",{"itemprop":"name"})
    title = html.find("h2",{"itemprop":"title"})
    applyLink = html.find("a",{"itemprop":"url"})["href"]

    if company and title and applyLink:
        company = company.text
        title = title.text
        applyLink = "https://remoteok.com"+applyLink
        
    return {'title':title, 'company':company, 'applyLink':applyLink}


def extract_jobs(URL):
    jobs = []

    rok_req = requests.get(URL, headers = headers)
    rok_soup = BeautifulSoup(rok_req.text,"html.parser")
    job_main = rok_soup.find("div",{"class":"container"})
    
    if job_main:
        job_set = job_main.find_all("tr",{"class":"job"})

        for res in job_set:
            job = extract_job(res)
            jobs.append(job)

        return jobs
    else:
        return


def get_reok_jobs(word):
    URL = f"https://remoteok.com/remote-{word}-jobs"
    jobs = extract_jobs(URL)
    #print(jobs)
    return jobs

#get_reok_jobs("python")