#!python3.9

from . import Message
from xml.etree.ElementTree import Element

class LinkMessage(Message):

    # message type 
    type:str = 'link'
    # handler key 
    key:str = 'link'

    def __init__(self, to_username: str, from_username: str, agent_id: str, title:str, desc:str, url:str, pic_url:str, **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
        # the title of the link
        self.title:str = title
        # the description of the link 
        self.description:str = desc
        # the url for the link 
        self.url:str = url
        # the url for the cover image 
        self.pic_url:str = pic_url

    def to_xml(self) -> str:
        '''Represent link message in XML format'''
        raise NotImplementedError('Unable to reply with a link message in current WeWork')

    def to_json(self) -> str:
        '''Represent link message in JSON format'''
        raise NotImplementedError('Unable to send a link message in current WeWork')
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse link message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        title:str = xml_tree.find('Title').text
        desc:str = xml_tree.find('Description').text
        url:str = xml_tree.find('Url').text
        pic_url:str = xml_tree.find('PicUrl').text
        msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, agent_id, title, desc, url, pic_url, create_time=create_time, msg_id=msg_id)

