import requests
import csv
import os
from bs4 import BeautifulSoup

os.system('cls')
URL = "http://www.alba.co.kr/"
count = 0

def get_alba_info(URL):
    alba_req = requests.get(URL)
    alba_soup = BeautifulSoup(alba_req.text, "html.parser")
    main = alba_soup.find("div",{"id":"MainSuperBrand"})
    brands = main.find_all("li",{"class":"impact"})

    return brands

# csv로 변환
def save_file(company):
    global count
    file = open(f"{company['name']}.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["place","title","time","pay","date"])

    for job in company['jobs']:
        writer.writerow(list(job.values()))
    count += 1
    print(f"complete({count}) : {company['name']}")

# place, title, time, pay, date
def extract_brand(brands):
    for brand in brands:
        link = brand.find("a",{"class":"goodsBox-info"}) # 지원링크(이걸 타고가야함)
        name = brand.find("span",{"class":"company"}) # 회사명

        if link and name: # 링크와 회사가 둘다 존재한다면 (빈 배너 방지용)
            link = link["href"] # 링크 정보 추출
            name = name.text    # 회사 이름 추출

            # 특수문자 => .replace()
            if "/" in name:
                name = name.replace("/"," ")
            
            # 슈퍼브랜드 링크 결과 스크랩
            company = {'name':name, 'jobs': []}

            # 회사 별로 requests 보내서 html 가져와야함.
            job_requests = requests.get(link)
            job_soup = BeautifulSoup(job_requests.text, "html.parser")
            job_info = job_soup.find("div",{"id":"NormalInfo"})
            job = job_info.find("tbody")

            rows = job.find_all("tr",{"class":""})

            for row in rows:
                place = row.find("td",{"class":"local"})
                if place:
                    place = place.text

                title = row.find("td",{"class":"title"})
                if title:
                    title = title.find("a").find("span",{"class":"company"}).text.strip()

                time = row.find("td",{"class":"data"})
                if time:
                    time = time.text

                pay = row.find("td",{"class":"pay"})
                if pay:
                    pay = pay.text

                date = row.find("td",{"class":"regDate"})
                if date:
                    date = date.text

                job = {"place":place,
                    "title":title,
                    "time":time,
                    "pay":pay,
                    "date":date
                    }
                company["jobs"].append(job)

            save_file(company)

if __name__=="__main__":
    brands = get_alba_info(URL)
    extract_brand(brands)