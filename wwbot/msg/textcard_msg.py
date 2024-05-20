#!python3.9

import json
from . import Message
from xml.etree.ElementTree import Element

class TextCardMessage(Message):

    # message type 
    type:str = 'textcard'

    def __init__(self, to_username: str, from_username: str, title: str, desc:str, url:str, btntext:str='', **kwargs) -> None:
        super().__init__(to_username, from_username, **kwargs)
        # the title for the card
        self.title:str = title
        # the description for the card 
        self.description:str = desc
        # the url for the card 
        self.url:str = url
        # the text for the button 
        self.btntext:str = btntext

    def to_xml(self) -> str:
        '''Represent textcard message in XML format'''
        raise NotImplementedError('Unable to reply with a textcard message in current WeWork')

    def to_json(self) -> str:
        '''Represent textcard message in JSON format'''
        return json.dumps({"touser":self.to_username,"msgtype":"textcard","agentid":self.agent_id,"textcard":{"title":self.title,"description":self.description,"url":self.url,"btntext":self.btntext}})
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse textcard message from XML object'''
        raise NotImplementedError('Unable to receive and parse a textcard message in current WeWork')

