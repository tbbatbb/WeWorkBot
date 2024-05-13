# -*- encoding: utf-8

import requests, base64, configparser
from flask import Flask
from wwbot import WWBot
from requests import Response
from xml.etree.cElementTree import Element

# register a customized handler for text message 
# for the formats of RECEIVED message, refer to https://developer.work.weixin.qq.com/document/path/90239
@WWBot.on('text')
def text_handler(from_user:str, to_user:str, msg_xml:Element) -> str:
    '''
    Response to text message 

    \param from_user: the ID of the user that sends the message
    \param to_user: usually equal to corp_id
    '''
    # get the content of the message 
    msg_content:str = msg_xml.find('Content').text
    gpt_url:str = 'http://idonotknow.theexact.url/v1/chat/completions'
    try:
        resp:Response = requests.post(gpt_url, json={
            "stream": False,
            "model": "gpt-4-0613",
            "messages": [{
                "role": "user",
                "content": msg_content
            }]
        }, headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer SomeToken'
        })
        if resp.status_code != 200: return 'No Response'
        answer:str = resp.json()['choices'][0]['message']['content']
        # return a string of xml format to reply the message 
        return WWBot.format_text_msg(from_user, to_user, answer)
    except Exception as e:
        WWBot.logger.error(e)
    # return a string of xml format to reply the message 
    return WWBot.format_text_msg(from_user, to_user, 'No Response')

config = configparser.ConfigParser()
config.read('config.ini')

app:Flask = Flask(config['WWBot']['app_name'])
corp_id:str = config['WeWork']['corp_id']
corp_secret:str = config['WeWork']['corp_secret']
token:str = config['WeWork']['token']
aes_key:bytes = base64.b64decode(config['WeWork']['aes_key'])
host:str = config['WWBot']['app_host']
port:int = int(config['WWBot']['app_port'])

# init the WWBot 
WWBot.config(corp_id, corp_secret, token, aes_key)

@WWBot.verify_handler(app, config['WWBot']['verify_path'])
@WWBot.request_handler(app, config['WWBot']['message_path'])
def useless(): 
    # the function is useless
    # it will not be called in the current version of WWBot
    pass

if __name__ == '__main__':
    app.run(host, port)