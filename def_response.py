import json
import requests
from bs4 import BeautifulSoup
from core.config import URL, DOMEN, HEADERS

def get_response(url_def, headers_def=HEADERS):      
    # function to get response from server
    response = requests.get(url=url_def, headers=headers_def) # get response from server
    if response.status_code == 200:     # response status  
        src = response.content          # response content from  server
        return src                      # return response
    else:
        return f"bad response {response.status_code}"

def get_soup(response):
    # function to get soup from response
    soup = BeautifulSoup(response, 'html.parser')
    all_news = soup.find_all("div", class_="tn-news-author-list-item")
    
    news_info = []
    for item in all_news:
        try:
            title = item.find("div", class_="tn-news-author-list-item-text").find("span", class_="tn-news-author-list-title")
            description = item.find("div", class_="tn-news-author-list-item-text").find("p", class_="tn-announce")
            date_time = item.find("div", class_="tn-news-author-list-item-text").find("li")
            news_url = DOMEN + item.find("a").get("href")
            image = item.find("div", class_="tn-image-container").find("img").get("src")
        except Exception: # if exception happens during the creation of the image element code above    then the        image element will be    removed from the DOM
            image = item.find("div", class_="tn-video-container").find("source").get("src")
            information = {
            "title": title.text,
            "description": description.text,
            "date_time": date_time.text.strip(),
            "image": DOMEN + image,
            "url": news_url
            }
        else:
            information = {
            "title": title.text,
            "description": description.text,
            "date_time": date_time.text.strip(),
            "image": DOMEN + image,
            "url": news_url
            }
        news_info.append(information)
    return news_info

def parser():
    response = get_response(url_def=URL)
    soup = get_soup(response)
    
    with open(f"core/json/tengrinews.json", "w", encoding="UTF-8") as file:
        json.dump(soup, file, indent=4, ensure_ascii=False)

parser()




