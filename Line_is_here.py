from flask import Flask, request, abort

#import packages and stuff
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
access_token = 'o3NtWyLEA68fXcXQaAdOuF/wTcZGuO4097AUEHcaTAe16aqJSpcqheCZA5ZrkKatuI3KbmfHTZoqBxBj3JQoaO1zpJXKbqFw8pAoA4aOX7ENwz3HRb0XtOcUsaYMm0mWTLEYGbldAEbVHsOjjWFgPwdB04t89/1O/w1cDnyilFU='
secret_token = 'd987897feed579975744d39c86253e45'
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret_token)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()