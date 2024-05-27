#!python3.9

import json
from . import Message
from typing import Dict, Any
from xml.etree.ElementTree import Element

class FileMessage(Message):

    # message type 
    type:str = 'file'
    # handler key 
    key:str = 'file'

    def __init__(self, to_username: str, from_username: str, agent_id: str, media_id: str, **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
        # media id for the file 
        self.media_id:str = media_id

    def to_xml(self) -> str:
        '''Represent file message in XML format'''
        raise NotImplementedError('Unable to reply with a file message in current WeWork')

    def to_json(self) -> str:
        '''Represent file message in JSON format'''
        data:Dict[str, Any] = {"msgtype":"file","file":{"media_id":self.media_id},"safe":1 if self.safe else 0,"enable_id_trans":1 if self.enable_id_trans else 0,"enable_duplicate_check":1 if self.enable_duplicate_check else 0,"duplicate_check_interval":self.duplicate_check_interval}
        if self.for_chat: data.update({"chatid":self.chat_id})
        elif not self.for_group_bot: data.update({"touser":self.to_username,"agentid":self.agent_id})
        return json.dumps(data)
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse file message from XML object'''
        raise NotImplementedError('Unable to receive and parse a file message in current WeWork')

