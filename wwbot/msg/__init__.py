# -*- encoding: utf-8

import time, random
from ..lib import Logger
from abc import abstractmethod
from xml.etree.cElementTree import Element

class Message:

    logger:Logger = Logger('Message')

    # message type 
    type:str = 'message'
    # handler key 
    key:str = 'message'

    def __init__(self, to_username:str, from_username:str, agent_id:str, create_time:int=None, msg_id:int=None, safe:bool=False, enable_id_trans:bool=False, enable_duplicate_check:bool=False, duplicate_check_interval:int=1800, for_chat:bool=False, chat_id:str=None, for_group_bot:bool=False, group_bot_key:str=None) -> None:
        # the id of the receiver of the message 
        self.to_username:str = to_username
        # the id of the sender of the message 
        self.from_username:str = from_username
        # the agent id of the message
        # also known as the application id 
        self.agent_id:str = agent_id
        # timestamp for the message 
        self.create_time:int = int(create_time) if create_time is not None else int(time.time())
        # message id 
        self.message_id:int = msg_id or (self.create_time * 1000 + random.randint(1000, 9999))
        # whether the message can be shared when it's sent by send_to 
        self.safe:bool = safe
        # whether to enable the id translation
        self.enable_id_trans:bool = enable_id_trans
        # whether to check the message duplication 
        self.enable_duplicate_check:bool = enable_duplicate_check
        # the interval of message duplication checking, in second
        self.duplicate_check_interval:int = duplicate_check_interval
        # whether the message is prepared for some chat 
        self.for_chat:bool = for_chat
        # if the message is prepared for some chat, then it will be sent to the chat with chat_id 
        self.chat_id:str = chat_id
        # whether the message is sent by a group bot
        self.for_group_bot:bool = for_group_bot
        # the key to send messages as group bots
        # contained in the webhook url of the group bot, like: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6449f223-4920-2394-3aa39d939ae0
        self.group_bot_key:str = group_bot_key
    
    @abstractmethod
    def to_xml(self) -> str:
        '''Represent the message in XML format'''
        pass

    @abstractmethod
    def to_json(self) -> str:
        '''Represent the message in JSON format'''
        pass

    @classmethod
    @abstractmethod
    def from_xml(cls, xml_tree:Element):
        '''Parse different types of messages from XML object'''
        pass 

from .event import event_msg_from_xml
from .text_msg import TextMessage
from .link_msg import LinkMessage
from .file_msg import FileMessage
from .image_msg import ImageMessage
from .voice_msg import VoiceMessage
from .video_msg import VideoMessage
from .news_msg import News, NewsMessage
from .location_msg import LocationMessage
from .markdown_msg import MarkdownMessage
from .textcard_msg import TextCardMessage
from .mpnews_msg import MPNews, MPNewsMessage

def msg_from_xml(xml_tree:Element) -> Message:
    '''Parse message from xml tree'''
    msg_type:str = xml_tree.find('MsgType').text
    if msg_type == 'event': return event_msg_from_xml(xml_tree)
    if msg_type == 'text': return TextMessage.from_xml(xml_tree)
    if msg_type == 'image': return ImageMessage.from_xml(xml_tree)
    if msg_type == 'voice': return VoiceMessage.from_xml(xml_tree)
    if msg_type == 'video': return VideoMessage.from_xml(xml_tree)
    if msg_type == 'link': return LinkMessage.from_xml(xml_tree)
    if msg_type == 'location': return LocationMessage.from_xml(xml_tree)
    Message.logger.warn('Unregistered message type')
