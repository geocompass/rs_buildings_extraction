"""
 Created by 七月 on 2018/5/7.
 微信公众号：林间有风
"""
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error_code import ServerError
from datetime import date

__author__ = '七月'


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder



