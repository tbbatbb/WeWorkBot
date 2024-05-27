#!python3.9

import json
from . import Message
from xml.etree.ElementTree import Element
from typing import Any, Dict, List, NamedTuple

class News(NamedTuple):
    '''A piece of single news'''
    title:str
    description:str
    pic_url:str
    url:str = None
    appid:str = None
    pagepath:str = None

class NewsMessage(Message):

    # message type 
    type:str = 'news'
    # handler key 
    key:str = 'news'

    def __init__(self, to_username: str, from_username: str, agent_id: str, articles:List[News], **kwargs) -> None:
        super().__init__(to_username, from_username, agent_id, **kwargs)
        # the news list 
        self.articles:List[News] = articles

    def to_xml(self) -> str:
        '''Represent news message in XML format'''
        news_str:str = ''.join(map(lambda n:f'<item><Title><![CDATA[{n.title}]]></Title><Description><![CDATA[{n.description}]]></Description><PicUrl><![CDATA[{n.pic_url}]]></PicUrl><Url><![CDATA[{n.url}]]></Url></item>', self.articles))
        return f'''<xml><ToUserName><![CDATA[{self.to_username}]]></ToUserName><FromUserName><![CDATA[{self.from_username}]]></FromUserName><CreateTime>{self.create_time}</CreateTime><MsgType><![CDATA[news]]></MsgType><ArticleCount>{len(self.articles)}</ArticleCount><Articles>{news_str}</Articles></xml>'''

    def to_json(self) -> str:
        '''Represent news message in JSON format'''
        articles:List[Dict[str, str]] = []
        for n in self.articles:
            article:Dict[str, str] = {"title":n.title,"description":n.description}
            if n.url is not None: article["url"] = n.url
            if n.appid is not None: 
                article["appid"] = n.appid
                article["pagepath"] = n.pagepath
            articles.append(article)
        data:Dict[str, Any] = {"msgtype":"news","news":{"articles":articles},"safe":1 if self.safe else 0,"enable_id_trans":1 if self.enable_id_trans else 0,"enable_duplicate_check":1 if self.enable_duplicate_check else 0,"duplicate_check_interval":self.duplicate_check_interval}
        if self.for_chat: data.update({"chatid":self.chat_id})
        elif not self.for_group_bot: data.update({"touser":self.to_username,"agentid":self.agent_id})
        return json.dumps(data)
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse news message from XML object'''
        raise NotImplementedError('Unable to receive and parse a news message in current WeWork')

