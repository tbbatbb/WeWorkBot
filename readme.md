# WeWorkBot

为企业微信自建应用构建的机器人，能够实现对各种类型消息的被动回复和主动发送。

现支持：
- 接收处理文本(`text`)、图片(`image`)、语音(`voice`)、视频(`video`)、位置(`location`)和链接(`link`)等消息类型；
- 以文本(`text`)、图片(`image`)、语音(`voice`)、视频(`video`)、图文(`news`)等消息类型进行被动回复；
- 以文本(`text`)、图片(`image`)、语音(`voice`)、视频(`video`)等消息类型主动发送应用消息。

## 示例代码

如下示例代码展示`WeWorkBot`的简单使用。该示例展示了如何回复**文本类型**(`text`)的消息：
```python
from flask import Flask
from wwbot import WWBot
from xml.etree.cElementTree import Element

# 注册一个文本消息的事件监听
@WWBot.on('text')
def text_handler(from_user:str, to_user:str, msg_xml:Element) -> str:
    '''
    三个参数，分别代表：
    from_user: 消息来源用户的id
    to_user: 接收消息的用户id。由于此时是企业应用作为消息的接收方，因此此时该值通常为企业id，即与corp_id相同
    '''
    # 从消息中提取消息内容字段
    # 关于接收到的消息格式具体定义，参考 https://developer.work.weixin.qq.com/document/path/90239
    msg_content:str = msg_xml.find('Content').text
    # 作为示例，直接使用接收到的消息作为回复，相当于一个 echo bot
    return WWBot.format_text_msg(from_user, to_user, msg_content)

# WeWorkBot运行在Flask框架之上
app:Flask = Flask('WWBot')
# 企业ID 
corp_id:str = 'corp_id'
# 企业自建应用的secret 可以创建自建应用后在应用详情页面查看
corp_secret:str = 'corp_secret'
# 自建应用启用API接收消息时，配置的“Token”参数
token:str = 'token'
# 自建应用启用API接收消息时，配置的“EncodingAESKey”参数
aes_key:bytes = base64.b64decode('aes_key')

# 配置机器人
WWBot.config(corp_id, corp_secret, token, aes_key)

# 那两个 /wwbot 指的是配置自建应用API接收消息时所填入URL的path部分
@WWBot.verify_handler(app, '/wwbot')
@WWBot.request_handler(app, '/wwbot')
def useless(): 
    # 该函数在当前版本中并不会被调用，所以随意定义
    pass

if __name__ == '__main__':
    app.run('0.0.0.0', 31221)
```

## TODO List

- [ ] 将“接口验证”和“消息接收”的url部分合并，不需要两次注册
- [ ] 支持更多的应用消息类型
- [ ] 将消息的定义和转换变得更加优雅
- [ ] 创建成python库。现在这个方式，不够优雅
- [ ] 完善Doc和Readme，包括获取corp_id等参数的方法