#!python3.9

from xml.etree.ElementTree import Element
from . import EventMessage

class LocationEventMessage(EventMessage):

    # handler key 
    key:str = 'event.location'

    def __init__(self, to_username: str, from_username: str, agent_id: str, event: str, latitude:str, longitude:str, precision:str, event_key: str = '', **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, event, event_key=event_key, **kwargs)
        # latitude 
        self.latitude:str = latitude
        # longitude
        self.longitude:str = longitude
        # precision 
        self.precision:str = precision

    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse location event message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        event:str = xml_tree.find('Event').text
        event_key:str = '' if xml_tree.find('EventKey') is None else xml_tree.find('EventKey').text
        latitude:str = xml_tree.find('Latitude').text
        longitude:str = xml_tree.find('Longitude').text
        precision:str = xml_tree.find('Precision').text
        # msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, agent_id, event, latitude, longitude, precision, event_key=event_key, create_time=create_time)