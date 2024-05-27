#!python3.9

import json
from . import Message
from typing import Any, Dict
from xml.etree.ElementTree import Element

class TextCardMessage(Message):

    # message type 
    type:str = 'textcard'
    # handler key 
    key:str = 'textcard'

    def __init__(self, to_username: str, from_username: str, agent_id: str, title: str, desc:str, url:str, btntext:str='', **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
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
        data:Dict[str, Any] = {"msgtype":"textcard","textcard":{"title":self.title,"description":self.description,"url":self.url,"btntext":self.btntext},"safe":1 if self.safe else 0,"enable_id_trans":1 if self.enable_id_trans else 0,"enable_duplicate_check":1 if self.enable_duplicate_check else 0,"duplicate_check_interval":self.duplicate_check_interval}
        if self.for_chat: data.update({"chatid":self.chat_id})
        elif not self.for_group_bot: data.update({"touser":self.to_username,"agentid":self.agent_id})
        return json.dumps(data)
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse textcard message from XML object'''
        raise NotImplementedError('Unable to receive and parse a textcard message in current WeWork')

