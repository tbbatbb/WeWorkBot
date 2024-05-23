#!python3.9

import json
from . import Message
from xml.etree.ElementTree import Element

class MarkdownMessage(Message):

    # message type 
    type:str = 'markdown'
    # handler key 
    key:str = 'markdown'

    def __init__(self, to_username: str, from_username: str, agent_id: str, content: str, **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
        # the content in markdown format
        self.content:str = content

    def to_xml(self) -> str:
        '''Represent markdown message in XML format'''
        raise NotImplementedError('Unable to reply with a markdown message in current WeWork')

    def to_json(self) -> str:
        '''Represent markdown message in JSON format'''
        return json.dumps({"touser":self.to_username,"msgtype":"markdown","agentid":self.agent_id,"markdown":{"content":self.content},"safe":1 if self.safe else 0,"enable_id_trans":1 if self.enable_id_trans else 0,"enable_duplicate_check":1 if self.enable_duplicate_check else 0,"duplicate_check_interval":self.duplicate_check_interval})
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse markdown message from XML object'''
        raise NotImplementedError('Unable to receive and parse a markdown message in current WeWork')

