# -*- encoding: utf-8

import hashlib, base64, time, requests, json, random, string, struct, socket, logging, sys
import xml.etree.cElementTree as ET
from .lib import Logger
from queue import Queue
from threading import Thread
from requests import Response
from Crypto.Cipher import AES
from flask import Flask, request
from .msg import Message, msg_from_xml, TextMessage, ImageMessage, VoiceMessage, VideoMessage, LinkMessage, LocationMessage
from xml.etree.cElementTree import Element
from typing import List, Tuple, Callable, Literal, Dict, Union

log = logging.getLogger('werkzeug')
log.disabled = True
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

class WWBot:
    '''Bot class for self-built applications of WeWork'''

    logger:Logger = Logger('WWBot')
    # some api urls 
    API_PUSH_URL:str = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}'
    # api url for sending chat messages 
    API_CHATMSG_URL:str = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token={token}'
    # api url for sending messages as group bots 
    API_WEBHOOK_URL:str = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'
    API_TOKEN_URL:str = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={appsecret}'

    __last_token_got_at:int = 0
    __cached_access_token:str = ""
    __access_token_lifetime:int = 7200

    max_retry:int = 3

    msg_handler:Dict[str, Callable[[Message], Message]] = {}
    __msg_queue:Queue[Message] = Queue()
    # the list of messages that have been handled
    __msg_handled:List[str] = []

    # configurations 
    corp_id:str = ''
    corp_secret:str = ''
    token:str = ''
    aes_key:bytes = b''
    callback_path:str = '/mbot'
    flask_app:Flask = None

    # message types 
    TEXT:str = 'text'
    IMAGE:str = 'image'
    VOICE:str = 'voice'
    VIDEO:str = 'video'
    LOCATION:str = 'location'
    LINK:str = 'link'

    @classmethod
    def msg_responder(cls) -> None:
        '''A thread function for sending messages in the msg_queue'''
        cls.logger.info('Message responder thread started')
        while True:
            msg:Message = cls.__msg_queue.get()
            sent:bool = cls.send_to(cls.corp_id, cls.corp_secret, msg)
            if sent:
                cls.logger.info(f'Message No. {msg.message_id} sent asynchronously')
            else:
                cls.logger.error(f'Failed to send message No. {msg.message_id} asynchronously, try next time')
                time.sleep(1)

    @classmethod
    def config(cls, app:Flask, corp_id:str, corp_secret:str, token:str, aes_key:bytes, callback_path:str='/mbot'):
        '''Configure the basic arguments for the bot'''
        # flask app 
        cls.flask_app = app
        # corp id (in the page of corp. detail)
        cls.corp_id = corp_id
        # corp secret (maybe in the page of corp. detail too)
        cls.corp_secret = corp_secret
        # random token set in the page of application detail 
        cls.token = token
        # the key for AES encryption, set in the page of application detail 
        cls.aes_key = aes_key
        # the url path for the message callback 
        cls.callback_path = callback_path

        @cls.verify_handler()
        @cls.request_handler()
        def useless(): pass 

        # start the message respnder thread
        msg_resoonder_thread:Thread = Thread(target=cls.msg_responder, name='cls.msg_responder')
        msg_resoonder_thread.daemon = True
        msg_resoonder_thread.start()

    @classmethod
    def cal_sig(cls, token:str, timestamp:str, nonce:str, enc_text:str) -> str:
        '''Calculate the SHA1 signature for the message'''
        args:List[str] = [token, timestamp, nonce, enc_text]
        args.sort()
        sig_str:str = ''.join(args)
        return hashlib.sha1(sig_str.encode('utf-8')).hexdigest()

    @classmethod
    def aes_decrypt(cls, aes_key:bytes, enc_bytes:bytes) -> bytes:
        '''Decrypt the text that encrypted with AES'''
        enc_msg:bytes = base64.b64decode(enc_bytes)
        aes:AES = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
        return aes.decrypt(enc_msg)

    @classmethod
    def aes_encrypt(cls, aes_key:bytes, text:bytes) -> str:
        '''Encrypt the text with AES'''
        aes:AES = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
        text_len:int = len(text)
        block_size:int = 32
        to_pad:int = block_size - (text_len % block_size)
        if to_pad == 0: to_pad = block_size
        return base64.b64encode(aes.encrypt(text + chr(to_pad).encode('utf-8')*to_pad)).decode('utf-8')

    @classmethod
    def get_access_token(cls, corp_id:str, corp_secret:str) -> Tuple[str, None]:
        '''Get access token'''
        now:float = time.time()
        if now - cls.__last_token_got_at < cls.__access_token_lifetime: return cls.__cached_access_token
        try:
            resp:Response = requests.get(cls.API_TOKEN_URL.format(corpid=corp_id, appsecret=corp_secret), timeout=20)
            if resp.status_code != 200:
                cls.logger.error('WxWork Receive Response With Status Code', resp.status_code)
                return None
            result:object = resp.json()
            if result['errcode'] != 0:
                cls.logger.error(result['errmsg'])
                return None
            cls.__access_token_lifetime = result['expires_in']
            cls.__last_token_got_at = now
            cls.__cached_access_token = result['access_token']
            return cls.__cached_access_token
        except Exception as e:
            cls.logger.error(e)
            return None

    @classmethod
    def send_to(cls, corp_id:str, corp_secret:str, msg:Message):
        '''Send a text message to a specific user'''
        access_token:str = cls.get_access_token(corp_id, corp_secret)
        if access_token is None:
            cls.logger.error('Failed To Get Access Token')
            return False
        url:str = cls.API_PUSH_URL.format(token=access_token)
        # if the message is for chat 
        if msg.for_chat:
            cls.logger.info('Message sent as Chat Message')
            url = cls.API_CHATMSG_URL.format(token=access_token)
        # if the message is tended to be sent as group bot 
        elif msg.for_group_bot:
            cls.logger.info('Message sent as Group Bot Message')
            url = cls.API_WEBHOOK_URL.format(key=msg.group_bot_key)
        try:
            resp:Response = requests.post(url, data=msg.to_json(), timeout=20)
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
    def on(cls, msg_type:str, must_reply:bool=True) -> Callable[[Callable[[Message], Message | List[Message] | None]], Callable[[Message], Message | List[Message] | None]]:
        '''Decorator for message dealing'''
        def deco(func:Callable[[Message], Message | List[Message] | None]) -> Callable[[Message], Message | List[Message] | None]:
            def on_wrapper(msg:Message) -> Message | List[Message] | None:
                return func(msg)
            cls.msg_handler[msg_type] = on_wrapper
            return on_wrapper
        return deco
    
    @classmethod
    def verify_handler(cls, methods:List[str]=['GET']):
        '''Decorator for url verification callback'''
        def deco(func:Callable):
            @cls.flask_app.route(cls.callback_path, methods=methods)
            def verify_handler_wrapper():
                msg_sig:str = request.args.get('msg_signature', default='')
                ts:str = request.args.get('timestamp', default='')
                nonce:str = request.args.get('nonce', default='')
                echo_str:str = request.args.get('echostr', default='')

                sig:str = cls.cal_sig(cls.token, ts, nonce, echo_str)
                if msg_sig != sig:
                    cls.logger.error('Message Signature Dismatched. Sig. Supposed: {sig}, Sig. Actual: {msg_sig}')
                    return 'Invalid Message Signature', 403
                
                dec_msg:bytes = cls.aes_decrypt(cls.aes_key, echo_str)
                rdm_str:bytes = dec_msg[:16]
                msg_len:int = int.from_bytes(dec_msg[16:20], 'big')
                msg:str = dec_msg[20:20+msg_len].decode('utf-8')

                cls.logger.info(f'Got EchoString {msg}')

                return msg, 200
            return verify_handler_wrapper
        return deco

    @classmethod
    def request_handler(cls, methods:List[str]=['POST']):
        '''Decorator for request callback'''
        def deco(func:Callable):
            @cls.flask_app.route(cls.callback_path, methods=methods)
            def request_handler_wrapper():
                msg_sig:str = request.args.get('msg_signature', default='')
                ts:str = request.args.get('timestamp', default='')
                nonce:str = request.args.get('nonce', default='')

                req_msg:str = request.get_data(as_text=True)
                
                if len(req_msg) <= 0: return 'Page not found', 404

                req_msg_xml:Element = ET.fromstring(req_msg)
                enc_msg:str = req_msg_xml.find('Encrypt').text

                sig:str = cls.cal_sig(cls.token, ts, nonce, enc_msg)
                if msg_sig != sig:
                    cls.logger.error('Message Signature Unmatched. Sig. Supposed: {sig}, Sig. Actual: {msg_sig}')
                    return 'Invalid Message Signature'
                
                dec_msg:bytes = cls.aes_decrypt(cls.aes_key, enc_msg)
                msg_len:int = int.from_bytes(dec_msg[16:20], 'big')
                msg_xml_str:str = dec_msg[20:20+msg_len].decode('utf-8')

                msg_detail_xml:Element = ET.fromstring(msg_xml_str)
                # parse message for detail 
                msg:Message = msg_from_xml(msg_detail_xml)

                if msg is None or msg.message_id in cls.__msg_handled: return 'Not a new message', 200

                cls.__msg_handled.append(msg.message_id)
                cls.logger.info(f'Got a new {msg.__class__.__name__} message, NO. {msg.message_id}')
                
                if msg.key not in cls.msg_handler:
                    cls.logger.warn(f'No message handler registered for messages of "{msg.key}" type')
                    return '', 200

                start_at:float = time.time()
                resp_msg:Message | List[Message] = cls.msg_handler[msg.key](msg)
                time_cost:float = time.time() - start_at
                if isinstance(resp_msg, list) and len(resp_msg) <= 0: resp_msg = None
                if isinstance(resp_msg, list) and len(resp_msg) == 1: resp_msg = resp_msg[0]
                cls.logger.info(f'Message No. {msg.message_id} handled in {time_cost:.3f} seconds')
                if resp_msg is None: return 'No resonse', 200
                elif isinstance(resp_msg, list):
                    cls.logger.warn(f'Multiple response messages for message No. {msg.message_id}, try to reply asynchronously')
                    for m in resp_msg: cls.__msg_queue.put(m)
                    return 'Reply asynchronously', 403
                elif time_cost >= 4.5:
                    cls.logger.warn(f'Message No. {msg.message_id} handled too slowly, try to reply asynchronously')
                    cls.__msg_queue.put(resp_msg)
                    return 'Reply asynchronously', 403
                cls.logger.info('Reply in time')

                resp_ts:str = str(int(time.time()))
                resp_nonce:str = ''.join(random.choices(string.ascii_letters, k=10))
                resp_rdm_str:str = ''.join(random.choices(string.ascii_letters, k=16))
                resp_recv_id:str = ''.join(random.choices(string.digits, k=16)).encode('utf-8')
                
                resp_xml:str = resp_msg.to_xml()
                resp_msg_encrypt:str = cls.aes_encrypt(cls.aes_key, resp_rdm_str.encode('utf-8') + struct.pack('I', socket.htonl(len(resp_xml.encode('utf-8')))) + resp_xml.encode('utf-8') + resp_recv_id)
                resp_msg_sig:str = cls.cal_sig(cls.token, resp_ts, resp_nonce, resp_msg_encrypt)

                return f'''<xml><Encrypt><![CDATA[{resp_msg_encrypt}]]></Encrypt><MsgSignature><![CDATA[{resp_msg_sig}]]></MsgSignature><TimeStamp>{resp_ts}</TimeStamp><Nonce><![CDATA[{resp_nonce}]]></Nonce></xml>'''
            return request_handler_wrapper
        return deco

