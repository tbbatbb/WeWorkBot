#!python3.9

import os, requests, mimetypes
from ..lib import Logger
from requests import Response
from requests_toolbelt import MultipartEncoder
from typing import Literal, NamedTuple, Dict, Any

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

class UploadByURLResult(NamedTuple):
    job_id:str
    err_code:int
    err_msg:str 

class GetUploadByURLDetail(NamedTuple):
    media_id:str
    created_at:str
    err_code:int
    err_msg:str

class GetUploadByURLResult(NamedTuple):
    detail:GetUploadByURLDetail
    status:int
    err_code:int
    err_msg:str 

class Media:
    
    logger:Logger = Logger('Media')

    @classmethod
    def __upload_file(cls, url:str, file_path:str) -> Response:
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
    def __post_req(cls, url:str, data:Dict[str, Any]) -> Response:
        '''Send POST request'''
        try:
            resp:Response = requests.post(url, json=data)
            return resp
        except Exception as e:
            cls.logger.error(e)
            return None

    @classmethod
    def upload(cls, access_token:str, file_type:Literal['image', 'voice', 'video', 'file'], file_path:str) -> UploadResult:
        '''Upload media files synchronously'''
        url:str = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type={file_type}'
        resp:Response = cls.__upload_file(url, file_path)
        if resp is None: return resp
        resp_json = resp.json()
        return UploadResult(resp_json['type'], resp_json['media_id'], resp_json['created_at'], resp_json['errcode'], resp_json['errmsg'])

    @classmethod
    def upload_by_url(cls, access_token:str, scene:int, type:Literal['video', 'file'], filename:str, url:str, md5:str) -> UploadByURLResult:
        '''Upload files by providing url'''
        req_url:str = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload_by_url?access_token={access_token}'
        resp:Response = cls.__post_req(req_url, {
            'scene': scene,
            'type': type,
            'filename': filename,
            'url': url,
            'md5': md5
        })
        if resp is None: return resp
        resp_json = resp.json()
        return UploadByURLResult(resp_json['jobid'], resp_json['errcode'], resp_json['errmsg'])
        
    @classmethod
    def get_upload_by_url_result(cls, access_token:str, job_id:str) -> GetUploadByURLResult:
        '''Get the result for the job "upload by url"'''
        req_url:str = f'https://qyapi.weixin.qq.com/cgi-bin/media/get_upload_by_url_result?access_token={access_token}'
        resp:Response = cls.__post_req(req_url, {'jobid': job_id})
        if resp is None: return resp
        resp_json = resp.json()
        return GetUploadByURLResult(
            GetUploadByURLDetail(resp_json['detail']['media_id'], resp_json['detail']['created_at'], resp_json['detail']['errcode'], resp_json['detail']['errmsg']),
            resp_json['status'],
            resp_json['errcode'],
            resp_json['errmsg']
        )

    @classmethod
    def uploadimg(cls, access_token:str, file_path:str) -> UploadImageResult:
        '''Upload image'''
        url:str = f'https://qyapi.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}'
        resp:Response = cls.__upload_file(url, file_path)
        if resp is None: return resp
        resp_json = resp.json()
        return UploadImageResult(resp_json['url'], resp_json['errcode'], resp_json['errmsg'])

    @classmethod
    def download(cls, access_token:str, media_id:str, save_to:str) -> bool:
        '''Download an uploaded file with media_id'''
        url:str = f'https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token={access_token}&media_id={media_id}'
        try:
            resp:Response = requests.get(url, stream=True)
            with open(save_to, 'wb') as outf:
                for iter in resp.iter_content(chunk_size=1024*32):
                    outf.write(iter)
            return True
        except Exception as e:
            cls.logger.error(e)
            return False