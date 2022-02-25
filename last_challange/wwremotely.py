import requests
from bs4 import BeautifulSoup

# title, company, applyLink 추출하기
def extract_job(html):
    company = html.find("span",{"class":"company"})
    title = html.find("span",{"class":"title"})
    applyLink = html.find("a", recursive=0)["href"]

    if company and title and applyLink:
        company = company.text
        title = title.text
        applyLink = "https://weworkremotely.com/" + applyLink
        # print(applyLink)
        # print("========================================")

    return {'title':title, 'company':company, 'applyLink':applyLink}

def extract_jobs(URL):
    jobs = []

    wwr_req = requests.get(URL)  
    wwr_soup = BeautifulSoup(wwr_req.text,"html.parser")
    job_main = wwr_soup.find("div",{"class":"jobs-container"})
    job_set = job_main.find_all("li")
    
    for objt in job_set:
        job = extract_job(objt)
        jobs.append(job)
    
    return jobs

def get_wwr_jobs(word):
    URL = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={word}"
    jobs = extract_jobs(URL)
    #print(jobs)
    return jobs

#get_wwr_jobs("python")