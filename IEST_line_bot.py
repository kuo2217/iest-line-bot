from flask import Flask
app = Flask(__name__)

from flask import request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
from urllib.parse import parse_qsl


line_bot_api = LineBotApi('8W2UAPtMfugubbs4TqODw6NOr2gjYHDtCKFXs0ncecIpw0o0ye+qw12Ja9FjJEHMl7TZ1tzQa5eJd5GWEb4lKcHBMxjZKKhHZ84BD+559+yHALORGVpDAzfXxPkIkZBMUZZ5mTzcf+PTfCgwIF5zqwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('985d3775c70fb588d7846e2b89e1f796')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg == '@關於我們':
        AboutUs(event)

    elif msg == '@簽到':
        SignIn(event)


    elif msg == '@課程列表':
        SendCurriculum(event) 

    elif msg == '@小幫手':
        SendHelper(event)
    
    elif msg == 'IEST':
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = "歡迎光臨資訊教育服務隊"))

    else:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = "蝦米?!"))

def SendCurriculum(event):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text = "2021/11/17\n基本安裝設定+Git使用\n課程連結:https://slides.com/sharonkuo/deck-c65f89\n\n2021/12/08\npython基礎語法\n課程連結:https://bit.ly/3FQfxLL\n\n2021/12/29\npython基本語法\n課程連結:https://bit.ly/3JBbFjY"))

def SendHelper(event): #按鈕樣板
    try:
        message = TemplateSendMessage(
            alt_text='helper',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/LhQ69eh.png',  #顯示的圖片
                title='小幫手',  #主標題
                text='請選擇：',  #副標題
                actions=[
                    URITemplateAction(  #開啟網頁
                        label='圖資課表(上學期)',
                        uri='http://web.lins.fju.edu.tw/upload/dep/course/dep-course110_1_0831.pdf'
                    ),
                    URITemplateAction(  #開啟網頁
                        label='圖資課表(下學期)',
                        uri='http://web.lins.fju.edu.tw/upload/dep/course/dep-course110_2_0831.pdf'
                    ),
                    URITemplateAction(  #開啟網頁
                        label='聯絡我們',
                        uri='https://www.facebook.com/fjulis.IEST'
                    ),
                    URITemplateAction(  #開啟網頁
                        label='加入我們',
                        uri='http://line.me/ti/g/z9QufTl4pX'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def AboutUs(event):
    try:
        message = TemplateSendMessage(
            alt_text='aboutus',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/mUOauOd.png',
                        action=MessageTemplateAction(
                            label='IEST',
                            text='IEST'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/SjtgCS7.png',
                        action=MessageTemplateAction(
                            label='IEST',
                            text='IEST'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/4LqLit8.png',
                        action=MessageTemplateAction(
                            label='IEST',
                            text='IEST'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/X2Qb3Aq.png',
                        action=MessageTemplateAction(
                            label='IEST',
                            text='IEST'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/AVaLRWs.png',
                        action=MessageTemplateAction(
                            label='IEST',
                            text='IEST'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/g62b7HG.png',
                        action=MessageTemplateAction(
                            label='IEST',
                            text='IEST'
                        )
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))    
    

if __name__ == '__main__':
    app.run()