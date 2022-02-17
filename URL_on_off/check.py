import os
import requests

def hello_ment():
    print("Welcome to IsItDown.py!")
    print("Please write a URL or URLs you wnat to check. (separated by comma)")

def restart():
    ans = str(input("Do you want to start over? y/n ")).lower()
    if ans == "y" or ans == "n":
        if ans == "y":
            main()
        elif ans == "n":
            print("k. bye!")
            return
    else:
        print("That's not a valid answer")
        restart()

def main():
    os.system('cls')
    hello_ment()
    
    url = []
    urlSet = input().lower().split(",")
    #print(urlSet)
    for urls in urlSet:
        urls = urls.strip()
        url.append(urls)
    #print(url)
    # http:// 빠진 url에 붙여주기
    for i, item in enumerate(url):
        if item[0:7] != "http://":
            url[i] = "http://" + item

    # valid URL 검사
    for item in url:
        if "." not in item:
            print(item + " is not a valid URL.")
        else:
            try:
                r = requests.get(str(item))
                if r.status_code == 200:
                    print(item + " is up!")
                else:
                    print(item + " is down!")
            except:
                print(item + " is down!")

    restart()
            
if __name__=="__main__":
    main()