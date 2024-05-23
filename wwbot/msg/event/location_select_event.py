#!python3.9

from . import EventMessage
from xml.etree.ElementTree import Element

class LocationSelectEventMessage(EventMessage):

    # handler key 
    key:str = 'event.location_select'

    def __init__(self, to_username: str, from_username: str, agent_id: str, event: str, loc_x:str, loc_y:str, scale:str, label:str, poi_name:str, event_key: str = '', **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, event, event_key=event_key, **kwargs)
        # location x
        self.location_x:str = loc_x
        # location y 
        self.location_y:str = loc_y
        # scale 
        self.scale:str = scale
        # label for the position 
        self.label:str = label
        self.poiname:str = poi_name

    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse location_select event message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        event:str = xml_tree.find('Event').text
        event_key:str = xml_tree.find('EventKey').text
        loc_x:str = xml_tree.find('SendLocationInfo/Location_X').text
        loc_y:str = xml_tree.find('SendLocationInfo/Location_Y').text
        scale:str = xml_tree.find('SendLocationInfo/Scale').text
        label:str = xml_tree.find('SendLocationInfo/Label').text
        poi_name:str = xml_tree.find('SendLocationInfo/Poiname').text
        # msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, agent_id, event, loc_x, loc_y, scale, label, poi_name, event_key=event_key, create_time=create_time)