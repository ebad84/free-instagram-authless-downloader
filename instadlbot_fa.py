import requests_html
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from instalibs import *

from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import time, os, json
from datetime import datetime, timedelta


# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = ''
BOTUSERNAME = ""

database : dict = {
    "admins":[""],
    "users": {
        "id":{
            "username":"username",
            "dlcount":int(),
            "lastdl":{"time":"seconds", "url":"http://url.com", "username":"username"}
        }
    },
    "downloads":{
        "yyyy-mm-dd":{
            "dlcount":int()
        }
    },
    "lastdl":{"time":"seconds", "url":"http://url.com", "username":"username"},
    "dlcount":int(),
    "sponsor-channels":[]
}
dbname = "database.json"
if dbname not in os.listdir():
    open(dbname, "w", encoding="utf-8").write(json.dumps(database, indent=4))
else:
    try:
        loadeddb = eval(open(dbname, "r", encoding="utf-8").read())
        database = loadeddb
    except:
        open(str(time.time())+ "_" + dbname, "w", encoding="utf-8").write(open(dbname, "r", encoding="utf-8").read())
        open(dbname, "w", encoding="utf-8").write(json.dumps(database, indent=4))


# def start(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /start is issued."""
#     user = update.effective_user
#     update.message.reply_markdown_v2(
#         fr'Hi {user.mention_markdown_v2()}\!',
#         reply_markup=ForceReply(selective=True),
#     )


# def help_command(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')


