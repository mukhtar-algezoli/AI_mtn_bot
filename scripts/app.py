"""
This bot listens to port 5002 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
import ast
from flask import Flask, request
from pymessenger.bot import Bot
# from classify import *
from similarity import *
import difflib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from templates import *
from crud import get_option
from crud import Database
app = Flask(__name__)

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

ACCESS_TOKEN = "EAAHIn6fRZCSkBAHW3qLJQ7RFRZCZBieyZBMtJT24MJ2O1TXPrmRDWBSaLs5nAlsuP0fyYbe8Qz3dmmuI2MuKThOZCXff7NZAh5P4ikZAZBReS1Ocj9kqP71JYYYqWp2sUDonj3YxV9ou4nBfPoSb4LwpLlgZBwBHwhzppn09enmCwhaOtHNAtFGp5"
VERIFY_TOKEN = "verify"
bot = Bot(ACCESS_TOKEN)
matches = ["داتا", "واي فاي", "فور جي", "g4"]
message = None
recipient_id = None
old_rep = None
wifi_message = """واي _فاي B315s-22 يغطي مساحة 50 متر ويدعم 32 مستخدم بسرعة تصل إلى 150 ميقابايت في الثانية ، سعر الجهاز 6115 جنية
ماي _فاي E5573 يغطي مساحة 15 متر ويدعم 10 مستخدمين بسرعة تصل إلى 42 ميقابايت في الثانية """
offers_4g_message = """ عـــــــروض ال 4G
500 ميغابايت ل10 يوم بقيمه  60.31 جنيه  #500*123*
1 قيقا بايت لشهر بقيمة 140.25 جنيه #1024*123*
 3 قيقا بايت لشهر  بقيمه 322.58  جنيه *123*3072#
 5 قيقا  بايت لشهر بقيمة  591.86 جنيه #5120*123*
 10 قيقا بايت لشهر بقيمة 823.27  جنيه #10240*123*
 20 قيقا بايت  لشهر بقيمة 1151.45 جنيه #20480*123*
 50 قيقا بايت لشهر بقيمه  2467 جنيه  #51*123*
 100 قيقا بايت لشهر بقيمه 3704  جنيه  #100*123*"""

data_sim_offers = """باقات  الانترنت لشرائح  البيانات دفع  الاجل
 يمكنك الحصول علي شريحة بيانات دفع اجل بزيارة اقرب مركز خدمة واحضار اثبات هوية ساري المفعول ومبلغ  التامين  الخاص بكل باقه علما بانه يتم اضافه  قيمه  العرض علي  الفاتوره النهائيه لكل شهر والتامين قيمه مسترده عند ايقاف الخدمه او التعامل بعد سداد الفواتير .
 الباقة  الشهرية العاديه   بقيمة 350.63 جنيه ومبلغ تامين235 جنيه
 الباقة الذهبية الشهرية  بقيمة 518.93جنيه ومبلغ تامين360جنيه
 الباقة البلاتينية الشهرية  بقيمة 631.13 جنيه ومبلغ تامين430 جنيه
 الباقة البلاتينية + بقيمه 1009.8جنيه ومبلغ تامين725 جنيه
 الباقة البلاتينية ++  بقيمه 1542.75 جنيه ومبلغ تامين 1110 جنيه
 الباقه البلاتينه ل6 اشهر 890.5جنيه ومبلغ تامين 725 جنيه
 الباقه البلاتينه ل12 شهر بقيمه 1644 جنيه ومبلغ تامين 1200 جنيه"""




def send_messages( messages):
        if recipient_id != 123456789:
           bot.send_action(recipient_id, "typing_on")
           for message in messages:
                if recipient_id != 123456789:
                     result = bot.send_message(recipient_id, message)
                     print(result)
                else:
                     pass
def show_option(db: Database, option_id):
        option = get_option(db, option_id)
        messages = None
        if option.type == 'menu':
                messages = menu(db,option)
        elif option.type == 'info':
                messages = info(db,option)
        if messages is not None:
          result =  send_messages( messages)

