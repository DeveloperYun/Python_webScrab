import requests
import csv
import os
from bs4 import BeautifulSoup

os.system('cls')
URL = "https://movie.naver.com/movie/sdb/rank/rmovie.naver"
movie_data = {}

def get_info(URL):
    movie_req = requests.get(URL)
    movie_soup = BeautifulSoup(movie_req.text,"html.parser")
    rankData = movie_soup.find("table",{"class":"list_ranking"})
    movies = rankData.find_all("tr")

    return movies

def save_to_file(movies):       # movies = 딕셔너리
    file = open("movies.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["제목","랭크","장르", "감독", "배우"])
    qdata = list(movies.values())
    
    for data in qdata:
        writer.writerow([data["title"],data["rank"],data["genre"],data["director"],data["actors"]])
        
    
def extract_data(movies):
    rank = 0
    global movie_data
    # 딕셔너리가 유지가 안되고 덮어씌워지는 에러 발생
    for movie in movies:
        title = movie.find("div",{"class":"tit3"})
        link = movie.find("div",{"class":"tit3"})

        if title and link:
            title = title.find("a")["title"]
            link = "https://movie.naver.com/"+link.find("a")["href"]
            
            # 개별 영화에 대한 정보
            data_req = requests.get(link)
            data_soup = BeautifulSoup(data_req.text, "html.parser")
            # 개요, 감독, 출연, 등급, 흥행 정보
            data_info = data_soup.select("dl.info_spec dd")

            rank = rank + 1
            genre = data_info[0].select_one("a").text
            director = data_info[1].select_one("a").text
            actors = data_info[2].select_one("a").text

            info = {
                    "title":title,
                    "rank":rank,
                    "genre":genre,
                    "director":director,
                    "actors":actors
                    }

            movie_data[title] = info
            # print("title : ",title)
            # print("rank  : ",rank)
            # print("genre : ",genre)
            # print("dir   : ",director)
            # print("actors: ",actors)
            # print("==============================")
    return movie_data

if __name__=="__main__":
    movies = get_info(URL)
    movie_gift = extract_data(movies)
    save_to_file(movie_gift)
