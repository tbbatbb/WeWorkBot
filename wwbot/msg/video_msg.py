#!python3.9

import json
from . import Message
from xml.etree.ElementTree import Element

class VideoMessage(Message):

    # message type 
    type:str = 'video'

    def __init__(self, to_username: str, from_username: str, agent_id: str, media_id: str, thumb_id:str = '', title:str = '', desc:str = '', **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
        # media id for the video 
        self.media_id:str = media_id
        # the id for the thumb image
        self.thumb_media_id:str = thumb_id
        # title for the video
        self.title:str = title
        # description for the video 
        self.description = desc

    def to_xml(self) -> str:
        '''Represent video message in XML format'''
        return f'''<xml><ToUserName><![CDATA[{self.to_username}]]></ToUserName><FromUserName><![CDATA[{self.from_username}]]></FromUserName><CreateTime>{self.create_time}</CreateTime><MsgType><![CDATA[video]]></MsgType><Video><MediaId><![CDATA[{self.media_id}]]></MediaId><Title><![CDATA[{self.title}]]></Title><Description><![CDATA[{self.description}]]></Description></Video><MsgId>{self.message_id}</MsgId><AgentID>{self.agent_id}</AgentID></xml>'''

    def to_json(self) -> str:
        '''Represent video message in JSON format'''
        return json.dumps({"touser":self.to_username,"msgtype":"video","agentid":self.agent_id,"video":{"media_id":self.media_id,"title":self.title,"description":self.description}})
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse video message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        media_id:str = xml_tree.find('MediaId').text
        thumb_id:str = xml_tree.find('ThumbMediaId').text
        msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, media_id, thumb_id=thumb_id, agent_id=agent_id, create_time=create_time, msg_id=msg_id)

