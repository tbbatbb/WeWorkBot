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

    def __init__(self, to_username: str, from_username: str, articles:List[News], **kwargs) -> None:
        super().__init__(to_username, from_username, **kwargs)
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
        return json.dumps({"touser":self.to_username,"msgtype":"news","agentid":self.agent_id,"news":{"articles":articles}})
    
    @classmethod
    def from_xml(cls, xml_tree: Element):
        '''Parse news message from XML object'''
        raise NotImplementedError('Unable to receive and parse a news message in current WeWork')

