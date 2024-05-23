#!python3.9

import requests, string, random
from ..lib import Logger
from requests import Response
from typing import List, Dict, Any, NamedTuple

class ChatInfo(NamedTuple):
    chat_id:str
    name:str
    owner:str
    user_list:List[str]

class Chat:

    logger:Logger = Logger('Chat')

    # api url for create chat 
    API_CREATE_URL:str = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access_token={token}'
    # api url for update chat 
    API_UPDATE_URL:str = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/update?access_token={token}'
    # api url for get chat 
    API_GET_URL:str = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/get?access_token={token}&chatid={chat_id}'

    @classmethod
    def create(cls, access_token:str, name:str, user_list:List[str], owner:str=None, chat_id:str=None) -> str:
        '''Create a chat with provided user list'''
        if len(user_list) < 2: return None
        if owner is None or owner not in user_list: owner = user_list[0]
        if chat_id is None: chat_id = ''.join(random.choices(string.ascii_letters+string.digits, k=32))
        url:str = cls.API_CREATE_URL.format(token=access_token)
        try:
            resp:Response = requests.post(url, json={"name":name,"owner": owner,"userlist":user_list,"chatid":chat_id}, timeout=20)
            if resp.status_code != 200:
                cls.logger.error('WxWork Receive Response With Status Code', resp.status_code)
                return None
            result:object = resp.json()
            if result['errcode'] != 0:
                cls.logger.error(result['errmsg'])
                return None
            return result['chatid']
        except Exception as e:
            cls.logger.error(e)
            return None
    
    @classmethod
    def update(cls, access_token:str, chat_id:str, name:str=None, add_user_list:List[str]=[], del_user_list:List[str]=[], owner:str=None) -> bool:
        '''Update a chat with provided information'''
        data:Dict[str, Any] = {"chatid": chat_id}
        if name is not None: data['name'] = name
        if owner is not None: data['owner'] = owner
        if len(add_user_list) > 0: data['add_user_list'] = add_user_list
        if len(del_user_list) > 0: data['del_user_list'] = del_user_list
        url:str = cls.API_UPDATE_URL.format(token=access_token)
        try:
            resp:Response = requests.post(url, json=data, timeout=20)
            if resp.status_code != 200:
                cls.logger.error('WxWork Receive Response With Status Code', resp.status_code)
                return False
            result:object = resp.json()
            if result['errcode'] != 0:
                cls.logger.error(result['errmsg'])
                return False
            return True
        except Exception as e:
            cls.logger.error(e)
            return False
    
    @classmethod
    def get(cls, access_token:str, chat_id:str) -> ChatInfo:
        '''Get a chat with provided chat id'''
        url:str = cls.API_GET_URL.format(token=access_token, chat_id=chat_id)
        try:
            resp:Response = requests.get(url, timeout=20)
            if resp.status_code != 200:
                cls.logger.error('WxWork Receive Response With Status Code', resp.status_code)
                return None
            result:object = resp.json()
            if result['errcode'] != 0:
                cls.logger.error(result['errmsg'])
                return None
            return ChatInfo(result['chat_info']['chatid'], result['chat_info']['name'], result['chat_info']['owner'], result['chat_info']['userlist'])
        except Exception as e:
            cls.logger.error(e)
            return None