@WWBot.on(WWBot.TEXT)
def text_default(msg:TextMessage) -> Message:
    return TextMessage(msg.from_username, msg.to_username, msg.agent_id, msg.content)

@WWBot.on(WWBot.IMAGE)
def image_default(msg:ImageMessage) -> Message:
    return ImageMessage(msg.from_username, msg.to_username, msg.agent_id, msg.media_id)

@WWBot.on(WWBot.VOICE)
def voice_defualt(msg:VoiceMessage) -> Message:
    return VoiceMessage(msg.from_username, msg.to_username, msg.agent_id, msg.media_id)

@WWBot.on(WWBot.VIDEO)
def video_default(msg:VideoMessage) -> Message:
    return VideoMessage(msg.from_username, msg.to_username, msg.agent_id, msg.media_id)

@WWBot.on(WWBot.LOCATION)
def location_default(msg:LocationMessage) -> Message:
    return TextMessage(msg.from_username, msg.to_username, msg.agent_id, f'{msg.label}:({msg.location_x},{msg.location_y})\nScale:{msg.scale}')

@WWBot.on(WWBot.LINK)
def link_default(msg:LinkMessage) -> Message:
    return TextMessage(msg.from_username, msg.to_username, msg.agent_id, f'{msg.title}\n{msg.description}\n{msg.url}\n{msg.pic_url}')
