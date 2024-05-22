# -*- encoding: utf-8

from flask import Flask
from wwbot import WWBot
from wwbot.msg import TextCardMessage

app:Flask = Flask('EchoBot')

corp_id:str = 'ww274398273492874'
corp_secret:str = '23kjs9dufij3234WERq234rwer234'
to_username:str = 'tbbatbb'
agent_id = '1000004'

txtcard_msg = TextCardMessage(
    to_username, 
    corp_id, 
    agent_id, 
    'TextCard消息测试', 
    f'一条给 $userName={to_username}$ 的测试消息', 
    'https://www.qq.com', 
    'More', 
    safe=True,
    enable_id_trans=True
)

# agent id is required when sending a message
WWBot.send_to(corp_id, corp_secret, txtcard_msg)

