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


from .view_event import ViewEventMessage
from .click_event import ClickEventMessage
from .location_event import LocationEventMessage
from .subscribe_event import SubscribeEventMessage
from .pic_weixin_event import PicWeixinEventMessage
from .enter_agent_event import EnterAgentEventMessage
from .pic_sysphoto_event import PicSysPhotoEventMessage
from .scancode_push_event import ScanCodePushEventMessage
from .location_select_event import LocationSelectEventMessage
from .batch_job_result_event import BatchJobResultEventMessage
from .scancode_waitmsg_event import ScanCodeWaitMsgEventMessage
from .pic_photo_or_album_event import PicPhotoOrAlbumEventMessage
from .share_agent_change_event import ShareAgentChangeEventMessage
from .share_chain_change_event import ShareChainChangeEventMessage
from .upload_media_job_finish_event import UploadMediaJobFinishEventMessage

def event_msg_from_xml(xml_tree:Element) -> Message:
    '''Parse message from xml tree'''
    event:str = xml_tree.find('Event').text.lower()
    if event in ['subscribe', 'unsubscribe']: return SubscribeEventMessage.from_xml(xml_tree)
    if event == 'view': return ViewEventMessage.from_xml(xml_tree)
    if event == 'click': return ClickEventMessage.from_xml(xml_tree)
    if event == 'location': return LocationEventMessage.from_xml(xml_tree)
    if event == 'pic_weixin': return PicWeixinEventMessage.from_xml(xml_tree)
    if event == 'enter_agent': return EnterAgentEventMessage.from_xml(xml_tree)
    if event == 'pic_sysphoto': return PicSysPhotoEventMessage.from_xml(xml_tree)
    if event == 'scancode_push': return ScanCodePushEventMessage.from_xml(xml_tree)
    if event == 'location_select': return LocationSelectEventMessage.from_xml(xml_tree)
    if event == 'batch_job_result': return BatchJobResultEventMessage.from_xml(xml_tree)
    if event == 'scancode_waitmsg': return ScanCodeWaitMsgEventMessage.from_xml(xml_tree)
    if event == 'pic_photo_or_album': return PicPhotoOrAlbumEventMessage.from_xml(xml_tree)
    if event == 'share_chain_change': return ShareChainChangeEventMessage.from_xml(xml_tree)
    if event == 'share_agent_change': return ShareAgentChangeEventMessage.from_xml(xml_tree)
    if event == 'upload_media_job_finish': return UploadMediaJobFinishEventMessage.from_xml(xml_tree)
    Message.logger.warn('Unregistered event type')
