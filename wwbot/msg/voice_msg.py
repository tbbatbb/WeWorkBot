#!python3.9

import json
from . import Message
from xml.etree.ElementTree import Element

class VoiceMessage(Message):

    # message type 
    type:str = 'voice'

    def __init__(self, to_username: str, from_username: str, media_id: str, format:str = 'amr', **kwargs) -> None:
        super().__init__(to_username, from_username, **kwargs)
        # media id for the voice 
        self.media_id:str = media_id
        # the format of the voice file 
        self.format:str = format

    def to_xml(self) -> str:
        '''Represent voice message in XML format'''
        return f'''<xml><ToUserName><![CDATA[{self.to_username}]]></ToUserName><FromUserName><![CDATA[{self.from_username}]]></FromUserName><CreateTime>{self.create_time}</CreateTime><MsgType><![CDATA[voice]]></MsgType><Voice><MediaId><![CDATA[{self.media_id}]]></MediaId></Voice><MsgId>{self.message_id}</MsgId><AgentID>{self.agent_id}</AgentID></xml>'''

    def to_json(self) -> str:
        '''Represent voice message in JSON format'''
        return json.dumps({"touser":self.to_username,"msgtype":"voice","agentid":self.agent_id,"voice":{"media_id":self.media_id}})
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse voice message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        media_id:str = xml_tree.find('MediaId').text
        format:str = xml_tree.find('Format').text
        msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, media_id, format=format, agent_id=agent_id, create_time=create_time, msg_id=msg_id)

