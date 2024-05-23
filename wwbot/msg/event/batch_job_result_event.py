#!python3.9

from xml.etree.ElementTree import Element
from . import EventMessage

class BatchJobResultEventMessage(EventMessage):

    # handler key 
    key:str = 'event.batch_job_result'

    def __init__(self, to_username: str, from_username: str, agent_id: str, event: str, job_id:str, job_type:str, err_code:str, err_msg:str, event_key: str = '', **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, event, event_key=event_key, **kwargs)
        # job id 
        self.job_id:str = job_id
        # job type
        self.job_type:str = job_type
        # error code 
        self.err_code:str = err_code
        # error message 
        self.err_msg:str = err_msg

    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse batch job result event message from XML object'''
        to_username:str = xml_tree.find('ToUserName').text
        from_username:str = xml_tree.find('FromUserName').text
        create_time:str = xml_tree.find('CreateTime').text
        event:str = xml_tree.find('Event').text
        event_key:str = '' if xml_tree.find('EventKey') is None else xml_tree.find('EventKey').text
        job_id:str = xml_tree.find('BatchJob/JobId').text
        job_type:str = xml_tree.find('BatchJob/JobType').text
        err_code:str = xml_tree.find('BatchJob/ErrCode').text
        err_msg:str = xml_tree.find('BatchJob/ErrMsg').text
        # msg_id:str = xml_tree.find('MsgId').text
        agent_id:str = xml_tree.find('AgentID').text

        return cls(to_username, from_username, agent_id, event, job_id, job_type, err_code, err_msg, event_key=event_key, create_time=create_time)