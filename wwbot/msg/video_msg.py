#!python3.9

import json
from . import Message
from typing import Any, Dict
from xml.etree.ElementTree import Element

class VideoMessage(Message):

    # message type 
    type:str = 'video'
    # handler key 
    key:str = 'video'

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
        data:Dict[str, Any] = {"msgtype":"video","video":{"media_id":self.media_id,"title":self.title,"description":self.description},"safe":1 if self.safe else 0,"enable_id_trans":1 if self.enable_id_trans else 0,"enable_duplicate_check":1 if self.enable_duplicate_check else 0,"duplicate_check_interval":self.duplicate_check_interval}
        if self.for_chat: data.update({"chatid":self.chat_id})
        elif not self.for_group_bot: data.update({"touser":self.to_username,"agentid":self.agent_id})
        return json.dumps(data)
    
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

        return cls(to_username, from_username, agent_id, media_id, thumb_id=thumb_id, create_time=create_time, msg_id=msg_id)

