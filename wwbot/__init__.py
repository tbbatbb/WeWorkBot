# -*- encoding: utf-8

import hashlib, base64, time, requests, json, random, string, struct, socket, logging, sys
import xml.etree.cElementTree as ET
from .lib import Logger
from threading import Thread
from requests import Response
from Crypto.Cipher import AES
from flask import Flask, request
from xml.etree.cElementTree import Element
from typing import List, Tuple, Callable, Literal, Dict, Any

log = logging.getLogger('werkzeug')
log.disabled = True
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

class WWBot:
    '''Bot class for self-built applications of WeWork'''

    logger:Logger = Logger('WWBot')
    # some api urls 
    API_PUSH_URL:str = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}'
    API_TOKEN_URL:str = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={appsecret}'

    __last_token_got_at:int = 0
    __cached_access_token:str = ""
    __access_token_lifetime:int = 7200

    max_retry:int = 3

    msg_handler:Dict[str, Callable] = {}
    resp_msg_cache:Dict[str, Dict[Literal['nreq', 'resp', 'msg_xml'], Any]] = {}

    # configurations 
    corp_id:str = ''
    corp_secret:str = ''
    token:str = ''
    aes_key:bytes = b''

    @classmethod
    def config(cls, corp_id:str, corp_secret:str, token:str, aes_key:bytes):
        cls.corp_id = corp_id
        cls.corp_secret = corp_secret
        cls.token = token
        cls.aes_key = aes_key

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
    def send_to(cls, corp_id:str, corp_secret:str, json_data:str):
        '''Send a text message to a specific user'''
        access_token:str = cls.get_access_token(corp_id, corp_secret)
        if access_token is None:
            cls.logger.error('Failed To Get Access Token')
            return False
        url:str = cls.API_PUSH_URL.format(token=access_token)
        try:
            resp:Response = requests.post(url, data=json_data, timeout=20)
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
    def format_text_msg(cls, to_id:str, from_id:str, content:str) -> str:
        timestamp:str = str(int(time.time()))
        return f'''<xml><ToUserName><![CDATA[{to_id}]]></ToUserName><FromUserName><![CDATA[{from_id}]]></FromUserName> <CreateTime>{timestamp}</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[{content}]]></Content></xml>'''

    @classmethod
    def format_image_msg(cls, to_id:str, from_id:str, media_id:str) -> str:
        timestamp:str = str(int(time.time()))
        return f'''<xml><ToUserName><![CDATA[{to_id}]]></ToUserName><FromUserName><![CDATA[{from_id}]]></FromUserName><CreateTime>{timestamp}</CreateTime><MsgType><![CDATA[image]]></MsgType><Image><MediaId><![CDATA[{media_id}]]></MediaId></Image></xml>'''

    @classmethod
    def format_voice_msg(cls, to_id:str, from_id:str, media_id:str) -> str:
        timestamp:str = str(int(time.time()))
        return f'''<xml><ToUserName><![CDATA[{to_id}]]></ToUserName><FromUserName><![CDATA[{from_id}]]></FromUserName><CreateTime>{timestamp}</CreateTime><MsgType><![CDATA[voice]]></MsgType><Voice><MediaId><![CDATA[{media_id}]]></MediaId></Voice></xml>'''

    @classmethod
    def format_video_msg(cls, to_id:str, from_id:str, media_id:str, title:str, desc:str) -> str:
        timestamp:str = str(int(time.time()))
        return f'''<xml><ToUserName><![CDATA[{to_id}]]></ToUserName><FromUserName><![CDATA[{from_id}]]></FromUserName><CreateTime>{timestamp}</CreateTime><MsgType><![CDATA[video]]></MsgType><Video><MediaId><![CDATA[{media_id}]]></MediaId><Title><![CDATA[{title}]]></Title><Description><![CDATA[{desc}]]></Description></Video></xml>'''

    @classmethod
    def format_news_msg(cls, to_id:str, from_id:str, news:List[Dict[Literal['title', 'desc', 'pic_url', 'url'], str]]) -> str:
        timestamp:str = str(int(time.time()))
        news_str:str = ''.join(map(lambda n: f'''<item><Title><![CDATA[{n["title"] if "title" in n else ""}]]></Title> <Description><![CDATA[{n["desc"] if "desc" in n else ""}]]></Description><PicUrl><![CDATA[{n["pic_url"] if "pic_url" in n else ""}]]></PicUrl><Url><![CDATA[{n["url"] if "url" in n else ""}]]></Url></item>''', news))
        return f'''<xml><ToUserName><![CDATA[{to_id}]]></ToUserName><FromUserName><![CDATA[{from_id}]]></FromUserName><CreateTime>{timestamp}</CreateTime><MsgType><![CDATA[news]]></MsgType><ArticleCount>{len(news)}</ArticleCount><Articles>{news_str}</Articles></xml>'''

    @classmethod
    def trans_xml_to_json(cls, agent_id:str, msg_xml:Element) -> str:
        msg_type:str = msg_xml.find('MsgType').text
        to_id:str = msg_xml.find('ToUserName').text
        if msg_type == 'text': 
            content:str = msg_xml.find('Content').text
            return json.dumps({"touser":f"{to_id}","msgtype":"text","agentid":f"{agent_id}","text":{"content":f"{content}"}})
        if msg_type in ['image', 'voice']:
            media_id:str = msg_xml.find('MediaId').text
            return json.dumps({"touser":f"{to_id}","msgtype":"image","agentid":f"{agent_id}","image":{"media_id":f"{media_id}"}})
        if msg_type == 'video':
            media_id:str = msg_xml.find('MediaId').text
            title:str = msg_xml.find('Title').text
            desc:str = msg_xml.find('Description').text
            return json.dumps({"touser":f"{to_id}","msgtype":"video","agentid":f"{agent_id}","image":{"media_id":f"{media_id}","title":f"{title}","description":f"{desc}"}})
        return '{}'

    @classmethod
    def on(cls, msg_type:Literal['text', 'image', 'voice', 'video', 'location', 'link'], must_reply:bool=True) -> Callable:
        '''Decorator for message dealing'''
        def deco(func:Callable):
            def on_wrapper(*args, **kwargs):
                msg_xml:Element = args[2]
                to_user:str = msg_xml.find('ToUserName').text
                from_user:str = msg_xml.find('FromUserName').text
                msg_id:str = msg_xml.find('MsgId').text
                if msg_id in cls.resp_msg_cache and cls.resp_msg_cache[msg_id]['resp'] is not None:
                    resp:str = cls.resp_msg_cache[msg_id]['resp']
                    del cls.resp_msg_cache[msg_id]
                    return resp
                if msg_id in cls.resp_msg_cache: return None

                def thread_job(corp_id:str, corp_secret:str, msg_xml:Element):
                    resp:str = func(from_user, to_user, msg_xml)
                    cls.resp_msg_cache[msg_id]['resp'] = resp
                    if cls.resp_msg_cache[msg_id]['nreq'] >= cls.max_retry:
                        if must_reply:
                            user_id:str = msg_xml.find('FromUserName').text
                            agent_id:str = msg_xml.find('AgentID').text
                            cls.logger.info(f'Reply to the message No. {msg_id} of {user_id} asynchronously')
                            cls.send_to(corp_id, corp_secret, cls.trans_xml_to_json(agent_id, ET.fromstring(resp)))
                        del cls.resp_msg_cache[msg_id]

                cls.resp_msg_cache[msg_id] = {
                    'nreq': 0,
                    'resp': None,
                    'msg_xml': msg_xml
                }
                thread:Thread = Thread(target=thread_job, args=args, kwargs=kwargs)
                thread.start()
            cls.msg_handler[msg_type] = on_wrapper
            return on_wrapper
        return deco
    
    @classmethod
    def verify_handler(cls, app:Flask, path:str, methods:List[str]=['GET']):
        '''Decorator for url verification callback'''
        def deco(func:Callable):
            @app.route(path, methods=methods)
            def verify_handler_wrapper(*args, **kwargs):
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
    def request_handler(cls, app:Flask, path:str, methods:List[str]=['POST']):
        '''Decorator for request callback'''
        def deco(func:Callable):
            @app.route(path, methods=methods)
            def request_handler_wrapper(*args, **kwargs):
                msg_sig:str = request.args.get('msg_signature', default='')
                ts:str = request.args.get('timestamp', default='')
                nonce:str = request.args.get('nonce', default='')

                req_msg:str = request.get_data(as_text=True)
                
                if len(req_msg) <= 0: return 'Page not found', 404

                req_msg_xml:Element = ET.fromstring(req_msg)
                enc_msg:str = req_msg_xml.find('Encrypt').text

                sig:str = cls.cal_sig(cls.token, ts, nonce, enc_msg)
                if msg_sig != sig:
                    cls.logger.error('Message Signature Dismatched. Sig. Supposed: {sig}, Sig. Actual: {msg_sig}')
                    return 'Invalid Message Signature'
                
                dec_msg:bytes = cls.aes_decrypt(cls.aes_key, enc_msg)
                msg_len:int = int.from_bytes(dec_msg[16:20], 'big')
                msg:str = dec_msg[20:20+msg_len].decode('utf-8')

                msg_detail_xml:Element = ET.fromstring(msg)
                msg_type:str = msg_detail_xml.find('MsgType').text
                msg_id:str = msg_detail_xml.find('MsgId').text

                cls.logger.info(f'Got a new {msg_type} message, NO. {msg_id}')

                start_at:float = time.time()
                resp_xml:str = cls.msg_handler[msg_type](cls.corp_id, cls.corp_secret, msg_detail_xml)
                while (time.time() - start_at < 4.8) and resp_xml is None:
                    time.sleep(0.4)
                    resp_xml = cls.msg_handler[msg_type](cls.corp_id, cls.corp_secret, msg_detail_xml)
                if resp_xml is None:
                    cls.resp_msg_cache[msg_id]['nreq'] += 1
                    cls.logger.warn('Failed to reply in time, try next time')
                    time.sleep(0.2)
                    return '', 403
                cls.logger.info('Reply in time')

                resp_ts:str = str(int(time.time()))
                resp_nonce:str = ''.join(random.choices(string.ascii_letters, k=10))
                resp_rdm_str:str = ''.join(random.choices(string.ascii_letters, k=16))
                resp_recv_id:str = ''.join(random.choices(string.digits, k=16)).encode('utf-8')
                
                resp_msg_encrypt:str = cls.aes_encrypt(cls.aes_key, resp_rdm_str.encode('utf-8') + struct.pack('I', socket.htonl(len(resp_xml.encode('utf-8')))) + resp_xml.encode('utf-8') + resp_recv_id)
                resp_msg_sig:str = cls.cal_sig(cls.token, resp_ts, resp_nonce, resp_msg_encrypt)

                return f'''<xml><Encrypt><![CDATA[{resp_msg_encrypt}]]></Encrypt><MsgSignature><![CDATA[{resp_msg_sig}]]></MsgSignature><TimeStamp>{resp_ts}</TimeStamp><Nonce><![CDATA[{resp_nonce}]]></Nonce></xml>'''
            return request_handler_wrapper
        return deco

