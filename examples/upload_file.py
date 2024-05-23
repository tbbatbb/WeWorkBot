#!python3.9

from wwbot import WWBot
from wwbot.msg import VideoMessage
from wwbot.media import Media, UploadResult

corp_id:str = 'ww274398273492874'
corp_secret:str = '23kjs9dufij3234WERq234rwer234'
to_username:str = 'tbbatbb'
agent_id = '1000004'

# get the access token 
access_token:str = WWBot.get_access_token(corp_id, corp_secret)

# upload the file and get the media_id 
ur:UploadResult = Media.upload(access_token, 'video', 'files/video.mp4')
# ur:UploadResult = Media.upload(access_token, 'file', 'files/video.mp4')
# ur:UploadResult = Media.upload(access_token, 'image', 'files/image.png')

if ur is None: print('uploading failed')

# construct the video message 
msg:VideoMessage = VideoMessage(to_username, corp_id, agent_id, ur.media_id, title='Video Message', desc='this is a video message')

# send the message 
WWBot.send_to(corp_id, corp_secret, msg)

# download file 
Media.download(access_token, ur.media_id, './saved_file')
