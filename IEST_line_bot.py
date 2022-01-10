from flask import Flask
from flask import request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
from urllib.parse import parse_qsl

app = Flask(__name__)
line_bot_api = LineBotApi('8W2UAPtMfugubbs4TqODw6NOr2gjYHDtCKFXs0ncecIpw0o0ye+qw12Ja9FjJEHMl7TZ1tzQa5eJd5GWEb4lKcHBMxjZKKhHZ84BD+559+yHALORGVpDAzfXxPkIkZBMUZZ5mTzcf+PTfCgwIF5zqwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('985d3775c70fb588d7846e2b89e1f796')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nghzkyrhisdvsf:c0ad142a2d4add238a03b5e80de731e985502bc435a78418229badd591075820@ec2-3-226-165-74.compute-1.amazonaws.com:5432/d8bkbshheajqlc'
db = SQLAlchemy(app)
liffid = '1656789911-bMzdgkjW'

#LIFF靜態頁面
@app.route('/page')
def page():
	return render_template('IESTsign.html', liffid = liffid)

# 重置資料庫
@app.route('/createdb')
def createdb():
    sql = """
    DROP TABLE IF EXISTS iestuser, sign;

    CREATE TABLE iestuser (
    id serial NOT NULL,
    uid character varying(50) NOT NULL,
    PRIMARY KEY (id));

    CREATE TABLE sign (
    id serial NOT NULL,
    bid character varying(50) NOT NULL,
    name character varying(20) NOT NULL,
    state character varying(20) NOT NULL,
    date character varying(50) NOT NULL,
    PRIMARY KEY (id))
    """
    db.engine.execute(sql)    
    return "資料表建立成功！"

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
    user_id = event.source.user_id
    sql_cmd = "select * from iestuser where uid='" + user_id + "'"
    query_data = db.engine.execute(sql_cmd)
    if len(list(query_data)) == 0:       
        sql_cmd = "insert into iestuser (uid) values('" + user_id + "');"
        db.engine.execute(sql_cmd)  


    msg = event.message.text
    if msg == '@關於我們':
        AboutUs(event)

    elif msg == '@簽到':
        SignIn(event, user_id)

    elif msg == '@課程列表':
        SendCurriculum(event) 

    elif msg == '@小幫手':
        SendHelper(event)
    
    elif msg == 'IEST':
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = "[┐∵]┘歡迎光臨資訊教育服務隊"))

    elif msg == '麻將':
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = "    🀙🀚🀛🀜🀝🀞🀟🀠🀡🀢🀣\n🀥    🀗🀐🀏🀎🀍🀌🀋🀊🀉   🀥\n🀖  🀗           🀙  🀥\n🀘  🀗           🀙  🀔\n🀕  🀡           🀁  🀁\n🀖  🀗           🀁  🀁\n🀘    🀎🀍🀌🀋🀊🀉🀇🀉🀇   🀁\n   🀐🀏🀎🀍🀌🀋🀊🀉🀇🀆🀅🀁"))

    elif msg[:3] == '###' and len(msg) > 3:  #處理LIFF傳回的FORM資料
        manageForm(event, msg, user_id)

    elif msg[:6] == '123456' and len(msg) > 6:  #推播給所有顧客
        pushMessage(event, msg)

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
    
def SignIn(event, user_id):  #簽到
    try:
        sql_cmd = "select * from sign where bid='" + user_id + "'"
        query_data = db.engine.execute(sql_cmd)
        message = TemplateSendMessage(
            alt_text = "簽到",
            template = ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/vzCuRFI.png',
                title='簽到表',
                text='請選擇',
                actions=[
                    URITemplateAction(label='簽到', uri='https://liff.line.me/' + liffid)  #開啟LIFF讓使用者輸入訂房資料
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def manageForm(event, msg, user_id):  #處理LIFF傳回的FORM資料
    try:
        flist = msg[3:].split('/')  #去除前三個「#」字元再分解字串
        name = flist[0]  #取得輸入資料
        state = flist[1]
        date = flist[2]
        sql_cmd = "insert into sign (bid, name, state, date) values('" + user_id + "', '" + name + "', '" + state + "', '" + date + "');"
        db.engine.execute(sql_cmd)
        text1 = "完成!"
        text1 += "\n狀態：" + state
        text1 += "\n時間：" + date
        message = TextSendMessage(  #顯示訂房資料
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def pushMessage(event, msg):
    try:
        mtext = msg[6:]  #取得訊息
        sql_cmd = "select * from iestuser"
        query_data = db.engine.execute(sql_cmd)
        userall = list(query_data)
        for user in userall:  #逐一推播
            message = TextSendMessage(
                text = mtext
            )
            line_bot_api.push_message(to=user[1], messages=[message])  #推播訊息
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


if __name__ == '__main__':
    app.run()