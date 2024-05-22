#!python3.9

import json
from . import Message
from xml.etree.ElementTree import Element

class FileMessage(Message):

    # message type 
    type:str = 'file'

    def __init__(self, to_username: str, from_username: str, agent_id: str, media_id: str, **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
        # media id for the file 
        self.media_id:str = media_id

    def to_xml(self) -> str:
        '''Represent file message in XML format'''
        raise NotImplementedError('Unable to reply with a file message in current WeWork')

    def to_json(self) -> str:
        '''Represent file message in JSON format'''
        return json.dumps({"touser":self.to_username,"msgtype":"file","agentid":self.agent_id,"file":{"media_id":self.media_id}})
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse file message from XML object'''
        raise NotImplementedError('Unable to receive and parse a file message in current WeWork')

