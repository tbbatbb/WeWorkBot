# -*- encoding: utf-8

import time, random
from abc import abstractmethod
from xml.etree.cElementTree import Element

class Message:

    def __init__(self, to_username:str, from_username:str, agent_id:str='', create_time:int=None, msg_id:int=None) -> None:
        # the id of the receiver of the message 
        self.to_username:str = to_username
        # the id of the sender of the message 
        self.from_username:str = from_username
        # the agent id of the message
        # also known as the application id 
        self.agent_id:str = agent_id
        # timestamp for the message 
        self.create_time:int = create_time or int(time.time())
        # message id 
        self.message_id:int = msg_id or self.create_time * 1000 + random.randint(1000, 9999)
    
    @abstractmethod
    def to_xml(self) -> str:
        '''Represent the message in XML format'''
        pass

    @abstractmethod
    def to_json(self) -> str:
        '''Represent the message in JSON format'''
        pass

    @abstractmethod
    @classmethod
    def from_xml(cls, xml_tree:Element):
        '''Parse different types of messages from XML object'''
        pass 


from .text_msg import TextMessage
from .image_msg import ImageMessage

def msg_from_xml(xml_tree:Element) -> Message:
    '''Parse message from xml tree'''
    msg_type:str = xml_tree.find('MsgType').text
    if msg_type == 'text': return TextMessage.from_xml(xml_tree)
    if msg_type == 'image': return ImageMessage.from_xml(xml_tree)
