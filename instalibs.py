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
charmap = {
    'A': '0','B': '1','C': '2','D': '3','E': '4','F': '5','G': '6','H': '7','I': '8','J': '9','K': 'a','L': 'b','M': 'c','N': 'd','O': 'e','P': 'f','Q': 'g','R': 'h','S': 'i','T': 'j','U': 'k','V': 'l','W': 'm','X': 'n','Y': 'o','Z': 'p','a': 'q','b': 'r','c': 's','d': 't','e': 'u','f': 'v','g': 'w','h': 'x','i': 'y','j': 'z','k': 'A','l': 'B','m': 'C','n': 'D','o': 'E','p': 'F','q': 'G','r': 'H','s': 'I','t': 'J','u': 'K','v': 'L','w': 'M','x': 'N','y': 'O','z': 'P','0': 'Q','1': 'R','2': 'S','3': 'T','4': 'U','5': 'V','6': 'W','7': 'X','8': 'Y','9': 'Z','-': '$','_': '_'
}

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
    print(url)
    pagecontent = req.get(url).text
    soup = BeautifulSoup(pagecontent, "html.parser")
    result = list()
    for item in soup.find_all("div", attrs={"class":"item"}):
        for i in item_to_result(str(item)):
            result.append(i)
    if result == []:
        result = item_to_result(pagecontent)
    return result

def storylink_to_output(link):
    url = f"https://igram.world/api/ig/story?url={link}"
    res = req.get(url).json()
    # print(res)
    try:
        videos = res["result"][0]["video_versions"]
    except:
        videos = [res["result"][0]["image_versions2"]["candidates"][0]]
    # print(res)
    return videos

def instagram_url_to_media_id(url):
    # code = "B8iwlG9pXHI"
    id = ""
    code = url.split("p/")[-1].replace("/", "")
    print(code)
    for letter in code:
        id += charmap[letter]
  
    alphabet = list(charmap.values())
    number = 0
    for char in id:
        number = number * 64 + alphabet.index(char)

    return number

def instagram_code_to_media_id(code):
    # code = "B8iwlG9pXHI"
    id = ""
    for letter in code:
        id += charmap[letter]
  
    alphabet = list(charmap.values())
    number = 0
    for char in id:
        number = number * 64 + alphabet.index(char)

    return number

def getInstagramUrlFromMediaId(media_id):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    shortened_id = ''

    while media_id > 0:
        remainder = media_id % 64
        # dual conversion sign gets the right ID for new posts
        media_id = (media_id - remainder) // 64;
        # remainder should be casted as an integer to avoid a type error. 
        shortened_id = alphabet[int(remainder)] + shortened_id

    return 'https://instagram.com/p/' + shortened_id + '/'


def instagram_media_url_to_links(url : str) -> list:
    url = url.replace("https://", "").replace("http://", "").replace("www.instagram.com", "instagram.com")
    if url.startswith("instagram.com/stories/"):
        videos = storylink_to_output(url)
        result = [i["url"] for i in videos]
    elif url.startswith("instagram.com/p/") or url.startswith("instagram.com/reel/"):
        code = re.findall(r"instagram\.com\/(?:p|reel|[^\/]{1,})\/([^\/\?]{1,})", url)[0]
        mediaid = instagram_code_to_media_id(code)
        result = postid_to_mediaurl(mediaid)
    else:
        result = "URLERR"


    return result