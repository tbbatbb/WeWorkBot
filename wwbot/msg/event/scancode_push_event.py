#!python3.9

from xml.etree.ElementTree import Element
from . import EventMessage

class ScanCodePushEventMessage(EventMessage):

    # handler key 
    key:str = 'event.scancode_push'

    def __init__(self, to_username: str, from_username: str, agent_id: str, event: str, scan_type:str, scan_result:str, event_key: str = '', **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, event, event_key=event_key, **kwargs)
        # scan type 
        self.scan_type:str = scan_type
        # scan result 
        self.scan_result:str = scan_result

    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse scancode_push event message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        event:str = xml_tree.find('Event').text
        event_key:str = xml_tree.find('EventKey').text
        scan_type:str = xml_tree.find('ScanCodeInfo/ScanType').text
        scan_result:str = xml_tree.find('ScanCodeInfo/ScanResult').text
        # msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, agent_id, event, scan_type, scan_result, event_key=event_key, create_time=create_time)