def handeltext(update: Update, context: CallbackContext) -> None:
    global database
    message = update.message.reply_text("درحال پردازش درخواست شما...")
    # update.message.reply_text(update.message.text)
    text = update.message.text
    # update.message.reply_text("getting media info")
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    is_admin = str(user_id) in database["admins"] or user_name in database["admins"] or "@"+user_name in database["admins"]
    chats_not_joined_yet = []
    today = datetime.today().strftime('%Y-%m-%d')
    time_now = datetime.now()
    if today not in database["downloads"]:
        database['downloads'][today] = {
            "dlcount":0
        }
    for chat_id in database["sponsor-channels"]:
        try:
            # print(context.bot.getChatMember(chat_id,user_id))
            # print(context.bot.getChatMember(chat_id,user_id).is_member)
            # print(context.bot.getChatMember(chat_id,user_id).is_anonymous)
            # print(context.bot.getChatMember(chat_id,user_id).MEMBER)
            if context.bot.getChatMember(chat_id,user_id).status == "left":
                chats_not_joined_yet.append(chat_id)
        except Exception as e:
            # print(e)
            pass
    # print(chats_not_joined_yet)
    if text == "/ping":
        result = f"""pong\n\n{update.message.from_user.id}\n{update.message.from_user.username}"""
        message.edit_text(result)
        return
    

    if not is_admin and len(chats_not_joined_yet) != 0:
        # should join in channels
        keyboard = [[InlineKeyboardButton(text = "بزن روش بجوین توش✅", url='https://t.me/'+channellink.replace("@", "").replace("https://t.me/", "").replace("http://t.me/", ""))] for channellink in chats_not_joined_yet]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # print(reply_markup)
        message.edit_text("هنوز تو این کانالا جوین نشدی! اول جوین این کانالا بشو : \n"+"\n".join(chats_not_joined_yet)+"\بعد اینو بزن : /start", reply_markup=reply_markup)
        return
    
    if (is_admin or str(user_id) == "651560594") and text.startswith("/"):
        if text == "/admins":
            update.message.reply_text(str(database["admins"]))
        elif text == "/start":
            update.message.reply_text("باح سلام ادمین گل. یه لینک برام بفرست که واستون دانلودش کنم، یا اینکه مدیریتم کن UWU\nمیتونی از کامند /help استفاده کنی")
        elif text == "/help":
            result = """🟩/admins \nکل ادمینارو نشون میده\n\n🟩/newadmin [Username/UserID]\nیه ادمین جدید اضافه کن\n\n🟩/removeadmin [Username/UserID]\nیه ادمینو بحذف
\n🟩/sponsors\nکانالای اسپانسر رو میتونی اینجا ببینی\n\n🟩/addsponsor [Username/ChannelID/ChannelPrivateLink]\nیه کانال اسپانسر جدید اضافه کن\n\n🟩/removesponsor [Username/ChannelID/ChannelPrivateLink]\nاسپانسر رو حذفش کن! نخوندم
\n🟩/dlcount\nکل تعداد دانلودای بات تا الان رو نشون بده\n\n🟩/lastdl\nآخرین لینکی که برا بات فرستاده شده چی بوده؟\n\n🟩/todaydlcount\nامروز چند تا دانلود داشتیم؟\n\n🟩/thisweekdlcount\n این هفته چقد دانلود داشتیم؟\n\n🟩/users\n کل کاربرایی که تا الان از بات استفاده کردن رو لیست کن. اول یوزر آیدیه بعد یوزرنیم بعد تعداد دانلودش  [یوزر آیدی-یوزرنیم-تعداد دانلود]
\n🟩/pubmsg\nپیام سراسری ارسال کن"""
            update.message.reply_text(result)
        elif text.startswith("/newadmin"):
            if text.replace("/newadmin", "") == "":
                update.message.reply_text("/newadmin AdminID")
            else:
                adminID = text.split(" ")[-1]
                if adminID in database["admins"]:
                    update.message.reply_text("این ادمین همین حالاشم موجوده")
                else:
                    database["admins"].append(adminID)
                    update.message.reply_text("done")
        elif text.startswith("/removeadmin"):
            if text.replace("/removeadmin", "") == "":
                update.message.reply_text("/removeadmin AdminID")
            else:
                adminID = text.split(" ")[-1]
                if adminID not in database["admins"]:
                    update.message.reply_text("این جزو ادمینایی که اد شدن نیست")
                elif adminID == user_name or adminID == str(user_id) or "@"+adminID == user_name:
                    update.message.reply_text("شما نمیتونی خودتو حذف کنی")
                else:
                    database["admins"].remove(adminID)
                    update.message.reply_text("done")
        elif text == "/sponsors":
            update.message.reply_text(str(database["sponsor-channels"]))
        elif text.startswith("/addsponsor"):
            if text.replace("/addsponsor", "") == "":
                update.message.reply_text("/addsponsor channelID")
            else:
                channelID = text.split(" ")[-1]
                if channelID in database["sponsor-channels"]:
                    update.message.reply_text("این اسپانسر همین حالاشم موجوده")
                else:
                    try:
                        update.message.reply_text(str(context.bot.getChatMember(channelID, context.bot.id)))
                        database["sponsor-channels"].append(channelID)
                        update.message.reply_text("done")
                    except Exception as e:
                        update.message.reply_text("اول منو به چنل یا گروه مدنظر اضافه کن، بعد پرمیشن ادمین بهم بده. نهایتا دوباره همین کامند رو بزن")
                        update.message.reply_text(str(e))
        elif text.startswith("/removesponsor"):
            if text.replace("/removesponsor", "") == "":
                update.message.reply_text("/removesponsor channelID")
            else:
                channelID = text.split(" ")[-1]
                if channelID not in database["sponsor-channels"]:
                    update.message.reply_text("این اصلا جزو اسپانسرا نیست. احتمالا اشتباه تایپی داری")
                else:
                    database["sponsor-channels"].remove(channelID)
                    update.message.reply_text("done")
        elif text == "/dlcount":
            update.message.reply_text(str(database["dlcount"]))
        elif text == "/lastdl":
            update.message.reply_text(str(database["lastdl"]))
        elif text == "/users":
            result = """"""
            for uid in database["users"]:
                result += f"{uid} {database['users'][uid]['username']} : {database['users'][uid]['dlcount']}\n"
                if len(result.split("\n")) == "100":
                    update.message.reply_text(result)
                    result = """"""
            if result != """""":
                update.message.reply_text(result)
        elif text == "/todaydlcount":
            update.message.reply_text(database['downloads'][today]["dlcount"])
        elif text == "/thisweekdlcount":
            sum_week = 0
            sum_week += database['downloads'][today]["dlcount"]
            for i in range(7):
                the_day = time_now - timedelta(seconds=86400)
                if the_day in database["downloads"]:
                    sum_week += database[the_day]["dlcount"]
        elif text.startswith("/pubmsg"):
            if text.replace("/pubmsg", "").replace("\n", "").replace(" ", "") == "":
                update.message.reply_text("شما یه پیام خالی رو نمیتونین ارسال کنین! توی خط اول کامند رو بنویسید و از خط دوم به بعد پیامتون رو بنویسید. مثال براتون ارسال میشه")
                update.message.reply_text("/pubmsg\nسلام!\nاین یه پیام سراسریه!!")
            else:
                update.message.reply_text("درحال ارسال پیام به همه یوزر ها... لطفا منتظر باشید.")
                countsent = 0
                for u in database["users"]:
                    try:
                        context.bot.send_message(chat_id=u, text=text.replace("/pubmsg\n", "").replace("/pubmsg", ""))
                        time.sleep(1)
                        countsent += 1
                    except:
                        pass
                update.message.reply_text("پیام به همه ارسال شد!! تعداد پیام ارسال شده : "+str(countsent))
        else:
            update.message.reply_text("کامند موجود نیست")

    else:
        if text == "/start":
            keyboard = [
                [
                    InlineKeyboardButton("😎دانلود پست", callback_data='post'),
                    InlineKeyboardButton("دانلود استوری😍", callback_data='story'),
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            message.edit_text("سلام! از تو به یک اشاره، از من به سر دویدن. میخوای چو کنی؟?!😈", reply_markup=reply_markup)
        else:
            for i in range(3):
                try:
                    result : str = instagram_media_url_to_links(text)
                    break
                except:
                    pass
            else:
                message.edit_text("یه مشکلی پیش اومده. یکم بعدا دوباره امتحان کن")
                return
            if type(result) == str:
                if result == "URLERR":
                    message.edit_text("""لینکی که میفرستی درست نیستتتتت! چند تا مثال این زیره باید شبیه اینا باشه :
                🟢story : https://www.instagram.com/stories/kourosh.zz/3179885446141608484/
                🟢post  : https://www.instagram.com/p/CvP7AnBNnDS/
                🟢reel  : https://www.instagram.com/reel/CvP7AnBNnDS/""")
                elif result.startswith("Error : "):
                    update.message.reply_text(result)
                    message.edit_text("به یه ارور خفن برخوردیم. اول ارور رو برا ادمین بفرست، یکم بعد تر دوباره امتحان کن.")
            else:
                message.edit_text("تموم شد. اینم چیزایی که خواسته بودی :)")
                # print(result)
                # exit()
                for i in result:
                    print(i)
                    try:
                        if ".mp4" in i:
                            update.message.reply_video(i)
                        elif ".jpeg" in i:
                            update.message.reply_photo(i)
                        else:
                            update.message.reply_document(i)
                    except:
                        update.message.reply_text(i)
                if user_id not in database["users"]:
                    database["users"][user_id] = {
                        "username":user_name,
                        "dlcount":1,
                        "lastdl":{"time":time.time(), "url":text, "username":user_name}
                    }
                else:
                    database["users"][user_id]["dlcount"] += 1
                    database["users"][user_id]["lastdl"]["time"] = time.time()
                    database["users"][user_id]["lastdl"]["url"] = text
                    database["lastdl"] = {"time":time.time(), "url":text, "username":user_name}
                    if today not in database["downloads"]:
                        database['downloads'][today]["dlcount"] = 1
                    else:
                        database['downloads'][today]["dlcount"] += 1
                    database['dlcount'] += 1

    # except Exception as e:
    #     update.message.reply_text("error : "+str(e))

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    text = ""
    if query.data == "post":
        text = "لینکتو بفرست.\nدقت کن باید لینکت مال پست و یه چیزی شبیه این باشه :\n 🟢 https://www.instagram.com/p/CvP7AnBNnDS/"
    elif query.data == "story":
        text = "لینکتو بفرست.\nدقت کن باید لینکت مال استوری و یه چیزی شبیه این باشه :\n 🟢 https://www.instagram.com/stories/kourosh.zz/3179885446141608484/"
    query.edit_message_text(text=text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, handeltext))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()
    while True:
        open(dbname, "w", encoding="utf-8").write(json.dumps(database, indent=4))
        time.sleep(2)


if __name__ == '__main__':
    main()