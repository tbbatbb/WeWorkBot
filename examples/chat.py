#!python3.9

from wwbot import WWBot
from wwbot.msg import VideoMessage
from wwbot.media import Media, UploadResult
from wwbot.chat import Chat

corp_id:str = 'ww274398273492874'
corp_secret:str = '23kjs9dufij3234WERq234rwer234'

# get the access token 
access_token:str = WWBot.get_access_token(corp_id, corp_secret)
print(access_token)

# create a group chat 
# !!!!!!!!!! make sure the bot is visible to the whole company, refer to https://developer.work.weixin.qq.com/document/path/90244   !!!!!!!!!!!!!!!!!
chat_id:str = Chat.create(access_token, 'Group Chat', ['tbbatbb', 'bbtabbt'], 'tbbatbb')

# upload the video 
ur:UploadResult = Media.upload(access_token, 'video', 'examples/files/video.mp4')

# to_username and agent_id can be None in the message for chat 
msg:VideoMessage = VideoMessage('to_username can be none', corp_id, 'agent_id can be none', ur.media_id, title='Video Test', desc='a video message', for_chat=True, chat_id=chat_id)

WWBot.send_to(corp_id, corp_secret, msg)
