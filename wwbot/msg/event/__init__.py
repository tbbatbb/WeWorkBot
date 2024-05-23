#!python3.9

from .. import Message
from xml.etree.cElementTree import Element

class EventMessage(Message):

    # message type 
    type:str = 'event'
    # handler key 
    key:str = 'event'

    def __init__(self, to_username: str, from_username: str, agent_id: str, event:str, event_key:str='', **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
        # event name 
        self.event:str = event
        # event key 
        self.event_key:str = event_key

    def to_xml(self) -> str:
        '''Represent event message in XML format'''
        raise NotImplementedError('Unable to reply with an event message in current WeWork')

    def to_json(self) -> str:
        '''Represent event message in JSON format'''
        raise NotImplementedError('Unable to send an event message in current WeWork')

from .subscribe_event import SubscribeEventMessage
from .enter_agent_event import EnterAgentEventMessage

def event_msg_from_xml(xml_tree:Element) -> Message:
    '''Parse message from xml tree'''
    event:str = xml_tree.find('Event').text.lower()
    if event in ['subscribe', 'unsubscribe']: return SubscribeEventMessage.from_xml(xml_tree)
    if event == 'enter_agent': return EnterAgentEventMessage.from_xml(xml_tree)
    if event == 'voice': return VoiceMessage.from_xml(xml_tree)
    if event == 'video': return VideoMessage.from_xml(xml_tree)
    if event == 'link': return LinkMessage.from_xml(xml_tree)
    if event == 'location': return LocationMessage.from_xml(xml_tree)
    Message.logger.warn('Unregistered message type')
