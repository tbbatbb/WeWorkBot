#!python3.9

from . import EventMessage
from xml.etree.ElementTree import Element
from typing import List, NamedTuple

class PicInfo(NamedTuple):
    pic_md5_sum:str

class PicSysPhotoEventMessage(EventMessage):

    # handler key 
    key:str = 'event.pic_sysphoto'

    def __init__(self, to_username: str, from_username: str, agent_id: str, event: str, count:str, pic_list:List[PicInfo], event_key: str = '', **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, event, event_key=event_key, **kwargs)
        # pic count
        self.count:str = count
        # pic list 
        self.pic_list:List[PicInfo] = pic_list

    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse pic_sysphoto event message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        event:str = xml_tree.find('Event').text
        event_key:str = xml_tree.find('EventKey').text
        count:str = xml_tree.find('SendPicsInfo/Count').text
        items:str = xml_tree.findall('SendPicsInfo/PicList/Item')
        pic_list:List[PicInfo] = list(map(lambda item: item.find('PicMd5Sum').text, items))
        # msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, agent_id, event, count, pic_list, event_key=event_key, create_time=create_time)