@WWBot.on('text')
def text_default(from_user:str, to_user:str, msg_xml:Element) -> str:
    msg_content:str = msg_xml.find('Content').text
    return WWBot.format_text_msg(from_user, to_user, msg_content)

@WWBot.on('image')
def image_default(from_user:str, to_user:str, msg_xml:Element) -> str:
    pic_url:str = msg_xml.find('PicUrl').text
    media_id:str = msg_xml.find('MediaId').text
    return WWBot.format_image_msg(from_user, to_user, media_id)

@WWBot.on('voice')
def voice_defualt(from_user:str, to_user:str, msg_xml:Element) -> str:
    media_id:str = msg_xml.find('MediaId').text
    return WWBot.format_voice_msg(from_user, to_user, media_id)

@WWBot.on('video')
def video_default(from_user:str, to_user:str, msg_xml:Element) -> str:
    media_id:str = msg_xml.find('MediaId').text
    title:str = msg_xml.find('Title').text
    desc:str = msg_xml.find('Description').text
    return WWBot.format_video_msg(from_user, to_user, media_id, title, desc)

@WWBot.on('location')
def location_default(from_user:str, to_user:str, msg_xml:Element) -> str:
    loc_x:str = msg_xml.find('Location_X').text
    loc_y:str = msg_xml.find('Location_Y').text
    scale:str = msg_xml.find('Scale').text
    label:str = msg_xml.find('Label').text
    msg:str = f'{label}:({loc_x},{loc_y})\nScale:{scale}'
    return WWBot.format_text_msg(from_user, to_user, msg)

@WWBot.on('link')
def link_default(from_user:str, to_user:str, msg_xml:Element) -> str:
    title:str = msg_xml.find('Title').text
    desc:str = msg_xml.find('Description').text
    url:str = msg_xml.find('Url').text
    pic_url:str = msg_xml.find('PicUrl').text
    msg:str = f'[《{title}》:{desc}]({url})\nPic: {pic_url}'
    return WWBot.format_text_msg(from_user, to_user, msg)
