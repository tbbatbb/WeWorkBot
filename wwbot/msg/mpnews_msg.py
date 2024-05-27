#!python3.9

import json
from . import Message
from xml.etree.ElementTree import Element
from typing import Any, Dict, List, NamedTuple

class MPNews(NamedTuple):
    '''A piece of single mpnews'''
    title:str
    thumb_media_id:str
    content:str
    author:str = None
    content_source_url:str = None
    desc:str = None

class MPNewsMessage(Message):

    # message type 
    type:str = 'mpnews'
    # handler key 
    key:str = 'mpnews'

    def __init__(self, to_username: str, from_username: str, agent_id: str, articles:List[MPNews], **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
        # the mpnews list 
        self.articles:List[MPNews] = articles

    def to_xml(self) -> str:
        '''Represent mpnews message in XML format'''
        raise NotImplementedError('Unable to reply with a mpnews message in current WeWork')

    def to_json(self) -> str:
        '''Represent mpnews message in JSON format'''
        articles:List[Dict[str, str]] = []
        for n in self.articles:
            article:Dict[str, str] = {"title":n.title,"thumb_media_id":n.thumb_media_id,"content":n.content}
            if n.author is not None: article["author"] = n.author
            if n.content_source_url is not None: article["content_source_url"] = n.content_source_url
            if n.desc is not None: article["digest"] = n.desc
            articles.append(article)
        data:Dict[str, Any] = {"msgtype":"mpnews","mpnews":{"articles":articles},"safe":1 if self.safe else 0,"enable_id_trans":1 if self.enable_id_trans else 0,"enable_duplicate_check":1 if self.enable_duplicate_check else 0,"duplicate_check_interval":self.duplicate_check_interval}
        if self.for_chat: data.update({"chatid":self.chat_id})
        elif not self.for_group_bot: data.update({"touser":self.to_username,"agentid":self.agent_id})
        return json.dumps(data)
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse mpnews message from XML object'''
        raise NotImplementedError('Unable to receive and parse a mpnews message in current WeWork')

