import requests
from bs4 import BeautifulSoup


def get_last_pages(URL):
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")

    # class : s-pagination 
    pagination = soup.find("div", {"class":"s-pagination"})
    pages = pagination.find_all('a')
    #last_page = pages[-2].text.strip()
    last_page = pages[-2].get_text(strip=True)

    return int(last_page)

def extract_job(html):
    title = html.find("h2",{"class":"mb4"}).find("a")["title"]
    
    # recursive=False 를 주면 span 안의 span까지 전부 가져오는 것을 방지할 수 있다.
    # 리스트 안에 두개의 item이 있다는 걸 아니까 아래와 같이 한 줄에 2개의 변수 선언해서 할당 가능.
    company, location = html.find("h3",{"class": "fc-black-700"}).find_all("span", recursive=0)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip(" • ")
    job_id = html['data-jobid']


    #print(company, location)

    return {'title': title,\
            'company': company, \
            'location': location, \
            'apply_link' : f"http://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page, URL):
    jobs = []

    # 최대 페이지 수 만큼 requests를 보내야 하므로 range를 사용.
    for page in range(last_page):
        result = requests.get(f"{URL}&pg={page+1}")

        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs(word):
    URL = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    last_pages = get_last_pages(URL)
    jobs = extract_jobs(last_pages, URL)
    return jobs
