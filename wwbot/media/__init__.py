#!python3.9

import os, requests, mimetypes
from ..lib import Logger
from requests import Response
from requests_toolbelt import MultipartEncoder
from typing import Literal, NamedTuple

mimetypes.init()

class UploadResult(NamedTuple):
    type:str
    media_id:str
    created_at:str
    err_code:int
    err_msg:str

class UploadImageResult(NamedTuple):
    url:str
    err_code:int
    err_msg:str 

class Media:
    
    logger:Logger = Logger('Media')

    @classmethod
    def __upload(cls, url:str, file_path:str) -> Response:
        '''Upload files to a specific url'''
        filename:str = os.path.basename(file_path)
        mimetype:str = mimetypes.guess_type(file_path)[0]
        if mimetype is None: mimetype = 'application/octet-stream'
        inf = open(file_path, 'rb')
        files = {
            'media': (
                filename,
                inf,
                mimetype
            ),
            'filename': filename,
            'Content-Disposition': 'form-data;'
        }
        form_data = MultipartEncoder(files)
        try:
            resp:Response = requests.post(url, data=form_data, headers={'Content-Type': form_data.content_type})
            inf.close()
            return resp
        except Exception as e:
            cls.logger.error(e)
            return None

    @classmethod
    def upload(cls, access_token:str, file_type:Literal['image', 'voice', 'video', 'file'], file_path:str) -> UploadResult:
        '''Upload media files synchronously'''
        url:str = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type={file_type}'
        resp:Response = cls.__upload(url, file_path)
        if resp is None: return resp
        resp_json = resp.json()
        return UploadResult(resp_json['type'], resp_json['media_id'], resp_json['created_at'], resp_json['errcode'], resp_json['errmsg'])
        
    @classmethod
    def uploadimg(cls, access_token:str, file_path:str) -> UploadImageResult:
        '''Upload image'''
        url:str = f'https://qyapi.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}'
        resp:Response = cls.__upload(url, file_path)
        if resp is None: return resp
        resp_json = resp.json()
        return UploadImageResult(resp_json['url'], resp_json['errcode'], resp_json['errmsg'])
