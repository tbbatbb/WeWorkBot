# -*- encoding: utf-8

from wwbot import WWBot
from wwbot.msg import TextCardMessage

corp_id:str = 'ww274398273492874'
corp_secret:str = '23kjs9dufij3234WERq234rwer234'
to_username:str = 'tbbatbb'
agent_id = '1000004'

txtcard_msg = TextCardMessage(
    to_username, 
    corp_id, 
    agent_id, 
    'This Is A TextCard Message', 
    f'A test message for $userName={to_username}$', 
    'https://www.qq.com', 
    'More', 
    safe=True,
    enable_id_trans=True
)

# WWBot does not need to be configured if only `send_to` is used

# agent id is required when sending a message
WWBot.send_to(corp_id, corp_secret, txtcard_msg)

