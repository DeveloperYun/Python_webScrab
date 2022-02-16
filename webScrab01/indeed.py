import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
    result = requests.get(URL)
    #print(indeed_result.text)

    soup = BeautifulSoup(result.text, "html.parser")
    #print(indeed_soup)

    pagination = soup.find("div", {"class":"pagination"})
    #print(type(pagination))

    links = pagination.find_all('a')

    # 각 링크의 span 정보만 추출
    pages = []
    for link in links[0:-1]:
        pages.append(int(link.find("span").string)) # == pages.append(link.string)

    # 마지막 페이지 추출
    max_page = pages[-1]
    return max_page

def extract_job(html):
    titles = html.find("h2",{"class":"jobTitle"})
    title_info = titles.find("span",title=True).string
    
    company = html.find("span",{"class": "companyName"})
    company_anchor = company.find("a")

    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)

    location = html.find("div",{"class": "companyLocation"}).text
    job_id = html["data-jk"]
    #print(job_id)


    return {'title': title_info,'company': company, 'location': location, 'link': \
            f"https://www.indeed.com/viewjob?jk={job_id}"}

def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):

        print("Scrapping page " + str(page))

        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("a", {"class":"tapItem"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs