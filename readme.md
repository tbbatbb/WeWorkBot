# WeWorkBot

为企业微信自建应用构建的机器人，能够实现对各种类型消息的被动回复和主动发送。

现支持：
- 接收处理文本(`text`)、图片(`image`)、语音(`voice`)、视频(`video`)、位置(`location`)和链接(`link`)等消息类型；
- 以文本(`text`)、图片(`image`)、语音(`voice`)、视频(`video`)、图文(`news`)等消息类型进行被动回复；
- 以文本(`text`)、图片(`image`)、语音(`voice`)、视频(`video`)、Markdown(`markdown`)、图文(`mpnews`)、图文(`news`)、文本卡片(`textcard`)、文件(`file`)等消息类型主动发送应用消息。

**注意！当前版本虽然能实现最基础的功能，但是库中代码接口定义尚未稳定，后期版本可能会对接口定义与使用方法有较大更改，望知悉！**

**注意！当前版本虽然能实现最基础的功能，但是库中代码接口定义尚未稳定，后期版本可能会对接口定义与使用方法有较大更改，望知悉！**

**注意！当前版本虽然能实现最基础的功能，但是库中代码接口定义尚未稳定，后期版本可能会对接口定义与使用方法有较大更改，望知悉！**

## 依赖

依赖的库不多，可以参考`requirements.txt`。

## 安装

**目前支持`Python >= 3.9`，其余版本未经测试。**

Python库现已发布，可以通过`pip install wwbot`进行安装。

## 示例代码

如下示例代码展示`WeWorkBot`的简单使用。该示例展示了如何回复**文本类型**(`text`)的消息：
```python
from flask import Flask
from wwbot import WWBot
from wwbot.msg import Message, TextMessage

# 注册一个文本消息的事件监听
@WWBot.on('text')
def text_handler(msg:TextMessage) -> Message:
    '''
    msg参数代表接收到的消息被解析后的实例
    '''
    # 从消息中提取消息内容字段
    # 关于接收到的消息格式具体定义，参考 https://developer.work.weixin.qq.com/document/path/90239
    msg_content:str = msg.content
    # 作为示例，直接使用接收到的消息作为回复，相当于一个 echo bot
    return TextMessage(msg.from_username, msg.to_username, msg_content)

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
# 接收消息回调时的url path部分
callback_path:str = '/wwbot'

# 配置机器人
WWBot.config(app, corp_id, corp_secret, token, aes_key, callback_path=callback_path)

if __name__ == '__main__':
    app.run('0.0.0.0', 31221)
```
更加完整的例子请参考`sample.py`。

## TODO List

- [x] 将“接口验证”和“消息接收”的url部分合并，不需要两次注册
- [ ] 实现临时资源上传，从而能够发送任意语音或是视频等多媒体消息
- [x] 支持更多的应用消息类型
- [x] 将消息的定义和转换变得更加优雅
- [x] 创建成python库。现在这个方式，不够优雅
- [ ] 完善Doc和Readme，包括获取corp_id等参数的方法

## 说明

代码随缘更新，主要看有没有空。一般会在周末更新比较频繁。