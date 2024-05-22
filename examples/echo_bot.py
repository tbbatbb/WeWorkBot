# -*- encoding: utf-8

import base64
from flask import Flask
from wwbot import WWBot
from wwbot.msg import Message, TextMessage

app:Flask = Flask('EchoBot')

corp_id:str = 'ww274398273492874'
corp_secret:str = '23kjs9dufij3234WERq234rwer234'
# token and AES encoding key set in the application detail page 
token:str = '243posfq32ra23r'
aes_key:bytes = base64.b64decode('aGVsbG8gZnJvbSB0YmJhdGJiIQ==')
# the address and port on which the bot is serving on 
host:str = '0.0.0.0'
port:int = 31231
message_path:str = '/mbot'

# init the WWBot 
WWBot.config(app, corp_id, corp_secret, token, aes_key, callback_path=message_path)

# register a customized handler for text message 
# for the formats of RECEIVED message, refer to https://developer.work.weixin.qq.com/document/path/90239
@WWBot.on('text')
def text_handler(msg:TextMessage) -> Message:
    '''
    Response to text message 

    \param msg: an instance of TextMessage because the handler is registered to 'text'
    '''
    # return a simple text message to reply the message 
    return TextMessage(msg.from_username, msg.to_username, msg.agent_id, msg.content)

if __name__ == '__main__':
    app.run(host, port)