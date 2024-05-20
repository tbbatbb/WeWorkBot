#!python3.9

import json
from . import Message
from xml.etree.ElementTree import Element

class ImageMessage(Message):

    # message type 
    type:str = 'image'

    def __init__(self, to_username: str, from_username: str, media_id: str, pic_url:str = '', **kwargs) -> None:
        super().__init__(to_username, from_username, **kwargs)
        # media id for the image 
        self.media_id:str = media_id
        # the url for the picture 
        self.pic_url:str = pic_url

    def to_xml(self) -> str:
        '''Represent image message in XML format'''
        return f'''<xml><ToUserName><![CDATA[{self.to_username}]]></ToUserName><FromUserName><![CDATA[{self.from_username}]]></FromUserName><CreateTime>{self.create_time}</CreateTime><MsgType><![CDATA[image]]></MsgType><Image><MediaId><![CDATA[{self.media_id}]]></MediaId></Image><MsgId>{self.message_id}</MsgId><AgentID>{self.agent_id}</AgentID></xml>'''

    def to_json(self) -> str:
        '''Represent image message in JSON format'''
        return json.dumps({"touser":self.to_username,"msgtype":"image","agentid":self.agent_id,"image":{"media_id":self.media_id}})
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse image message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        pic_url:str = xml_tree.find('PicUrl').text
        media_id:str = xml_tree.find('MediaId').text
        msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, media_id, pic_url=pic_url, agent_id=agent_id, create_time=create_time, msg_id=msg_id)

