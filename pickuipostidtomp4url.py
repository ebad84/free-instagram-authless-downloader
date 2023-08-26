import requests_html
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


ua = UserAgent()
req = requests_html.HTMLSession()
req.headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

# exit()

def item_to_result(item):
    result = list()
    video_link = re.findall(r"onclick=\"window\.open\('([^']{1,})'", item)
    img_link = re.findall(r"<img alt=\"tiny_stickers\" src=\"([^\"]{1,})\"", item)
    if video_link == []:
        result.append(img_link[0])
    else:
        result.append(video_link[0])
    return result

def postid_to_mediaurl(mediaid = 3162751668674872320):
    url = f"https://www.picuki.com/media/{mediaid}"
    pagecontent = req.get(url).text
    soup = BeautifulSoup(pagecontent, "html.parser")
    result = list()
    for item in soup.find_all("div", attrs={"class":"item"}):
        for i in item_to_result(str(item)):
            result.append(i)
    if result == []:
        result = item_to_result(pagecontent)
    return result

print(postid_to_mediaurl(3176415747541347924))