def fun(sentiment):
    if sentiment == 0:
        return 'data_offer'
    elif sentiment == 1:
        return 'voice_offers'
    elif sentiment == 2:
        return 'complaint'
    elif sentiment == 3:
        return 'service_centers'
    elif sentiment == 4:
        return 'my_sim'
    else:
        return 'nothing'


def data_offer():
    db = firestore.client()
    go_to_similarity = True
    for word in matches:
        search_in = message.split()
        matches_output = difflib.get_close_matches(word, search_in, cutoff=0.6)
        if matches_output:
            go_to_similarity = False
           # if word == matches[0]:
           #     bot.send_text_message(recipient_id, data_sim_offers)

            if word == matches[1]:
                bot.send_text_message(recipient_id, wifi_message)

            elif word == matches[2]:
                bot.send_text_message(recipient_id, offers_4g_message)

            elif word == matches[3]:

                bot.send_text_message(recipient_id, offers_4g_message)
    if go_to_similarity:
        db = firestore.client()
        similarity_output, k, sim = compare_sim(message)

        #bot.send_text_message(recipient_id, similarity_output)
        print(similarity_output)
        goto = get_doc_goto_with_sim_txt(db,'data_offer',sim) 
        show_option(db, goto)

    return


def voice_offers():
    db = firestore.client()
    similarity_output, k, sim = compare_sim(message)
    #print(fun(k))
    #bot.send_text_message(recipient_id, similarity_output)
    print(similarity_output)
    goto = get_doc_goto_with_sim_txt(db,'voice_offers',sim)
    show_option(db, goto)
    return


def complaint():
    db = firestore.client()
    similarity_output, k, sim = compare_sim(message)
    #bot.send_text_message(recipient_id, similarity_output)
    print(similarity_output)
    goto = get_doc_goto_with_sim_txt(db,'complaints',sim)
    show_option(db, goto)
    return


def my_sim():
    db = firestore.client()
    similarity_output, k, sim = compare_sim(message)
    #bot.send_text_message(recipient_id, similarity_output)
    print(similarity_output)
    goto = get_doc_goto_with_sim_txt(db,'my_sim',sim)
    show_option(db, goto)
    return


def service_centers():
    db = firestore.client()
    similarity_output, k, sim = compare_sim(message)
    #bot.send_text_message(recipient_id, similarity_output)
    print(similarity_output)
    goto = get_doc_goto_with_sim_txt(db,'service_centers',sim)
    show_option(db, goto)
    return


def others():
    bot.send_text_message(recipient_id, "الرجاء توضيح  الاستفسار للإفادة")
    return


@app.route("/message", methods=['GET', 'POST'])
def hello():
    global message
    global old_rep
    global recipient_id
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            #if messaging.postback is not None:
            #  print(True)
            #else:
            #  print(False)
           # print(messaging)

            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    bot.send_action(recipient_id, 'mark_seen')
                    if x['message'].get('text'):
                        message = x['message']['text']
                        if old_rep == message:
                            print("duplicated message")
                            return "Success"
                        else:
                            old_rep = message
                       # classify_output = classify_input(message)
                        similarity_output, k, sim = compare_classify(message)
                        classify_output = fun(k)
                       # bot.send_text_message(recipient_id, classify_output)
                        eval(classify_output+"()")
                else:
                    if x.get('postback'):
                       y = x.get('postback').get('payload') 
                       if old_rep == y:
                           print("dublicated message")
                           return "Success"
                       else:
                           old_rep = y
                       y =  ast.literal_eval(y)
                       option_id = y.get("option_id")
                       next_option_id = get_next_option_with_option_id(db,option_id)
                       show_option(db, next_option_id)
                       
                    pass
        return "Success"


if __name__ == "__main__":
   # load_classification_model()
   # print("loading similarity model")
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': "serious-cabinet-282523",
    })

    db = firestore.client()
    load_model('../Similarity/')
    print("loading similarity data")
    load_data('../labeled_data/mtn_data_labeled.csv')
    print("processing similarity data")
    cal_embeddings_classify()
    cal_embeddings_sim(db)
    print("finished processing")
    print("ready for input")
    app.run(port=5002, debug=True,use_reloader=False)
