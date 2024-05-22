# -*- encoding: utf-8

from flask import Flask
from wwbot import WWBot
from wwbot.msg import TextMessage

app:Flask = Flask('EchoBot')

corp_id:str = 'ww274398273492874'
corp_secret:str = '23kjs9dufij3234WERq234rwer234'
agent_id = '1000004'

# agent id is required when sending a message
WWBot.send_to(corp_id, corp_secret, TextMessage('tbbatbb', corp_id, agent_id, 'hello from tbbatbb!'))

