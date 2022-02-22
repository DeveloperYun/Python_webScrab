from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from export_csv import save_to_file

app = Flask("SuperScrapper")

# 임시 데이터베이스
db = {}

@app.route("/") # / = root
def hello():
    return render_template("potato.html")

@app.route("/report")
def report():
    # URL에서 입력한 것을 추출한다. ?뒤의 word에 해당하는 부분.
    word = request.args.get('word')

    # 유저가 아무것도 입력 안했을땐 word가 None이 된다.
    if word:
        word = word.lower() # 대문자로 입력해도 소문자로 바꿔서 정정
        existing_jobs = db.get(word) # word가 DB에 있는지 탐색 중...

        if existing_jobs: # 만약 db에 해당 word가 존재한다면
            jobs = existing_jobs
        else: # 해당 word가 db에 없다면
            jobs = get_jobs(word) # scrapper가 돌아가며 정보를 scrap
            db[word] = jobs # 정보를 db에 저장
    else:
        # 이 때는 홈으로 redirect 시켜준다.
        return redirect("/")
    
    # word와 job의 개수도 변수로 넘겨준다.
    return render_template("report.html",sesBy=word,\
                                         resultsNumber=len(jobs),\
                                         jobs=jobs)

@app.route("/export")
def export():
    # try block에서 어떤 종류의 에러든 일어나면 except 로 처리
    try:
        word = request.args.get('word')
        if not word: # word가 없다면 예외처리
            raise Exception

        word = word.lower()
        jobs = db.get(word)

        if not jobs: # jobs가 db에 없다면 예외처리
            raise Exception
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/") # 홈으로 redirect

app.run()