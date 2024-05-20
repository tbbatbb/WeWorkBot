#!python3.9

import json
from . import Message
from xml.etree.ElementTree import Element

class TextMessage(Message):

    # message type 
    type:str = 'text'

    def __init__(self, to_username: str, from_username: str, content: str, **kwargs) -> None:
        super().__init__(to_username, from_username, **kwargs)
        # the content of the message 
        self.content:str = content

    def to_xml(self) -> str:
        '''Represent the text message in XML format'''
        return f'''<xml><ToUserName><![CDATA[{self.to_username}]]></ToUserName><FromUserName><![CDATA[{self.from_username}]]></FromUserName><CreateTime>{self.create_time}</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[{self.content}]]></Content><MsgId>{self.message_id}</MsgId><AgentID>{self.agent_id}</AgentID></xml>'''
        
    def to_json(self) -> str:
        '''Represent the text message in JSON format'''
        return json.dumps({"touser":self.to_username,"msgtype":"text","agentid":self.agent_id,"text":{"content":self.content}})
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse text message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        content:str = xml_tree.find('Content').text
        msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, content, agent_id=agent_id, create_time=create_time, msg_id=msg_id)
