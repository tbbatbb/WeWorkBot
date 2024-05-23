#!python3.9

from . import Message
from xml.etree.ElementTree import Element

class LocationMessage(Message):

    # message type 
    type:str = 'location'
    # handler key 
    key:str = 'location'

    def __init__(self, to_username: str, from_username: str, agent_id: str, loc_x:str, loc_y:str, scale:str, label:str, **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
        # the latitude value for the location
        self.location_x:str = loc_x
        # the longitude value for the location 
        self.location_y:str = loc_y
        # the scale 
        self.scale:str = scale
        # the lable for the location 
        self.label:str = label

    def to_xml(self) -> str:
        '''Represent location message in XML format'''
        raise NotImplementedError('Unable to reply with a location message in current WeWork')

    def to_json(self) -> str:
        '''Represent location message in JSON format'''
        raise NotImplementedError('Unable to send a location message in current WeWork')
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse location message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        loc_x:str = xml_tree.find('Location_X').text
        loc_y:str = xml_tree.find('Location_Y').text
        scale:str = xml_tree.find('Scale').text
        label:str = xml_tree.find('Label').text
        msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, agent_id, loc_x, loc_y, scale, label, create_time=create_time, msg_id=msg_id)

