from flask import Flask
app = Flask(__name__)

from flask import request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent, ImageSendMessage, LocationSendMessage, TemplateSendMessage, ButtonsTemplate, URITemplateAction, ConfirmTemplate, PostbackTemplateAction
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
        Signin(event)


    elif msg == '@課程列表':
        SendCurriculum(event) 

    elif msg == '@小幫手':
        SendTips(event)

    else:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = "蝦米?!"))

def SendCurriculum(event):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text = "2021/11/17\n基本安裝設定+Git使用\n課程連結:https://slides.com/sharonkuo/deck-c65f89\n\n2021/12/08\npython基礎語法\n課程連結:https://bit.ly/3FQfxLL\n\n2021/12/29\npython基本語法\n課程連結:https://bit.ly/3JBbFjY"))

def SendTips(event):
    message = TextSendMessage(
        text = '請選擇',
        quick_reply = QuickReply(
            items=[
                QuickReplyButton
                    (action=MessageAction(label="課表", text="@課表"))
        ])
    ) 
    line_bot_api.reply_message(event.reply_token, message)


    

if __name__ == '__main__':
    app.run()