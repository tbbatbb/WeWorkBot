#!python3.9

import json
from . import Message
from typing import Any, Dict
from xml.etree.ElementTree import Element

class TextMessage(Message):

    # message type 
    type:str = 'text'
    # handler key 
    key:str = 'text'

    def __init__(self, to_username: str, from_username: str, agent_id: str, content: str, **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
        # the content of the message 
        self.content:str = content

    def to_xml(self) -> str:
        '''Represent the text message in XML format'''
        return f'''<xml><ToUserName><![CDATA[{self.to_username}]]></ToUserName><FromUserName><![CDATA[{self.from_username}]]></FromUserName><CreateTime>{self.create_time}</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[{self.content}]]></Content><MsgId>{self.message_id}</MsgId><AgentID>{self.agent_id}</AgentID></xml>'''
        
    def to_json(self) -> str:
        '''Represent the text message in JSON format'''
        data:Dict[str, Any] = {"msgtype":"text","text":{"content":self.content},"safe":1 if self.safe else 0,"enable_id_trans":1 if self.enable_id_trans else 0,"enable_duplicate_check":1 if self.enable_duplicate_check else 0,"duplicate_check_interval":self.duplicate_check_interval}
        if self.for_chat: data.update({"chatid":self.chat_id})
        elif not self.for_group_bot: data.update({"touser":self.to_username,"agentid":self.agent_id})
        return json.dumps(data)
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse text message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        content:str = xml_tree.find('Content').text
        msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, agent_id, content, create_time=create_time, msg_id=msg_id)

