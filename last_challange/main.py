from flask import Flask, render_template, request, redirect, send_file
from wwremotely import get_wwr_jobs
from so import get_so_jobs
from remoteok import get_reok_jobs
from export_csv import save_to_file

app = Flask("FinalScrapper")

# fake db
db = {}

#integrated crawling data
def combined_data(word):
    data = []
    data1 = [] 
    data1 = get_wwr_jobs(word)

    data2 = []
    data2 = get_so_jobs(word)

    data3 = []
    data3 = get_reok_jobs(word)
    
    if data1:
        data += data1
    if data2:
        data += data2
    if data3:
        data += data3
    #print(data)
    #print(len(data))
    return data
    

@app.route("/") # / = root
def front():
    return render_template("front_page.html")

@app.route("/report")
def report():
    # url 에서 추출한 term 정보
    word = request.args.get('word')
    if word: # 아무것도 입력 안했을때 방지
        word = word.lower()
        existing_jobs = db.get(word)

        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = combined_data(word)
            db[word] = jobs
    else:
        return redirect("/")

    return render_template("final_report.html",search = word,\
                                               job_len=len(jobs),\
                                               jobs = jobs)


@app.route("/exportTo")
def exportTo():
    try:
        word = request.args.get('word')
        #print(word)
        if not word:
            raise Exception
        
        word = word.lower()
        jobs = db.get(word) #리스트(내부: 딕셔너리)
        #print(jobs) (동작o)
        if not jobs:
            raise Exception
            
        save_to_file(jobs,word)
        return send_file(f"{word}.csv")
    except:
        return redirect("/")

app.run()