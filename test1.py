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

charmap = {
    'A': '0',
    'B': '1',
    'C': '2',
    'D': '3',
    'E': '4',
    'F': '5',
    'G': '6',
    'H': '7',
    'I': '8',
    'J': '9',
    'K': 'a',
    'L': 'b',
    'M': 'c',
    'N': 'd',
    'O': 'e',
    'P': 'f',
    'Q': 'g',
    'R': 'h',
    'S': 'i',
    'T': 'j',
    'U': 'k',
    'V': 'l',
    'W': 'm',
    'X': 'n',
    'Y': 'o',
    'Z': 'p',
    'a': 'q',
    'b': 'r',
    'c': 's',
    'd': 't',
    'e': 'u',
    'f': 'v',
    'g': 'w',
    'h': 'x',
    'i': 'y',
    'j': 'z',
    'k': 'A',
    'l': 'B',
    'm': 'C',
    'n': 'D',
    'o': 'E',
    'p': 'F',
    'q': 'G',
    'r': 'H',
    's': 'I',
    't': 'J',
    'u': 'K',
    'v': 'L',
    'w': 'M',
    'x': 'N',
    'y': 'O',
    'z': 'P',
    '0': 'Q',
    '1': 'R',
    '2': 'S',
    '3': 'T',
    '4': 'U',
    '5': 'V',
    '6': 'W',
    '7': 'X',
    '8': 'Y',
    '9': 'Z',
    '-': '$',
    '_': '_'
}

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


from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = ''

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    # update.message.reply_text(update.message.text)
    text = update.message.text
    update.message.reply_text("getting post info")
    # try:
    mediaid = instagram_url_to_media_id(text)
    result = postid_to_mediaurl(mediaid)
    update.message.reply_text("uploading results for you :)")
    for i in result:
        if ".mp4" in i:
            update.message.reply_video(i)
        elif ".jpeg" in i:
            update.message.reply_photo(i)
        else:
            update.message.reply_document(i)
    # except Exception as e:
    #     update.message.reply_text("error : "+str(e))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()