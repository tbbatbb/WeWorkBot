#!python3.9

import json
from . import Message
from xml.etree.ElementTree import Element

class MarkdownMessage(Message):

    # message type 
    type:str = 'markdown'

    def __init__(self, to_username: str, from_username: str, content: str, **kwargs) -> None:
        super().__init__(to_username, from_username, **kwargs)
        # the content in markdown format
        self.content:str = content

    def to_xml(self) -> str:
        '''Represent markdown message in XML format'''
        raise NotImplementedError('Unable to reply with a markdown message in current WeWork')

    def to_json(self) -> str:
        '''Represent markdown message in JSON format'''
        return json.dumps({"touser":self.to_username,"msgtype":"markdown","agentid":self.agent_id,"markdown":{"content":self.content}})
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse markdown message from XML object'''
        raise NotImplementedError('Unable to receive and parse a markdown message in current WeWork')

